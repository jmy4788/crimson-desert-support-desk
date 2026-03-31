from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.services.seed import seed_database


def test_health_returns_seeded_counts(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["counts"]["patches"] == 3
    assert payload["counts"]["issues"] == 8
    assert payload["counts"]["faq_entries"] == 10


def test_issue_filters_and_detail(client: TestClient) -> None:
    list_response = client.get("/api/issues", params={"platform": "Xbox PC App", "status": "investigating"})
    assert list_response.status_code == 200
    issue_payload = list_response.json()
    assert issue_payload["total"] == 1
    assert issue_payload["items"][0]["slug"] == "xbox-pc-launch-fail"

    detail_response = client.get("/api/issues/blurry-screen")
    assert detail_response.status_code == 200
    detail_payload = detail_response.json()
    assert detail_payload["landing_page"]["canonical_path"] == "/ko/issues/blurry-screen"
    assert detail_payload["workaround_steps"][0]["label"] in {"공식 안내", "공식 안내 기반 해석", "추론"}


def test_patch_detail_contains_diff_and_related_links(client: TestClient) -> None:
    response = client.get("/api/patches/1.01.02")

    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] == "1.01.02"
    assert payload["diff"]["initial_release"] is False
    assert len(payload["related_issues"]) >= 2


def test_search_returns_unified_results(client: TestClient) -> None:
    response = client.get("/api/search", params={"q": "Xbox"})

    assert response.status_code == 200
    payload = response.json()
    result_types = {item["type"] for item in payload["items"]}
    assert "issue" in result_types
    assert "faq" in result_types


def test_settings_doctor_labels_are_safe(client: TestClient) -> None:
    response = client.post(
        "/api/settings-doctor/query",
        json={
            "platform": "PC",
            "gpu_vendor": "NVIDIA",
            "upscaler_mode": "DLSS",
            "symptom": "DLSS 켜면 하늘이 깜빡여요",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["matched_issue_slug"] == "dlss-flicker"
    assert all(action["label"] in {"공식 안내", "공식 안내 기반 해석", "추론"} for action in payload["actions"])
    assert all("registry" not in action["step_text"].lower() for action in payload["actions"])


def test_seed_upsert_is_idempotent(client: TestClient) -> None:
    app = client.app
    counts = seed_database(app.state.engine, app.state.settings.seed_path)

    assert counts["patches"] == 3
    assert counts["issues"] == 8
    assert counts["faq_entries"] == 10


def test_admin_seed_disabled_in_prod(tmp_path: Path) -> None:
    database_path = tmp_path / "prod_support_desk.db"
    settings = Settings(
        app_env="prod",
        database_url=f"sqlite:///{database_path.as_posix()}",
        seed_path=Path(__file__).resolve().parents[2] / "data" / "seeds" / "sample_data.json",
        auto_seed_on_start=False,
    )
    app = create_app(settings)
    with TestClient(app) as prod_client:
        response = prod_client.post("/api/admin/seed")

    assert response.status_code == 403

