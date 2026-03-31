from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

import httpx
import yaml
from bs4 import BeautifulSoup


NOTICE_LIST_URL_TEMPLATE = "https://crimsondesert.pearlabyss.com/{locale}/News/Notice"
SUPPORTED_TYPES = {"patch_note", "known_issue", "faq"}


@dataclass
class NoticeSummary:
    board_no: int
    locale: str
    title: str
    url: str
    source_type: str


@dataclass
class NoticeDetail:
    board_no: int
    locale: str
    title: str
    url: str
    source_type: str
    published_at: str
    fetched_at: str
    raw_text: str
    list_items: list[str]
    meta_description: str


@dataclass
class GeneratedDocument:
    filename: str
    source_type: str
    title: str
    content: str


def fetch_notice_summaries(
    *,
    locale: str = "ko-KR",
    pages: int = 4,
    source_types: set[str] | None = None,
    timeout: float = 20.0,
) -> list[NoticeSummary]:
    allowed_types = source_types or SUPPORTED_TYPES
    summaries: list[NoticeSummary] = []
    seen_board_numbers: set[int] = set()

    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        for page in range(1, max(1, pages) + 1):
            response = client.get(
                NOTICE_LIST_URL_TEMPLATE.format(locale=locale),
                params={"_pageNo": page, "_categoryNo": 0},
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for anchor in soup.select("a.item_box[href*='/News/Notice/Detail']"):
                href = anchor.get("href", "").strip()
                board_no = _extract_board_no(href)
                if board_no is None or board_no in seen_board_numbers:
                    continue

                title_node = anchor.select_one(".info_wrap .title")
                title = _clean_text(title_node.get_text(" ", strip=True) if title_node else "")
                if not title:
                    continue

                source_type = classify_notice_type(title)
                if source_type is None or source_type not in allowed_types:
                    continue

                summaries.append(
                    NoticeSummary(
                        board_no=board_no,
                        locale=locale,
                        title=title,
                        url=urljoin(str(response.url), href),
                        source_type=source_type,
                    )
                )
                seen_board_numbers.add(board_no)

    return summaries


def fetch_notice_detail(summary: NoticeSummary, *, timeout: float = 20.0) -> NoticeDetail:
    response = httpx.get(summary.url, follow_redirects=True, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title_node = soup.select_one("#boardTitle") or soup.select_one(".board_header .title")
    date_node = soup.select_one(".board_header .date")
    content_node = soup.select_one(".board_content .inner.contents_area")
    meta_node = soup.select_one("meta[name='description']")

    if title_node is None or content_node is None:
        raise ValueError(f"Could not parse official notice detail: {summary.url}")

    raw_text = extract_raw_text(content_node.get_text("\n", strip=True))
    list_items = []
    for item in content_node.select("li"):
        if item.find_parent("li") is not None:
            continue
        text = _clean_text(item.get_text(" ", strip=True))
        if text:
            list_items.append(text)

    return NoticeDetail(
        board_no=summary.board_no,
        locale=summary.locale,
        title=_clean_text(title_node.get_text(" ", strip=True)),
        url=str(response.url),
        source_type=summary.source_type,
        published_at=parse_notice_datetime(_clean_text(date_node.get_text(" ", strip=True) if date_node else "")),
        fetched_at=datetime.now(timezone.utc).isoformat(),
        raw_text=raw_text,
        list_items=dedupe_keep_order(list_items),
        meta_description=_clean_text(meta_node.get("content", "") if meta_node else ""),
    )


def generate_documents(detail: NoticeDetail) -> list[GeneratedDocument]:
    if detail.source_type == "patch_note":
        return [build_patch_document(detail)]
    if detail.source_type == "known_issue":
        return build_known_issue_documents(detail)
    if detail.source_type == "faq":
        return build_faq_documents(detail)
    return []


def write_documents(documents: list[GeneratedDocument], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    for document in documents:
        path = output_dir / document.filename
        path.write_text(document.content, encoding="utf-8")
        written_paths.append(path)
    return written_paths


def classify_notice_type(title: str) -> str | None:
    lowered = title.casefold()
    if any(keyword in lowered for keyword in ("patch notes", "patch note", "패치 노트")):
        return "patch_note"
    if any(keyword in lowered for keyword in ("known issues", "known issue", "알려진 현상", "알려진 문제점", "확인된 현상")):
        return "known_issue"
    if any(keyword in lowered for keyword in ("faq", "자주 묻는 질문")):
        return "faq"
    return None


def build_patch_document(detail: NoticeDetail) -> GeneratedDocument:
    detail_lines = detail.list_items or extract_lines(detail.raw_text, minimum_length=12, limit=20)
    version = extract_patch_version(detail.title) or f"board-{detail.board_no}"
    payload = {
        "source_type": "patch_note",
        "title": detail.title,
        "source_url": detail.url,
        "published_at": detail.published_at,
        "fetched_at": detail.fetched_at,
        "version": version,
        "platforms": detect_platforms(f"{detail.title}\n{detail.raw_text}"),
        "summary": summarize_text(detail.meta_description or detail.raw_text, limit=220),
        "related_issue_slugs": [],
        "details": [
            {
                "category": "Official Notes",
                "items": detail_lines or [summarize_text(detail.raw_text, limit=160)],
            }
        ],
        "landing": build_patch_landing_payload(detail, version, detail_lines),
    }
    return GeneratedDocument(
        filename=f"patch-board{detail.board_no}-{slugify(version)}.md",
        source_type="patch_note",
        title=detail.title,
        content=build_frontmatter_document(payload, detail.raw_text),
    )


def build_known_issue_documents(detail: NoticeDetail) -> list[GeneratedDocument]:
    issue_lines = detail.list_items or extract_lines(detail.raw_text, minimum_length=25, limit=10)
    if not issue_lines:
        issue_lines = [summarize_text(detail.raw_text, limit=180)]

    last_seen_at = extract_last_updated_at(detail.raw_text) or detail.published_at
    platforms = detect_platforms(f"{detail.title}\n{detail.raw_text}")
    used_slugs: set[str] = set()
    documents: list[GeneratedDocument] = []

    for index, line in enumerate(issue_lines, start=1):
        slug = ensure_unique_slug(slugify(line)[:60] or f"known-issue-{detail.board_no}-{index}", used_slugs)
        title = summarize_text(line, limit=72)
        payload = {
            "source_type": "known_issue",
            "title": title,
            "source_url": detail.url,
            "published_at": detail.published_at,
            "fetched_at": detail.fetched_at,
            "slug": slug,
            "symptom_summary": summarize_text(line, limit=180),
            "category": detect_issue_category(line),
            "status": detect_issue_status(f"{detail.title}\n{detail.raw_text}"),
            "platforms": platforms,
            "first_seen_at": detail.published_at,
            "last_seen_at": last_seen_at,
            "escalation_needed": requires_escalation(line),
            "related_patch_versions": [],
            "workaround_steps": [],
            "landing": build_issue_landing_payload(detail, slug, title, line),
        }
        documents.append(
            GeneratedDocument(
                filename=f"issue-board{detail.board_no}-{index:02d}-{slug}.md",
                source_type="known_issue",
                title=title,
                content=build_frontmatter_document(payload, detail.raw_text),
            )
        )

    return documents


def build_faq_documents(detail: NoticeDetail) -> list[GeneratedDocument]:
    faq_pairs = extract_faq_pairs(detail.raw_text)
    if not faq_pairs:
        question = normalize_faq_question(detail.title, detail.raw_text)
        faq_pairs = [(question, detail.meta_description or detail.raw_text)]

    documents: list[GeneratedDocument] = []
    used_names: set[str] = set()
    for index, (question_text, answer_text) in enumerate(faq_pairs, start=1):
        question = normalize_faq_question(question_text, detail.raw_text)
        answer = normalize_faq_answer(answer_text)
        slug = ensure_unique_slug(slugify(question)[:60] or f"faq-{detail.board_no}-{index}", used_names)
        payload = {
            "source_type": "faq",
            "title": f"FAQ: {question}",
            "source_url": detail.url,
            "published_at": detail.published_at,
            "fetched_at": detail.fetched_at,
            "question": question,
            "answer": answer,
            "tags": detect_faq_tags(f"{question}\n{answer}"),
            "related_issue_slugs": [],
            "related_patch_versions": [],
        }
        documents.append(
            GeneratedDocument(
                filename=f"faq-board{detail.board_no}-{slug}.md",
                source_type="faq",
                title=payload["title"],
                content=build_frontmatter_document(payload, detail.raw_text),
            )
        )
    return documents


def build_frontmatter_document(payload: dict[str, object], raw_text: str) -> str:
    frontmatter = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=1000).strip()
    return f"---\n{frontmatter}\n---\n{raw_text.strip()}\n"


def parse_notice_datetime(value: str) -> str:
    normalized = value.replace("\xa0", " ").strip()
    patterns = [
        "%b %d, %Y, %H:%M (UTC)",
        "%Y.%m.%d %H:%M (UTC)",
        "%Y/%m/%d %H:%M UTC",
        "%Y/%m/%d %H:%M",
    ]
    for pattern in patterns:
        try:
            return datetime.strptime(normalized, pattern).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return datetime.now(timezone.utc).isoformat()


def extract_raw_text(text: str) -> str:
    return "\n".join(part for part in (_clean_text(line) for line in text.splitlines()) if part)


def extract_patch_version(title: str) -> str | None:
    match = re.search(r"(\d+\.\d+\.\d+)", title)
    return match.group(1) if match else None


def extract_last_updated_at(raw_text: str) -> str | None:
    patterns = [
        r"Last updated:\s*([0-9]{4}/[0-9]{2}/[0-9]{2}\s+[0-9]{2}:[0-9]{2}\s*UTC)",
        r"최종\s*업데이트[:\s]*([0-9]{4}[./][0-9]{2}[./][0-9]{2}\s+[0-9]{2}:[0-9]{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            return parse_notice_datetime(match.group(1))
    return None


def extract_lines(raw_text: str, *, minimum_length: int, limit: int) -> list[str]:
    lines = [_clean_text(line.lstrip("-*• ").strip()) for line in raw_text.splitlines()]
    filtered = [line for line in lines if len(line) >= minimum_length]
    return dedupe_keep_order(filtered[:limit])


def summarize_text(text: str, *, limit: int) -> str:
    normalized = _clean_text(text)
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def detect_platforms(text: str) -> list[str]:
    lowered = text.casefold()
    platforms: list[str] = []
    if any(keyword in lowered for keyword in ("pc", "steam", "windows", "nvidia", "amd", "dlss", "fsr")):
        platforms.append("PC")
    if any(keyword in lowered for keyword in ("playstation", "ps5", "플레이스테이션")):
        platforms.append("PS5")
    if any(keyword in lowered for keyword in ("xbox", "엑스박스")):
        platforms.append("Xbox Series X|S")
    if "mac" in lowered:
        platforms.append("Mac")
    return dedupe_keep_order(platforms)


def detect_issue_category(text: str) -> str:
    lowered = text.casefold()
    category_map = {
        "visual": ("flicker", "shadow", "hair", "texture", "graphic", "visual", "blur", "display", "화면", "그래픽"),
        "performance": ("fps", "stutter", "performance", "lag", "frame", "끊김", "프레임"),
        "crash": ("crash", "freeze", "hang", "멈춤", "튕김"),
        "audio": ("audio", "sound", "voice", "소리", "오디오"),
        "controls": ("controller", "input", "keyboard", "mouse", "패드", "입력"),
        "progression": ("quest", "mission", "progress", "save", "퀘스트", "진행", "저장"),
    }
    for category, keywords in category_map.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "general"


def detect_issue_status(text: str) -> str:
    lowered = text.casefold()
    if any(keyword in lowered for keyword in ("resolved", "fixed", "해결")):
        return "monitoring"
    if any(keyword in lowered for keyword in ("investigating", "investigate", "확인 중", "조사 중")):
        return "investigating"
    return "monitoring"


def requires_escalation(text: str) -> bool:
    lowered = text.casefold()
    return any(
        keyword in lowered
        for keyword in ("crash", "freeze", "save", "unable", "cannot progress", "멈춤", "저장", "진행 불가")
    )


def normalize_faq_question(title: str, raw_text: str) -> str:
    cleaned = _clean_text(re.sub(r"^(faq[:\s-]*|자주 묻는 질문[:\s-]*)", "", title, flags=re.IGNORECASE))
    if cleaned:
        return cleaned
    return summarize_text(raw_text, limit=90) or "공식 FAQ"


def normalize_faq_answer(text: str) -> str:
    cleaned_lines = [_clean_text(line) for line in text.splitlines()]
    filtered = [line for line in cleaned_lines if line and line not in {"[", "]", "링크", "바로 가기"}]
    return " ".join(filtered).strip()


def extract_faq_pairs(raw_text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    current_question: str | None = None
    current_answer_lines: list[str] = []

    for raw_line in raw_text.splitlines():
        line = _clean_text(raw_line)
        if not line or line in {"[", "]", "링크", "바로 가기"}:
            continue
        if is_heading_line(line):
            continue
        if is_faq_question(line):
            if current_question is not None:
                pairs.append((current_question, "\n".join(current_answer_lines).strip()))
            current_question = line
            current_answer_lines = []
            continue
        if current_question is not None:
            current_answer_lines.append(line)

    if current_question is not None:
        pairs.append((current_question, "\n".join(current_answer_lines).strip()))

    return [(question, answer) for question, answer in pairs if question and answer]


def is_faq_question(text: str) -> bool:
    lowered = text.casefold()
    if "://" in text or lowered.startswith(("ms-windows-store:", "http://", "https://")):
        return False
    if "?" in text or "？" in text:
        return True
    return any(
        lowered.endswith(ending)
        for ending in (
            "지원하나요",
            "되나요",
            "있나요",
            "인가요",
            "해야 하나요",
            "가능한가요",
            "받을 수 있나요",
            "확인하나요",
            "안됩니다",
        )
    )


def is_heading_line(text: str) -> bool:
    if len(text) > 20:
        return False
    if any(char in text for char in "?!.:;[]()"):
        return False
    lowered = text.casefold()
    return any(
        keyword in lowered
        for keyword in (
            "플랫폼",
            "시스템",
            "고객지원",
            "기능",
            "에디션",
            "보너스",
            "아이템",
        )
    )


def build_patch_landing_payload(detail: NoticeDetail, version: str, detail_lines: list[str]) -> dict[str, object]:
    top_lines = detail_lines[:3] or [summarize_text(detail.raw_text, limit=160)]
    faq_items = [
        {
            "question": "이번 패치에서 먼저 봐야 할 것은 무엇인가요?",
            "answer": top_lines[0],
        }
    ]
    if len(top_lines) > 1:
        faq_items.append(
            {
                "question": "가장 눈에 띄는 추가 변경점은 무엇인가요?",
                "answer": top_lines[1],
            }
        )

    body_lines = "\n".join(f"- {line}" for line in top_lines)
    return {
        "title": detail.title,
        "meta_description": summarize_text(detail.meta_description or detail.raw_text, limit=150),
        "canonical_path": f"/ko/patches/{version}",
        "body_markdown": f"{summarize_text(detail.raw_text, limit=180)}\n\n{body_lines}",
        "faq_items": faq_items,
    }


def build_issue_landing_payload(detail: NoticeDetail, slug: str, title: str, line: str) -> dict[str, object]:
    workaround_hint = "최신 패치 적용 여부와 동일 증상 재현 조건을 먼저 기록해 두세요."
    if "xbox" in line.casefold():
        workaround_hint = "Xbox 관련 계정 동기화와 앱 업데이트 여부를 먼저 확인하세요."
    if any(keyword in line.casefold() for keyword in ("blur", "흐리", "뭉개", "flicker", "깜빡")):
        workaround_hint = "그래픽 옵션과 업스케일러 변경 전후를 같은 장면에서 비교하는 것이 좋습니다."

    return {
        "title": title,
        "meta_description": summarize_text(detail.meta_description or line, limit=150),
        "canonical_path": f"/ko/issues/{slug}",
        "body_markdown": f"{summarize_text(line, limit=180)}\n\n- 최신 공지 기준 상태 확인\n- 재현 조건 기록\n- 관련 패치 적용 여부 확인",
        "faq_items": [
            {
                "question": "이 문제를 먼저 어떻게 확인해야 하나요?",
                "answer": workaround_hint,
            }
        ],
    }


def detect_faq_tags(text: str) -> list[str]:
    lowered = text.casefold()
    tags: list[str] = []
    tag_map = {
        "patch": ("patch", "version", "패치", "버전"),
        "graphics": ("dlss", "fsr", "graphics", "그래픽"),
        "install": ("install", "download", "설치", "다운로드"),
        "controller": ("controller", "input", "패드", "입력"),
        "account": ("account", "login", "계정", "로그인"),
    }
    for tag, keywords in tag_map.items():
        if any(keyword in lowered for keyword in keywords):
            tags.append(tag)
    return tags


def slugify(value: str) -> str:
    normalized = value.casefold()
    normalized = re.sub(r"[^\w\s-]", " ", normalized)
    normalized = re.sub(r"[\s_]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized.strip("-")


def ensure_unique_slug(slug: str, used_slugs: set[str]) -> str:
    candidate = slug or "item"
    index = 2
    while candidate in used_slugs:
        candidate = f"{slug}-{index}"
        index += 1
    used_slugs.add(candidate)
    return candidate


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    for item in items:
        if item not in seen:
            results.append(item)
            seen.add(item)
    return results


def _extract_board_no(url: str) -> int | None:
    parsed = urlparse(url)
    value = parse_qs(parsed.query).get("_boardNo", [None])[0]
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()
