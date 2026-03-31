from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from sqlmodel import Session, select

from app.models import Issue, Patch
from app.services.search import rebuild_search_index
from app.services.seed import (
    count_entities,
    replace_issue_workaround_steps,
    replace_patch_links_for_issue,
    replace_patch_links_for_patch,
    upsert_faq_entry_record,
    upsert_issue_record,
    upsert_landing_page_record,
    upsert_patch_record,
    upsert_source_record,
)


ALLOWED_SOURCE_TYPES = {"patch_note", "known_issue", "faq"}
ALLOWED_STEP_LABELS = {"공식 안내", "공식 안내 기반 해석", "추론"}


@dataclass
class ImportBatchResult:
    imported_files: list[str]
    entity_counts: dict[str, int]
    db_counts: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    dry_run: bool = False


def _split_frontmatter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path.name}: frontmatter 시작 구분선(---)이 없습니다.")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        raise ValueError(f"{path.name}: frontmatter 종료 구분선(---)이 없습니다.")

    metadata = yaml.safe_load("\n".join(lines[1:end_index])) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"{path.name}: frontmatter는 key/value 객체여야 합니다.")

    raw_text = "\n".join(lines[end_index + 1 :]).strip()
    if not raw_text:
        raise ValueError(f"{path.name}: 원문 본문(raw source text)이 비어 있습니다.")
    return metadata, raw_text


def _normalize_datetime(value: Any, field_name: str, path: Path) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time()).isoformat()
    if isinstance(value, str):
        return value
    raise ValueError(f"{path.name}: {field_name} 값은 ISO datetime 문자열이어야 합니다.")


def _require_string(metadata: dict[str, Any], field_name: str, path: Path) -> str:
    value = metadata.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path.name}: `{field_name}` 필드는 비어 있지 않은 문자열이어야 합니다.")
    return value.strip()


def _string_list(value: Any, field_name: str, path: Path) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{path.name}: `{field_name}` 필드는 문자열 배열이어야 합니다.")
    return [item.strip() for item in value]


def _section_list(value: Any, field_name: str, path: Path) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{path.name}: `{field_name}` 필드는 배열이어야 합니다.")
    sections: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{path.name}: `{field_name}` 항목은 객체여야 합니다.")
        category = item.get("category")
        items = item.get("items")
        if not isinstance(category, str) or not category.strip():
            raise ValueError(f"{path.name}: `{field_name}.category`는 비어 있지 않은 문자열이어야 합니다.")
        sections.append({"category": category.strip(), "items": _string_list(items, f"{field_name}.items", path)})
    return sections


def _workaround_steps(value: Any, path: Path) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{path.name}: `workaround_steps`는 배열이어야 합니다.")

    steps: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{path.name}: `workaround_steps` 항목은 객체여야 합니다.")
        label = _require_string(item, "label", path)
        if label not in ALLOWED_STEP_LABELS:
            raise ValueError(f"{path.name}: workaround step label은 {sorted(ALLOWED_STEP_LABELS)} 중 하나여야 합니다.")
        step_order = item.get("step_order", index)
        if not isinstance(step_order, int):
            raise ValueError(f"{path.name}: `step_order`는 정수여야 합니다.")
        steps.append(
            {
                "step_order": step_order,
                "label": label,
                "step_text": _require_string(item, "step_text", path),
                "risk_level": _require_string(item, "risk_level", path),
            }
        )
    return steps


def _landing_payload(
    metadata: dict[str, Any],
    *,
    path: Path,
    route_key: str,
    default_slug: str,
    default_title: str,
    default_canonical_path: str,
    related_issue_slugs: list[str],
    related_patch_versions: list[str],
    updated_at: str,
) -> dict[str, Any] | None:
    landing = metadata.get("landing")
    if landing is None:
        return None
    if not isinstance(landing, dict):
        raise ValueError(f"{path.name}: `landing`은 객체여야 합니다.")

    faq_items = landing.get("faq_items", [])
    if not isinstance(faq_items, list):
        raise ValueError(f"{path.name}: `landing.faq_items`는 배열이어야 합니다.")

    sanitized_faq_items: list[dict[str, str]] = []
    for item in faq_items:
        if not isinstance(item, dict):
            raise ValueError(f"{path.name}: `landing.faq_items` 항목은 객체여야 합니다.")
        sanitized_faq_items.append(
            {
                "question": _require_string(item, "question", path),
                "answer": _require_string(item, "answer", path),
            }
        )

    title = landing.get("title", default_title)
    meta_description = landing.get("meta_description")
    body_markdown = landing.get("body_markdown", "")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{path.name}: `landing.title`은 비어 있지 않은 문자열이어야 합니다.")
    if not isinstance(meta_description, str) or not meta_description.strip():
        raise ValueError(f"{path.name}: `landing.meta_description`은 비어 있지 않은 문자열이어야 합니다.")
    if not isinstance(body_markdown, str) or not body_markdown.strip():
        raise ValueError(f"{path.name}: `landing.body_markdown`은 비어 있지 않은 문자열이어야 합니다.")

    return {
        "route_key": route_key,
        "slug": str(landing.get("slug", default_slug)),
        "locale": str(landing.get("locale", metadata.get("locale", "ko"))),
        "title": title.strip(),
        "meta_description": meta_description.strip(),
        "body_markdown": body_markdown.strip(),
        "canonical_path": str(landing.get("canonical_path", default_canonical_path)),
        "faq_items": sanitized_faq_items,
        "related_issue_slugs": related_issue_slugs,
        "related_patch_versions": related_patch_versions,
        "updated_at": updated_at,
    }


def parse_import_document(path: Path) -> dict[str, Any]:
    metadata, raw_text = _split_frontmatter(path.read_text(encoding="utf-8"), path)
    source_type = _require_string(metadata, "source_type", path)
    if source_type not in ALLOWED_SOURCE_TYPES:
        raise ValueError(f"{path.name}: `source_type`은 {sorted(ALLOWED_SOURCE_TYPES)} 중 하나여야 합니다.")

    published_at = _normalize_datetime(metadata.get("published_at"), "published_at", path)
    fetched_at = _normalize_datetime(metadata.get("fetched_at", published_at), "fetched_at", path)
    source_payload = {
        "source_type": source_type,
        "title": _require_string(metadata, "title", path),
        "source_url": _require_string(metadata, "source_url", path),
        "published_at": published_at,
        "fetched_at": fetched_at,
        "raw_text": raw_text,
        "preserve_source_record": bool(metadata.get("preserve_source_record", False)),
        "normalized_json": {
            "import_path": path.as_posix(),
            "import_type": source_type,
            "metadata": {key: value for key, value in metadata.items() if key != "landing"},
        },
    }

    if source_type == "patch_note":
        version = _require_string(metadata, "version", path)
        related_issue_slugs = _string_list(metadata.get("related_issue_slugs", []), "related_issue_slugs", path)
        patch_payload = {
            "version": version,
            "title": source_payload["title"],
            "published_at": published_at,
            "platforms": _string_list(metadata.get("platforms", []), "platforms", path),
            "summary": _require_string(metadata, "summary", path),
            "details": _section_list(metadata.get("details"), "details", path),
            "source_url": source_payload["source_url"],
            "related_issue_slugs": related_issue_slugs,
        }
        landing = _landing_payload(
            metadata,
            path=path,
            route_key=f"patch:{version}",
            default_slug=f"patches/{version.replace('.', '-')}",
            default_title=source_payload["title"],
            default_canonical_path=f"/ko/patches/{version}",
            related_issue_slugs=related_issue_slugs,
            related_patch_versions=[version],
            updated_at=fetched_at,
        )
        return {"kind": source_type, "source": source_payload, "patch": patch_payload, "landing": landing, "path": path}

    if source_type == "known_issue":
        slug = _require_string(metadata, "slug", path)
        related_patch_versions = _string_list(metadata.get("related_patch_versions", []), "related_patch_versions", path)
        issue_payload = {
            "slug": slug,
            "title": source_payload["title"],
            "symptom_summary": _require_string(metadata, "symptom_summary", path),
            "category": _require_string(metadata, "category", path),
            "status": _require_string(metadata, "status", path),
            "platforms": _string_list(metadata.get("platforms", []), "platforms", path),
            "first_seen_at": _normalize_datetime(metadata.get("first_seen_at", published_at), "first_seen_at", path),
            "last_seen_at": _normalize_datetime(metadata.get("last_seen_at", fetched_at), "last_seen_at", path),
            "escalation_needed": bool(metadata.get("escalation_needed", False)),
            "source_url": source_payload["source_url"],
            "workaround_steps": _workaround_steps(metadata.get("workaround_steps", []), path),
        }
        landing = _landing_payload(
            metadata,
            path=path,
            route_key=f"issue:{slug}",
            default_slug=f"issues/{slug}",
            default_title=source_payload["title"],
            default_canonical_path=f"/ko/issues/{slug}",
            related_issue_slugs=[slug],
            related_patch_versions=related_patch_versions,
            updated_at=issue_payload["last_seen_at"],
        )
        return {
            "kind": source_type,
            "source": source_payload,
            "issue": issue_payload,
            "related_patch_versions": related_patch_versions,
            "landing": landing,
            "path": path,
        }

    faq_payload = {
        "locale": str(metadata.get("locale", "ko")),
        "question": _require_string(metadata, "question", path),
        "answer": _require_string(metadata, "answer", path),
        "tags": _string_list(metadata.get("tags", []), "tags", path),
        "related_issue_slugs": _string_list(metadata.get("related_issue_slugs", []), "related_issue_slugs", path),
        "related_patch_versions": _string_list(metadata.get("related_patch_versions", []), "related_patch_versions", path),
        "source_url": source_payload["source_url"],
    }
    return {"kind": source_type, "source": source_payload, "faq": faq_payload, "path": path}


def discover_import_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.exists():
        raise FileNotFoundError(f"입력 경로를 찾을 수 없습니다: {target}")

    candidates = sorted(
        path
        for path in target.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
    )
    return [path for path in candidates if path.read_text(encoding="utf-8").lstrip().startswith("---")]


def import_documents(engine, files: list[Path], *, dry_run: bool = False) -> ImportBatchResult:
    documents = [parse_import_document(path) for path in files]
    entity_counts = {
        "patch_note": sum(1 for item in documents if item["kind"] == "patch_note"),
        "known_issue": sum(1 for item in documents if item["kind"] == "known_issue"),
        "faq": sum(1 for item in documents if item["kind"] == "faq"),
    }

    if dry_run:
        return ImportBatchResult(
            imported_files=[item["path"].name for item in documents],
            entity_counts=entity_counts,
            dry_run=True,
        )

    warnings: list[str] = []
    with Session(engine) as session:
        source_map: dict[str, Any] = {}

        for document in documents:
            source = upsert_source_record(session, document["source"])
            source_map[document["source"]["source_url"]] = source

        for document in documents:
            if document["kind"] == "patch_note":
                upsert_patch_record(session, document["patch"], source_map)
            elif document["kind"] == "known_issue":
                upsert_issue_record(session, document["issue"], source_map)
            else:
                upsert_faq_entry_record(session, document["faq"], source_map)

        session.flush()

        existing_issues = set(session.exec(select(Issue.slug)).all())
        existing_patches = set(session.exec(select(Patch.version)).all())

        for document in documents:
            if document["kind"] == "known_issue":
                issue = session.exec(select(Issue).where(Issue.slug == document["issue"]["slug"])).first()
                if issue is None:
                    continue
                replace_issue_workaround_steps(session, issue, document["issue"]["workaround_steps"])
                missing_patch_versions = [
                    version for version in document["related_patch_versions"] if version not in existing_patches
                ]
                if missing_patch_versions:
                    warnings.append(
                        f"{document['path'].name}: 연결할 patch version이 없어 링크를 건너뜀 - {', '.join(missing_patch_versions)}"
                    )
                replace_patch_links_for_issue(session, issue, document["related_patch_versions"])
                if document["landing"]:
                    upsert_landing_page_record(session, document["landing"])

            if document["kind"] == "patch_note":
                patch = session.exec(select(Patch).where(Patch.version == document["patch"]["version"])).first()
                if patch is None:
                    continue
                missing_issue_slugs = [
                    slug for slug in document["patch"]["related_issue_slugs"] if slug not in existing_issues
                ]
                if missing_issue_slugs:
                    warnings.append(
                        f"{document['path'].name}: 연결할 issue slug가 없어 링크를 건너뜀 - {', '.join(missing_issue_slugs)}"
                    )
                replace_patch_links_for_patch(session, patch, document["patch"]["related_issue_slugs"])
                if document["landing"]:
                    upsert_landing_page_record(session, document["landing"])

        session.commit()
        rebuild_search_index(session)
        db_counts = count_entities(session)

    return ImportBatchResult(
        imported_files=[item["path"].name for item in documents],
        entity_counts=entity_counts,
        db_counts=db_counts,
        warnings=warnings,
        dry_run=False,
    )
