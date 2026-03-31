from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from sqlalchemy import func
from sqlmodel import Session, select

from app.models import FAQEntry, Issue, LandingPage, Patch, PatchIssueLink, Source, WorkaroundStep
from app.schemas import (
    FAQItem,
    FAQListResponse,
    HealthResponse,
    IssueDetail,
    IssueListResponse,
    IssueSummary,
    LandingFAQItem,
    LandingMeta,
    PatchDetail,
    PatchListResponse,
    PatchSection,
    PatchSummary,
    RelatedIssueSummary,
    RelatedPatchSummary,
    WorkaroundStepRead,
)
from app.services.diff import build_patch_diff
from app.services.search import source_ref_from_source


def _paginate(items: list, page: int, page_size: int) -> list:
    start = max(page - 1, 0) * page_size
    return items[start : start + page_size]


def _load_sources(session: Session) -> dict[int, Source]:
    return {source.id: source for source in session.exec(select(Source)).all()}


def _load_patch_issue_maps(session: Session) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    patch_to_issues: dict[int, list[int]] = defaultdict(list)
    issue_to_patches: dict[int, list[int]] = defaultdict(list)
    for link in session.exec(select(PatchIssueLink)).all():
        patch_to_issues[link.patch_id].append(link.issue_id)
        issue_to_patches[link.issue_id].append(link.patch_id)
    return patch_to_issues, issue_to_patches


def _latest_checked(*dates: datetime) -> datetime:
    return max(dates)


def _landing_meta(session: Session, route_key: str) -> LandingMeta | None:
    landing = session.exec(select(LandingPage).where(LandingPage.route_key == route_key)).first()
    if landing is None:
        return None
    return LandingMeta(
        route_key=landing.route_key,
        title=landing.title,
        meta_description=landing.meta_description,
        body_markdown=landing.body_markdown,
        canonical_path=landing.canonical_path,
        faq_items=[LandingFAQItem(**item) for item in landing.faq_items_json],
        updated_at=landing.updated_at,
    )


def _issue_summary(issue: Issue, source: Source, related_patch_versions: list[str]) -> IssueSummary:
    return IssueSummary(
        slug=issue.slug,
        title=issue.title,
        symptom_summary=issue.symptom_summary,
        category=issue.category,
        status=issue.status,
        platforms=issue.platforms_json,
        last_seen_at=issue.last_seen_at,
        latest_checked_at=_latest_checked(issue.last_seen_at, source.fetched_at),
        related_patch_versions=related_patch_versions,
    )


def _patch_summary(patch: Patch, source: Source, related_issue_slugs: list[str]) -> PatchSummary:
    return PatchSummary(
        version=patch.version,
        title=patch.title,
        published_at=patch.published_at,
        platforms=patch.platforms_json,
        summary=patch.summary,
        latest_checked_at=_latest_checked(patch.published_at, source.fetched_at),
        related_issue_slugs=related_issue_slugs,
    )


def get_issue_list(
    session: Session,
    *,
    platform: str | None,
    status: str | None,
    category: str | None,
    q: str | None,
    page: int,
    page_size: int,
) -> IssueListResponse:
    issues = session.exec(select(Issue).order_by(Issue.last_seen_at.desc())).all()
    sources = _load_sources(session)
    _, issue_to_patches = _load_patch_issue_maps(session)
    patches = {patch.id: patch for patch in session.exec(select(Patch)).all()}

    def matches(issue: Issue) -> bool:
        if platform and not any(platform.lower() in value.lower() for value in issue.platforms_json):
            return False
        if status and issue.status.lower() != status.lower():
            return False
        if category and issue.category.lower() != category.lower():
            return False
        if q and q.lower() not in f"{issue.title} {issue.symptom_summary}".lower():
            return False
        return True

    filtered = [issue for issue in issues if matches(issue)]
    open_count = sum(1 for issue in issues if issue.status != "resolved")
    items = [
        _issue_summary(
            issue,
            sources[issue.source_id],
            [
                patches[patch_id].version
                for patch_id in issue_to_patches.get(issue.id or 0, [])
                if patch_id in patches
            ],
        )
        for issue in _paginate(filtered, page, page_size)
    ]
    return IssueListResponse(items=items, total=len(filtered), page=page, page_size=page_size, open_count=open_count)


def get_issue_detail(session: Session, slug: str) -> IssueDetail | None:
    issue = session.exec(select(Issue).where(Issue.slug == slug)).first()
    if issue is None:
        return None

    sources = _load_sources(session)
    _, issue_to_patches = _load_patch_issue_maps(session)
    patches = {patch.id: patch for patch in session.exec(select(Patch)).all()}
    related_patches = [
        patches[patch_id]
        for patch_id in issue_to_patches.get(issue.id or 0, [])
        if patch_id in patches
    ]
    related_patches.sort(key=lambda item: item.published_at, reverse=True)
    steps = session.exec(
        select(WorkaroundStep).where(WorkaroundStep.issue_id == issue.id).order_by(WorkaroundStep.step_order)
    ).all()
    source_refs = [source_ref_from_source(sources[issue.source_id])]
    for patch in related_patches:
        patch_source = sources.get(patch.source_id)
        if patch_source is not None:
            source_refs.append(source_ref_from_source(patch_source))

    deduped_source_refs = list({ref.source_url: ref for ref in source_refs}.values())
    issue_source = sources[issue.source_id]
    return IssueDetail(
        **_issue_summary(issue, issue_source, [patch.version for patch in related_patches]).model_dump(),
        source_refs=deduped_source_refs,
        workaround_steps=[
            WorkaroundStepRead(
                step_order=step.step_order,
                label=step.label,
                step_text=step.step_text,
                risk_level=step.risk_level,
            )
            for step in steps
        ],
        related_patches=[
            RelatedPatchSummary(version=patch.version, title=patch.title, published_at=patch.published_at)
            for patch in related_patches
        ],
        landing_page=_landing_meta(session, f"issue:{issue.slug}"),
        escalation_recommendation=(
            "기본 조치 후에도 동일 증상이 남으면 패치 버전, 플랫폼, 재현 장면을 함께 공식 지원 채널에 제출하세요."
            if issue.escalation_needed or issue.status != "resolved"
            else "현 시점에서는 추가 신고보다 최신 패치 적용 여부를 우선 확인하세요."
        ),
    )


def get_patch_list(
    session: Session,
    *,
    platform: str | None,
    q: str | None,
    page: int,
    page_size: int,
) -> PatchListResponse:
    patches = session.exec(select(Patch).order_by(Patch.published_at.desc())).all()
    sources = _load_sources(session)
    patch_to_issues, _ = _load_patch_issue_maps(session)
    issues = {issue.id: issue for issue in session.exec(select(Issue)).all()}

    def matches(patch: Patch) -> bool:
        if platform and not any(platform.lower() in value.lower() for value in patch.platforms_json):
            return False
        if q and q.lower() not in f"{patch.title} {patch.summary}".lower():
            return False
        return True

    filtered = [patch for patch in patches if matches(patch)]
    items = [
        _patch_summary(
            patch,
            sources[patch.source_id],
            [
                issues[issue_id].slug
                for issue_id in patch_to_issues.get(patch.id or 0, [])
                if issue_id in issues
            ],
        )
        for patch in _paginate(filtered, page, page_size)
    ]
    return PatchListResponse(items=items, total=len(filtered), page=page, page_size=page_size)


def get_patch_detail(session: Session, version: str) -> PatchDetail | None:
    patch = session.exec(select(Patch).where(Patch.version == version)).first()
    if patch is None:
        return None

    sources = _load_sources(session)
    patch_to_issues, _ = _load_patch_issue_maps(session)
    issues = {issue.id: issue for issue in session.exec(select(Issue)).all()}
    related_issues = [
        issues[issue_id]
        for issue_id in patch_to_issues.get(patch.id or 0, [])
        if issue_id in issues
    ]
    previous_patch = session.exec(
        select(Patch).where(Patch.published_at < patch.published_at).order_by(Patch.published_at.desc())
    ).first()

    source_refs = [source_ref_from_source(sources[patch.source_id])]
    for issue in related_issues:
        issue_source = sources.get(issue.source_id)
        if issue_source is not None:
            source_refs.append(source_ref_from_source(issue_source))

    deduped_source_refs = list({ref.source_url: ref for ref in source_refs}.values())
    patch_source = sources[patch.source_id]
    return PatchDetail(
        **_patch_summary(patch, patch_source, [issue.slug for issue in related_issues]).model_dump(),
        source_refs=deduped_source_refs,
        sections=[PatchSection(category=section["category"], items=section["items"]) for section in patch.details_json],
        diff=build_patch_diff(patch.details_json, previous_patch.details_json if previous_patch else None),
        related_issues=[
            RelatedIssueSummary(
                slug=issue.slug,
                title=issue.title,
                status=issue.status,
                category=issue.category,
                last_seen_at=issue.last_seen_at,
            )
            for issue in sorted(related_issues, key=lambda item: item.last_seen_at, reverse=True)
        ],
        landing_page=_landing_meta(session, f"patch:{patch.version}"),
    )


def get_faq_list(
    session: Session,
    *,
    q: str | None,
    issue_slug: str | None,
    patch_version: str | None,
    page: int,
    page_size: int,
) -> FAQListResponse:
    faqs = session.exec(select(FAQEntry).order_by(FAQEntry.id)).all()
    sources = _load_sources(session)

    def matches(faq: FAQEntry) -> bool:
        if issue_slug and issue_slug not in faq.related_issue_slugs_json:
            return False
        if patch_version and patch_version not in faq.related_patch_versions_json:
            return False
        if q and q.lower() not in f"{faq.question} {faq.answer}".lower():
            return False
        return True

    filtered = [faq for faq in faqs if matches(faq)]
    items = [
        FAQItem(
            id=faq.id or 0,
            question=faq.question,
            answer=faq.answer,
            tags=faq.tags_json,
            related_issue_slugs=faq.related_issue_slugs_json,
            related_patch_versions=faq.related_patch_versions_json,
            latest_checked_at=sources[faq.source_id].fetched_at,
            source_refs=[source_ref_from_source(sources[faq.source_id])],
        )
        for faq in _paginate(filtered, page, page_size)
    ]
    return FAQListResponse(items=items, total=len(filtered), page=page, page_size=page_size)


def get_health(session: Session, environment: str) -> HealthResponse:
    counts = {
        "sources": session.exec(select(func.count()).select_from(Source)).one(),
        "patches": session.exec(select(func.count()).select_from(Patch)).one(),
        "issues": session.exec(select(func.count()).select_from(Issue)).one(),
        "faq_entries": session.exec(select(func.count()).select_from(FAQEntry)).one(),
        "landing_pages": session.exec(select(func.count()).select_from(LandingPage)).one(),
    }
    return HealthResponse(status="ok", environment=environment, counts=counts)

