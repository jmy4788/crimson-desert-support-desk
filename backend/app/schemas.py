from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SourceRef(BaseModel):
    title: str
    source_type: str
    source_url: str
    published_at: datetime
    fetched_at: datetime


class LandingFAQItem(BaseModel):
    question: str
    answer: str


class LandingMeta(BaseModel):
    route_key: str
    title: str
    meta_description: str
    body_markdown: str
    canonical_path: str
    faq_items: list[LandingFAQItem] = Field(default_factory=list)
    updated_at: datetime


class WorkaroundStepRead(BaseModel):
    step_order: int
    label: str
    step_text: str
    risk_level: str


class RelatedPatchSummary(BaseModel):
    version: str
    title: str
    published_at: datetime


class RelatedIssueSummary(BaseModel):
    slug: str
    title: str
    status: str
    category: str
    last_seen_at: datetime


class PatchSection(BaseModel):
    category: str
    items: list[str]


class PatchDiffEntry(BaseModel):
    category: str
    current_text: str | None = None
    previous_text: str | None = None


class PatchDiff(BaseModel):
    initial_release: bool = False
    added: list[PatchDiffEntry] = Field(default_factory=list)
    changed: list[PatchDiffEntry] = Field(default_factory=list)
    removed: list[PatchDiffEntry] = Field(default_factory=list)


class PatchSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version: str
    title: str
    published_at: datetime
    platforms: list[str]
    summary: str
    latest_checked_at: datetime
    related_issue_slugs: list[str] = Field(default_factory=list)


class PatchDetail(PatchSummary):
    source_refs: list[SourceRef] = Field(default_factory=list)
    sections: list[PatchSection] = Field(default_factory=list)
    diff: PatchDiff
    related_issues: list[RelatedIssueSummary] = Field(default_factory=list)
    landing_page: LandingMeta | None = None


class PatchListResponse(BaseModel):
    items: list[PatchSummary]
    total: int
    page: int
    page_size: int


class IssueSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    title: str
    symptom_summary: str
    category: str
    status: str
    platforms: list[str]
    last_seen_at: datetime
    latest_checked_at: datetime
    related_patch_versions: list[str] = Field(default_factory=list)


class IssueDetail(IssueSummary):
    source_refs: list[SourceRef] = Field(default_factory=list)
    workaround_steps: list[WorkaroundStepRead] = Field(default_factory=list)
    related_patches: list[RelatedPatchSummary] = Field(default_factory=list)
    landing_page: LandingMeta | None = None
    escalation_recommendation: str


class IssueListResponse(BaseModel):
    items: list[IssueSummary]
    total: int
    page: int
    page_size: int
    open_count: int


class FAQItem(BaseModel):
    id: int
    question: str
    answer: str
    tags: list[str]
    related_issue_slugs: list[str]
    related_patch_versions: list[str]
    latest_checked_at: datetime
    source_refs: list[SourceRef]


class FAQListResponse(BaseModel):
    items: list[FAQItem]
    total: int
    page: int
    page_size: int


class SearchResultItem(BaseModel):
    type: str
    title: str
    slug_or_version: str
    snippet: str
    platforms: list[str]
    updated_at: datetime
    url: str


class SearchResponse(BaseModel):
    query: str
    count: int
    items: list[SearchResultItem]


class DoctorQueryInput(BaseModel):
    platform: str
    gpu_vendor: str
    upscaler_mode: str
    symptom: str


class DoctorAction(BaseModel):
    order: int
    title: str
    step_text: str
    label: str
    risk_level: str
    source_refs: list[SourceRef] = Field(default_factory=list)


class DoctorQueryResponse(BaseModel):
    matched_issue_slug: str | None = None
    report_issue_recommended: bool
    actions: list[DoctorAction]


class SeedRequest(BaseModel):
    reset: bool = False


class SeedResponse(BaseModel):
    seeded_counts: dict[str, int]


class HealthResponse(BaseModel):
    status: str
    environment: str
    counts: dict[str, int]
