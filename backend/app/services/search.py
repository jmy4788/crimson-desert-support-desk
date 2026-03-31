from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from sqlalchemy import text
from sqlmodel import Session, select

from app.models import FAQEntry, Issue, Patch, Source, WorkaroundStep
from app.schemas import SearchResponse, SearchResultItem, SourceRef


def rebuild_search_index(session: Session) -> None:
    if session.bind is None or session.bind.dialect.name != "sqlite":
        return

    connection = session.connection()
    connection.execute(text("DELETE FROM search_index"))

    issues = session.exec(select(Issue).order_by(Issue.last_seen_at.desc())).all()
    patches = session.exec(select(Patch).order_by(Patch.published_at.desc())).all()
    faqs = session.exec(select(FAQEntry).order_by(FAQEntry.id)).all()
    steps = session.exec(select(WorkaroundStep).order_by(WorkaroundStep.issue_id, WorkaroundStep.step_order)).all()

    issue_step_map: dict[int, list[str]] = {}
    for step in steps:
        issue_step_map.setdefault(step.issue_id, []).append(step.step_text)

    for issue in issues:
        body = " ".join([issue.symptom_summary, issue.category, issue.status, *issue_step_map.get(issue.id or 0, [])])
        connection.execute(
            text(
                """
                INSERT INTO search_index (entity_type, entity_key, title, body, platforms, updated_at, locale)
                VALUES (:entity_type, :entity_key, :title, :body, :platforms, :updated_at, :locale)
                """
            ),
            {
                "entity_type": "issue",
                "entity_key": issue.slug,
                "title": issue.title,
                "body": body,
                "platforms": "||".join(issue.platforms_json),
                "updated_at": issue.last_seen_at.isoformat(),
                "locale": "ko",
            },
        )

    for patch in patches:
        section_text = " ".join(item for section in patch.details_json for item in section.get("items", []))
        connection.execute(
            text(
                """
                INSERT INTO search_index (entity_type, entity_key, title, body, platforms, updated_at, locale)
                VALUES (:entity_type, :entity_key, :title, :body, :platforms, :updated_at, :locale)
                """
            ),
            {
                "entity_type": "patch",
                "entity_key": patch.version,
                "title": patch.title,
                "body": f"{patch.summary} {section_text}".strip(),
                "platforms": "||".join(patch.platforms_json),
                "updated_at": patch.published_at.isoformat(),
                "locale": "ko",
            },
        )

    for faq in faqs:
        connection.execute(
            text(
                """
                INSERT INTO search_index (entity_type, entity_key, title, body, platforms, updated_at, locale)
                VALUES (:entity_type, :entity_key, :title, :body, :platforms, :updated_at, :locale)
                """
            ),
            {
                "entity_type": "faq",
                "entity_key": str(faq.id),
                "title": faq.question,
                "body": faq.answer,
                "platforms": "||".join(faq.tags_json),
                "updated_at": datetime.now().isoformat(),
                "locale": faq.locale,
            },
        )

    session.commit()


def query_search_index(session: Session, query: str, platform: str | None, limit: int) -> SearchResponse:
    cleaned_query = query.strip()
    if not cleaned_query:
        return SearchResponse(query=query, count=0, items=[])

    if session.bind is None or session.bind.dialect.name != "sqlite":
        return _query_search_index_fallback(session, cleaned_query, platform, limit)

    rows = session.execute(
        text(
            """
            SELECT
                entity_type,
                entity_key,
                title,
                snippet(search_index, 2, '', '', '…', 18) AS snippet,
                platforms,
                updated_at,
                bm25(search_index) AS rank
            FROM search_index
            WHERE search_index MATCH :query
            ORDER BY rank
            LIMIT :limit
            """
        ),
        {"query": cleaned_query, "limit": limit},
    ).mappings()

    items: list[SearchResultItem] = []
    platform_lower = platform.lower() if platform else None
    for row in rows:
        platforms = [value for value in str(row["platforms"]).split("||") if value]
        if platform_lower and not any(platform_lower in item.lower() for item in platforms):
            continue

        entity_type = str(row["entity_type"])
        entity_key = str(row["entity_key"])
        url = {
            "issue": f"/ko/issues/{entity_key}",
            "patch": f"/ko/patches/{entity_key}",
            "faq": f"/ko/faq?q={quote(str(row['title']))}",
        }.get(entity_type, "/ko")
        items.append(
            SearchResultItem(
                type=entity_type,
                title=str(row["title"]),
                slug_or_version=entity_key,
                snippet=str(row["snippet"] or row["title"]),
                platforms=platforms,
                updated_at=datetime.fromisoformat(str(row["updated_at"])),
                url=url,
            )
        )

    return SearchResponse(query=query, count=len(items), items=items)


def _query_search_index_fallback(session: Session, query: str, platform: str | None, limit: int) -> SearchResponse:
    tokens = [token.casefold() for token in query.split() if token.strip()]
    platform_lower = platform.casefold() if platform else None

    issues = session.exec(select(Issue).order_by(Issue.last_seen_at.desc())).all()
    patches = session.exec(select(Patch).order_by(Patch.published_at.desc())).all()
    faqs = session.exec(select(FAQEntry).order_by(FAQEntry.id.desc())).all()
    steps = session.exec(select(WorkaroundStep).order_by(WorkaroundStep.issue_id, WorkaroundStep.step_order)).all()

    issue_step_map: dict[int, list[str]] = {}
    for step in steps:
        issue_step_map.setdefault(step.issue_id, []).append(step.step_text)

    scored_items: list[tuple[int, SearchResultItem]] = []

    for issue in issues:
        platforms = issue.platforms_json
        if platform_lower and not any(platform_lower in item.casefold() for item in platforms):
            continue
        body = " ".join([issue.symptom_summary, issue.category, issue.status, *issue_step_map.get(issue.id or 0, [])]).strip()
        score = _search_score([issue.title, body], tokens)
        if score > 0:
            scored_items.append(
                (
                    score,
                    SearchResultItem(
                        type="issue",
                        title=issue.title,
                        slug_or_version=issue.slug,
                        snippet=_build_snippet(body or issue.title, tokens),
                        platforms=platforms,
                        updated_at=issue.last_seen_at,
                        url=f"/ko/issues/{issue.slug}",
                    ),
                )
            )

    for patch in patches:
        platforms = patch.platforms_json
        if platform_lower and not any(platform_lower in item.casefold() for item in platforms):
            continue
        section_text = " ".join(item for section in patch.details_json for item in section.get("items", []))
        body = f"{patch.summary} {section_text}".strip()
        score = _search_score([patch.title, body], tokens)
        if score > 0:
            scored_items.append(
                (
                    score,
                    SearchResultItem(
                        type="patch",
                        title=patch.title,
                        slug_or_version=patch.version,
                        snippet=_build_snippet(body or patch.title, tokens),
                        platforms=platforms,
                        updated_at=patch.published_at,
                        url=f"/ko/patches/{patch.version}",
                    ),
                )
            )

    for faq in faqs:
        body = faq.answer
        tags = faq.tags_json
        if platform_lower and not any(platform_lower in item.casefold() for item in tags):
            continue
        score = _search_score([faq.question, body, " ".join(tags)], tokens)
        if score > 0:
            scored_items.append(
                (
                    score,
                    SearchResultItem(
                        type="faq",
                        title=faq.question,
                        slug_or_version=str(faq.id),
                        snippet=_build_snippet(body or faq.question, tokens),
                        platforms=tags,
                        updated_at=datetime.now(),
                        url=f"/ko/faq?q={quote(faq.question)}",
                    ),
                )
            )

    sorted_items = [item for _, item in sorted(scored_items, key=lambda entry: (entry[0], entry[1].updated_at), reverse=True)]
    return SearchResponse(query=query, count=min(len(sorted_items), limit), items=sorted_items[:limit])


def _search_score(chunks: list[str], tokens: list[str]) -> int:
    haystack = " ".join(chunks).casefold()
    if not tokens:
        return 0
    return sum(haystack.count(token) for token in tokens)


def _build_snippet(text_value: str, tokens: list[str], *, max_length: int = 160) -> str:
    cleaned = " ".join(text_value.split())
    if not cleaned:
        return ""

    lowered = cleaned.casefold()
    first_index = min((lowered.find(token) for token in tokens if token in lowered), default=0)
    start = max(first_index - 40, 0)
    snippet = cleaned[start : start + max_length].strip()
    if start > 0:
        snippet = f"…{snippet}"
    if start + max_length < len(cleaned):
        snippet = f"{snippet}…"
    return snippet


def source_ref_from_source(source: Source) -> SourceRef:
    return SourceRef(
        title=source.title,
        source_type=source.source_type,
        source_url=source.source_url,
        published_at=source.published_at,
        fetched_at=source.fetched_at,
    )
