from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column, JSON, UniqueConstraint
from sqlmodel import Field, SQLModel


class Source(SQLModel, table=True):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("source_url", "published_at", name="uq_source_url_published_at"),)

    id: int | None = Field(default=None, primary_key=True)
    source_type: str = Field(index=True)
    title: str
    source_url: str = Field(index=True)
    published_at: datetime = Field(index=True)
    fetched_at: datetime = Field(index=True)
    raw_text: str
    normalized_json: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class Patch(SQLModel, table=True):
    __tablename__ = "patches"

    id: int | None = Field(default=None, primary_key=True)
    version: str = Field(index=True, unique=True)
    title: str
    published_at: datetime = Field(index=True)
    platforms_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    summary: str
    details_json: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    source_id: int = Field(foreign_key="sources.id", index=True)


class Issue(SQLModel, table=True):
    __tablename__ = "issues"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    symptom_summary: str
    category: str = Field(index=True)
    status: str = Field(index=True)
    platforms_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    first_seen_at: datetime = Field(index=True)
    last_seen_at: datetime = Field(index=True)
    escalation_needed: bool = False
    source_id: int = Field(foreign_key="sources.id", index=True)


class PatchIssueLink(SQLModel, table=True):
    __tablename__ = "patch_issue_links"
    __table_args__ = (UniqueConstraint("patch_id", "issue_id", name="uq_patch_issue_link"),)

    id: int | None = Field(default=None, primary_key=True)
    patch_id: int = Field(foreign_key="patches.id", index=True)
    issue_id: int = Field(foreign_key="issues.id", index=True)


class FAQEntry(SQLModel, table=True):
    __tablename__ = "faq_entries"

    id: int | None = Field(default=None, primary_key=True)
    locale: str = Field(default="ko", index=True)
    question: str = Field(index=True, unique=True)
    answer: str
    tags_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    related_issue_slugs_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    related_patch_versions_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    source_id: int = Field(foreign_key="sources.id", index=True)


class WorkaroundStep(SQLModel, table=True):
    __tablename__ = "workaround_steps"

    id: int | None = Field(default=None, primary_key=True)
    issue_id: int = Field(foreign_key="issues.id", index=True)
    step_order: int = Field(index=True)
    label: str
    step_text: str
    risk_level: str


class LandingPage(SQLModel, table=True):
    __tablename__ = "landing_pages"

    id: int | None = Field(default=None, primary_key=True)
    route_key: str = Field(index=True, unique=True)
    slug: str
    locale: str = Field(default="ko", index=True)
    title: str
    meta_description: str
    body_markdown: str
    canonical_path: str
    faq_items_json: list[dict[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
    related_issue_slugs_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    related_patch_versions_json: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    updated_at: datetime = Field(index=True)

