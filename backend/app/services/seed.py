from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import func
from sqlmodel import Session, delete, select

from app.database import reset_database
from app.models import FAQEntry, Issue, LandingPage, Patch, PatchIssueLink, Source, WorkaroundStep
from app.services.search import rebuild_search_index


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _match_datetime_shape(value: datetime, reference: datetime) -> datetime:
    if reference.tzinfo is None and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    if reference.tzinfo is not None and value.tzinfo is None:
        return value.replace(tzinfo=reference.tzinfo)
    return value


def database_is_empty(engine) -> bool:
    with Session(engine) as session:
        count = session.exec(select(func.count()).select_from(Source)).one()
    return count == 0


def read_seed_payload(seed_path: Path) -> dict[str, Any]:
    return json.loads(seed_path.read_text(encoding="utf-8"))


def _upsert_source(session: Session, payload: dict[str, Any]) -> Source:
    published_at = parse_datetime(payload["published_at"])
    preserve_source_record = bool(payload.get("preserve_source_record", False))
    source = session.exec(
        select(Source).where(
            Source.source_url == payload["source_url"],
            Source.published_at == published_at,
        )
    ).first()
    if source is None:
        source = Source(
            source_type=payload["source_type"],
            title=payload["title"],
            source_url=payload["source_url"],
            published_at=published_at,
            fetched_at=parse_datetime(payload["fetched_at"]),
            raw_text=payload["raw_text"],
            normalized_json=payload.get("normalized_json", {}),
        )
        session.add(source)
    else:
        next_fetched_at = parse_datetime(payload["fetched_at"])
        next_fetched_at = _match_datetime_shape(next_fetched_at, source.fetched_at)
        source.fetched_at = max(source.fetched_at, next_fetched_at)
        if not preserve_source_record:
            source.source_type = payload["source_type"]
            source.title = payload["title"]
            source.raw_text = payload["raw_text"]
            source.normalized_json = payload.get("normalized_json", {})
    session.flush()
    return source


def _upsert_patch(session: Session, payload: dict[str, Any], source_map: dict[str, Source]) -> Patch:
    patch = session.exec(select(Patch).where(Patch.version == payload["version"])).first()
    source = source_map[payload["source_url"]]
    if patch is None:
        patch = Patch(
            version=payload["version"],
            title=payload["title"],
            published_at=parse_datetime(payload["published_at"]),
            platforms_json=payload["platforms"],
            summary=payload["summary"],
            details_json=payload["details"],
            source_id=source.id,
        )
        session.add(patch)
    else:
        patch.title = payload["title"]
        patch.published_at = parse_datetime(payload["published_at"])
        patch.platforms_json = payload["platforms"]
        patch.summary = payload["summary"]
        patch.details_json = payload["details"]
        patch.source_id = source.id
    session.flush()
    return patch


def _upsert_issue(session: Session, payload: dict[str, Any], source_map: dict[str, Source]) -> Issue:
    issue = session.exec(select(Issue).where(Issue.slug == payload["slug"])).first()
    source = source_map[payload["source_url"]]
    if issue is None:
        issue = Issue(
            slug=payload["slug"],
            title=payload["title"],
            symptom_summary=payload["symptom_summary"],
            category=payload["category"],
            status=payload["status"],
            platforms_json=payload["platforms"],
            first_seen_at=parse_datetime(payload["first_seen_at"]),
            last_seen_at=parse_datetime(payload["last_seen_at"]),
            escalation_needed=payload["escalation_needed"],
            source_id=source.id,
        )
        session.add(issue)
    else:
        issue.title = payload["title"]
        issue.symptom_summary = payload["symptom_summary"]
        issue.category = payload["category"]
        issue.status = payload["status"]
        issue.platforms_json = payload["platforms"]
        issue.first_seen_at = parse_datetime(payload["first_seen_at"])
        issue.last_seen_at = parse_datetime(payload["last_seen_at"])
        issue.escalation_needed = payload["escalation_needed"]
        issue.source_id = source.id
    session.flush()
    return issue


def upsert_source_record(session: Session, payload: dict[str, Any]) -> Source:
    return _upsert_source(session, payload)


def upsert_patch_record(session: Session, payload: dict[str, Any], source_map: dict[str, Source]) -> Patch:
    return _upsert_patch(session, payload, source_map)


def upsert_issue_record(session: Session, payload: dict[str, Any], source_map: dict[str, Source]) -> Issue:
    return _upsert_issue(session, payload, source_map)


def replace_issue_workaround_steps(session: Session, issue: Issue, steps: list[dict[str, Any]]) -> None:
    session.exec(delete(WorkaroundStep).where(WorkaroundStep.issue_id == issue.id))
    for step_payload in steps:
        session.add(
            WorkaroundStep(
                issue_id=issue.id,
                step_order=step_payload["step_order"],
                label=step_payload["label"],
                step_text=step_payload["step_text"],
                risk_level=step_payload["risk_level"],
            )
        )
    session.flush()


def replace_patch_links_for_patch(session: Session, patch: Patch, issue_slugs: list[str]) -> None:
    session.exec(delete(PatchIssueLink).where(PatchIssueLink.patch_id == patch.id))
    for issue_slug in issue_slugs:
        issue = session.exec(select(Issue).where(Issue.slug == issue_slug)).first()
        if issue is not None:
            session.add(PatchIssueLink(patch_id=patch.id, issue_id=issue.id))
    session.flush()


def replace_patch_links_for_issue(session: Session, issue: Issue, patch_versions: list[str]) -> None:
    session.exec(delete(PatchIssueLink).where(PatchIssueLink.issue_id == issue.id))
    for version in patch_versions:
        patch = session.exec(select(Patch).where(Patch.version == version)).first()
        if patch is not None:
            session.add(PatchIssueLink(patch_id=patch.id, issue_id=issue.id))
    session.flush()


def upsert_faq_entry_record(session: Session, payload: dict[str, Any], source_map: dict[str, Source]) -> FAQEntry:
    faq = session.exec(select(FAQEntry).where(FAQEntry.question == payload["question"])).first()
    source = source_map[payload["source_url"]]
    if faq is None:
        faq = FAQEntry(
            locale=payload.get("locale", "ko"),
            question=payload["question"],
            answer=payload["answer"],
            tags_json=payload.get("tags", []),
            related_issue_slugs_json=payload.get("related_issue_slugs", []),
            related_patch_versions_json=payload.get("related_patch_versions", []),
            source_id=source.id,
        )
        session.add(faq)
    else:
        faq.locale = payload.get("locale", "ko")
        faq.answer = payload["answer"]
        faq.tags_json = payload.get("tags", [])
        faq.related_issue_slugs_json = payload.get("related_issue_slugs", [])
        faq.related_patch_versions_json = payload.get("related_patch_versions", [])
        faq.source_id = source.id
    session.flush()
    return faq


def upsert_landing_page_record(session: Session, payload: dict[str, Any]) -> LandingPage:
    landing_page = session.exec(select(LandingPage).where(LandingPage.route_key == payload["route_key"])).first()
    if landing_page is None:
        landing_page = LandingPage(
            route_key=payload["route_key"],
            slug=payload["slug"],
            locale=payload.get("locale", "ko"),
            title=payload["title"],
            meta_description=payload["meta_description"],
            body_markdown=payload["body_markdown"],
            canonical_path=payload["canonical_path"],
            faq_items_json=payload.get("faq_items", []),
            related_issue_slugs_json=payload.get("related_issue_slugs", []),
            related_patch_versions_json=payload.get("related_patch_versions", []),
            updated_at=parse_datetime(payload["updated_at"]),
        )
        session.add(landing_page)
    else:
        landing_page.slug = payload["slug"]
        landing_page.locale = payload.get("locale", "ko")
        landing_page.title = payload["title"]
        landing_page.meta_description = payload["meta_description"]
        landing_page.body_markdown = payload["body_markdown"]
        landing_page.canonical_path = payload["canonical_path"]
        landing_page.faq_items_json = payload.get("faq_items", [])
        landing_page.related_issue_slugs_json = payload.get("related_issue_slugs", [])
        landing_page.related_patch_versions_json = payload.get("related_patch_versions", [])
        landing_page.updated_at = parse_datetime(payload["updated_at"])
    session.flush()
    return landing_page


def count_entities(session: Session) -> dict[str, int]:
    return {
        "sources": session.exec(select(func.count()).select_from(Source)).one(),
        "patches": session.exec(select(func.count()).select_from(Patch)).one(),
        "issues": session.exec(select(func.count()).select_from(Issue)).one(),
        "faq_entries": session.exec(select(func.count()).select_from(FAQEntry)).one(),
        "workaround_steps": session.exec(select(func.count()).select_from(WorkaroundStep)).one(),
        "landing_pages": session.exec(select(func.count()).select_from(LandingPage)).one(),
    }


def seed_database(engine, seed_path: Path, *, reset: bool = False) -> dict[str, int]:
    if reset:
        reset_database(engine)

    payload = read_seed_payload(seed_path)
    with Session(engine) as session:
        source_map = {
            source_payload["source_url"]: upsert_source_record(session, source_payload)
            for source_payload in payload.get("sources", [])
        }

        patch_map = {
            patch_payload["version"]: upsert_patch_record(session, patch_payload, source_map)
            for patch_payload in payload.get("patches", [])
        }
        issue_map = {
            issue_payload["slug"]: upsert_issue_record(session, issue_payload, source_map)
            for issue_payload in payload.get("issues", [])
        }

        session.exec(delete(WorkaroundStep))
        session.exec(delete(PatchIssueLink))
        session.exec(delete(FAQEntry))
        session.exec(delete(LandingPage))
        session.flush()

        for issue_payload in payload.get("issues", []):
            issue = issue_map[issue_payload["slug"]]
            replace_issue_workaround_steps(session, issue, issue_payload.get("workaround_steps", []))

        for patch_payload in payload.get("patches", []):
            patch = patch_map[patch_payload["version"]]
            replace_patch_links_for_patch(session, patch, patch_payload.get("related_issue_slugs", []))

        for faq_payload in payload.get("faq_entries", []):
            upsert_faq_entry_record(session, faq_payload, source_map)

        for landing_payload in payload.get("landing_pages", []):
            upsert_landing_page_record(session, landing_payload)

        session.commit()
        rebuild_search_index(session)
        return count_entities(session)
