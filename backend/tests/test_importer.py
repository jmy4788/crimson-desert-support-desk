from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Source
from app.services.importer import import_documents


def test_importer_supports_dry_run(client: TestClient, tmp_path: Path) -> None:
    faq_file = tmp_path / "faq-version-check.md"
    faq_file.write_text(
        """---
source_type: faq
title: "FAQ: 설치된 버전은 어디에서 확인하나요?"
source_url: "https://www.crimsondesert.com/support/platform-faq-version-check"
published_at: "2026-03-31T09:30:00+09:00"
fetched_at: "2026-03-31T09:35:00+09:00"
question: "설치된 버전은 어디에서 확인하나요?"
answer: "타이틀 화면 우측 하단과 패치 허브를 함께 비교하세요."
tags:
  - "version"
related_issue_slugs:
  - "patch-version-confusion"
related_patch_versions:
  - "1.01.02"
---
공식 FAQ 원문
""",
        encoding="utf-8",
    )

    result = import_documents(client.app.state.engine, [faq_file], dry_run=True)

    assert result.dry_run is True
    assert result.entity_counts["faq"] == 1
    assert result.db_counts == {}


def test_importer_creates_new_patch_and_issue_with_links(client: TestClient, tmp_path: Path) -> None:
    patch_file = tmp_path / "patch-1-01-03.md"
    patch_file.write_text(
        """---
source_type: patch_note
title: "Crimson Desert Patch 1.01.03"
source_url: "https://www.crimsondesert.com/support/patch-notes-1-01-03"
published_at: "2026-03-31T10:00:00+09:00"
fetched_at: "2026-03-31T10:15:00+09:00"
version: "1.01.03"
platforms:
  - "PC"
summary: "런처 로고 이후 크래시 문제를 우선 완화하는 소규모 패치입니다."
related_issue_slugs:
  - "launcher-crash-after-logo"
details:
  - category: "Stability"
    items:
      - "로고 직후 크래시 재시도 루틴을 보강했습니다."
landing:
  title: "패치 1.01.03 요약"
  meta_description: "런처 로고 이후 크래시 관련 변경점 정리"
  canonical_path: "/ko/patches/1.01.03"
  body_markdown: |
    - 로고 이후 크래시 완화
    - 관련 known issue와 함께 확인
---
공식 패치 노트 원문
""",
        encoding="utf-8",
    )

    issue_file = tmp_path / "issue-launcher-crash.md"
    issue_file.write_text(
        """---
source_type: known_issue
title: "런처 로고 이후 크래시가 발생하는 문제"
source_url: "https://www.crimsondesert.com/support/known-issues-2026-03-31"
published_at: "2026-03-31T10:05:00+09:00"
fetched_at: "2026-03-31T10:15:00+09:00"
slug: "launcher-crash-after-logo"
symptom_summary: "런처 로고가 보인 직후 게임이 종료되는 사례가 있습니다."
category: "launch"
status: "investigating"
platforms:
  - "PC"
first_seen_at: "2026-03-31T10:05:00+09:00"
last_seen_at: "2026-03-31T10:15:00+09:00"
escalation_needed: true
related_patch_versions:
  - "1.01.03"
workaround_steps:
  - step_order: 1
    label: "공식 안내"
    step_text: "런처를 완전히 종료한 뒤 재시작합니다."
    risk_level: "low"
landing:
  title: "런처 로고 이후 크래시 대응"
  meta_description: "런처 로고 이후 종료되는 문제의 상태와 조치"
  canonical_path: "/ko/issues/launcher-crash-after-logo"
  body_markdown: |
    - 현재 조사 중
    - 관련 패치 1.01.03 확인
---
공식 known issue 원문
""",
        encoding="utf-8",
    )

    result = import_documents(client.app.state.engine, [patch_file, issue_file], dry_run=False)

    assert result.entity_counts["patch_note"] == 1
    assert result.entity_counts["known_issue"] == 1
    assert result.db_counts["patches"] == 4
    assert result.db_counts["issues"] == 9

    patch_response = client.get("/api/patches/1.01.03")
    assert patch_response.status_code == 200
    patch_payload = patch_response.json()
    assert any(item["slug"] == "launcher-crash-after-logo" for item in patch_payload["related_issues"])

    issue_response = client.get("/api/issues/launcher-crash-after-logo")
    assert issue_response.status_code == 200
    issue_payload = issue_response.json()
    assert any(item["version"] == "1.01.03" for item in issue_payload["related_patches"])
    assert issue_payload["landing_page"]["canonical_path"] == "/ko/issues/launcher-crash-after-logo"


def test_curated_override_can_preserve_existing_source_record(client: TestClient, tmp_path: Path) -> None:
    original_file = tmp_path / "faq-auto.md"
    original_file.write_text(
        """---
source_type: faq
title: "FAQ: 화면이 흐리게 보일 때"
source_url: "https://www.crimsondesert.com/support/platform-faq-visual"
published_at: "2026-03-31T09:30:00+09:00"
fetched_at: "2026-03-31T09:35:00+09:00"
question: "화면이 흐리게 보일 때는 어떻게 하나요?"
answer: "공식 FAQ 원문 답변"
tags:
  - "graphics"
---
공식 FAQ 원문 전체
""",
        encoding="utf-8",
    )

    curated_file = tmp_path / "faq-curated.md"
    curated_file.write_text(
        """---
source_type: faq
preserve_source_record: true
title: "FAQ: 화면이 흐리게 보일 때"
source_url: "https://www.crimsondesert.com/support/platform-faq-visual"
published_at: "2026-03-31T09:30:00+09:00"
fetched_at: "2026-03-31T10:05:00+09:00"
question: "화면이 흐리게 보일 때는 어떻게 하나요?"
answer: "수작업으로 정리한 답변"
tags:
  - "graphics"
  - "console"
---
큐레이션 메모
""",
        encoding="utf-8",
    )

    import_documents(client.app.state.engine, [original_file, curated_file], dry_run=False)

    with Session(client.app.state.engine) as session:
        source = session.exec(select(Source).where(Source.source_url == "https://www.crimsondesert.com/support/platform-faq-visual")).one()

    assert source.raw_text == "공식 FAQ 원문 전체"
    assert source.fetched_at.isoformat() == "2026-03-31T10:05:00"
