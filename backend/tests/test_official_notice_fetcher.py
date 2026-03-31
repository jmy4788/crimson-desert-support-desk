from __future__ import annotations

from app.services.official_notice_fetcher import NoticeDetail, build_faq_documents, build_patch_document


def test_build_faq_documents_splits_multiple_questions() -> None:
    detail = NoticeDetail(
        board_no=63,
        locale="ko-KR",
        title="자주 묻는 질문",
        url="https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=63",
        source_type="faq",
        published_at="2026-03-12T15:30:00+00:00",
        fetched_at="2026-03-31T12:57:46+00:00",
        raw_text=(
            "플랫폼/시스템 관련\n"
            "붉은사막은 어떤 플랫폼에서 플레이할 수 있나요?\n"
            "Steam, PS5, Xbox에서 플레이할 수 있습니다.\n"
            "붉은사막은 Intel Arc 사용을 지원하나요?\n"
            "현재 호환성 및 최적화 대응 작업을 진행하고 있습니다.\n"
            "ms-windows-store://pdp/?productid=9MWPM2CQNLHN\n"
        ),
        list_items=[],
        meta_description="공식 FAQ 요약",
    )

    documents = build_faq_documents(detail)

    assert len(documents) == 2
    assert "어떤 플랫폼에서 플레이할 수 있나요?" in documents[0].content
    assert "Intel Arc 사용을 지원하나요?" in documents[1].content


def test_build_patch_document_adds_landing_payload() -> None:
    detail = NoticeDetail(
        board_no=79,
        locale="ko-KR",
        title="패치 노트 버전 1.01.03 (전 플랫폼 핫픽스)",
        url="https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=79",
        source_type="patch_note",
        published_at="2026-03-31T03:05:00+00:00",
        fetched_at="2026-03-31T13:00:00+00:00",
        raw_text="1.01.03 패치 사항을 안내해드립니다.\n특정 환경에서 화면 흐림이 일부 완화되었습니다.",
        list_items=["특정 환경에서 화면 흐림이 일부 완화되었습니다.", "Steam 핫픽스가 먼저 적용됩니다."],
        meta_description="1.01.03 패치 핵심 요약",
    )

    document = build_patch_document(detail)

    assert "landing:" in document.content
    assert "canonical_path: /ko/patches/1.01.03" in document.content
