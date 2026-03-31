from __future__ import annotations

import re

from sqlmodel import Session, select

from app.models import Issue, Source
from app.schemas import DoctorAction, DoctorQueryInput, DoctorQueryResponse
from app.services.search import source_ref_from_source


RULES: dict[str, list[dict[str, str]]] = {
    "blurry-screen": [
        {
            "title": "해상도와 렌더 스케일 확인",
            "step_text": "게임 내 렌더 스케일이 100% 이하로 내려가 있지 않은지 먼저 확인하세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "업스케일러 일시 전환",
            "step_text": "DLSS/FSR/XeSS 사용 중이라면 한 번 Native 또는 다른 업스케일러로 전환해 변화가 있는지 확인하세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "후처리 옵션 최소화",
            "step_text": "모션 블러, 필름 그레인, 샤프닝 강도를 낮춘 뒤 동일 장면을 다시 확인하세요.",
            "label": "추론",
            "risk_level": "low",
        },
    ],
    "dlss-flicker": [
        {
            "title": "최신 패치 적용 여부 확인",
            "step_text": "패치 허브의 최신 버전으로 업데이트한 뒤 동일 구역에서 현상이 반복되는지 재현하세요.",
            "label": "공식 안내",
            "risk_level": "low",
        },
        {
            "title": "업스케일러 대체 테스트",
            "step_text": "DLSS 사용 중 깜빡임이 지속되면 TSR 또는 XeSS로 전환해 증상이 줄어드는지 확인하세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "광원 관련 옵션 낮추기",
            "step_text": "문제가 하늘 또는 구름 장면에서 두드러지면 레이 트레이싱 및 재구성 옵션을 한 단계 낮춘 뒤 비교하세요.",
            "label": "추론",
            "risk_level": "low",
        },
    ],
    "xbox-pc-launch-fail": [
        {
            "title": "Xbox PC 앱 업데이트 확인",
            "step_text": "Xbox PC 앱과 Gaming Services가 최신 상태인지 확인한 뒤 앱을 완전히 종료하고 다시 시작하세요.",
            "label": "공식 안내",
            "risk_level": "low",
        },
        {
            "title": "로그인 세션 재동기화",
            "step_text": "Microsoft Store와 Xbox PC 앱의 로그인 계정이 같은지 확인하고, 다르면 다시 로그인하세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "캐시 정리 후 재시도",
            "step_text": "앱 재시작 이후에도 동일하면 PC를 재부팅한 뒤 첫 실행만 다시 확인하세요.",
            "label": "추론",
            "risk_level": "low",
        },
    ],
    "intel-arc-support": [
        {
            "title": "공식 최소 사양 문구 확인",
            "step_text": "FAQ에 기재된 지원 GPU 목록과 현재 드라이버 버전을 먼저 대조하세요.",
            "label": "공식 안내",
            "risk_level": "low",
        },
        {
            "title": "보수적 그래픽 프리셋 사용",
            "step_text": "Arc GPU라면 첫 실행에서는 중간 프리셋과 TSR 기준으로 안정성을 먼저 점검하세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "추가 신고 준비",
            "step_text": "재현이 가능하면 드라이버 버전, 패치 버전, 증상 장면을 기록해 공식 문의 시 함께 제출하세요.",
            "label": "추론",
            "risk_level": "low",
        },
    ],
    "controller-instability": [
        {
            "title": "입력 장치 단순화",
            "step_text": "테스트 시에는 한 개의 패드만 연결하고 Steam Input 또는 플랫폼별 입력 래퍼를 중복 사용하지 마세요.",
            "label": "공식 안내 기반 해석",
            "risk_level": "low",
        },
        {
            "title": "게임 재시작 후 재인식",
            "step_text": "입력 장치 변경 후에는 게임을 완전히 종료했다가 다시 실행해 초기 인식 과정을 새로 시작하세요.",
            "label": "공식 안내",
            "risk_level": "low",
        },
        {
            "title": "유선 연결 우선 점검",
            "step_text": "불안정한 입력이 지속되면 유선 연결 상태에서 동일 증상이 나는지 먼저 확인하세요.",
            "label": "추론",
            "risk_level": "low",
        },
    ],
}


def _tokenize(value: str) -> set[str]:
    return {token for token in re.split(r"[^a-z0-9가-힣]+", value.lower()) if token}


def _match_issue(session: Session, symptom: str) -> Issue | None:
    symptom_tokens = _tokenize(symptom)
    if not symptom_tokens:
        return None

    best_issue: Issue | None = None
    best_score = 0
    issues = session.exec(select(Issue).order_by(Issue.last_seen_at.desc())).all()
    for issue in issues:
        issue_tokens = _tokenize(f"{issue.slug} {issue.title} {issue.symptom_summary}")
        score = len(symptom_tokens & issue_tokens)
        if score > best_score:
            best_score = score
            best_issue = issue
    return best_issue


def build_doctor_response(session: Session, payload: DoctorQueryInput) -> DoctorQueryResponse:
    issue = _match_issue(session, payload.symptom)
    issue_slug = issue.slug if issue else None
    source_refs = []
    if issue is not None:
        source = session.get(Source, issue.source_id)
        if source is not None:
            source_refs = [source_ref_from_source(source)]

    matched_rule_key = issue_slug or next(
        (rule_key for rule_key in RULES if rule_key.replace("-", " ") in payload.symptom.lower()),
        None,
    )
    rule_actions = RULES.get(matched_rule_key or "", [])
    if not rule_actions:
        rule_actions = [
            {
                "title": "공식 허브 최신 상태 확인",
                "step_text": "해당 증상에 직접 대응하는 공지가 있는지 Known Issues와 Patch Hub를 먼저 확인하세요.",
                "label": "공식 안내",
                "risk_level": "low",
            },
            {
                "title": "재현 조건 기록",
                "step_text": "플랫폼, GPU, 업스케일러, 패치 버전을 기록한 뒤 같은 조건에서 다시 재현해 보세요.",
                "label": "공식 안내 기반 해석",
                "risk_level": "low",
            },
            {
                "title": "문제 신고 준비",
                "step_text": "반복 재현이 가능하면 시스템 정보와 증상 영상을 함께 준비해 공식 지원 채널로 전달하세요.",
                "label": "추론",
                "risk_level": "low",
            },
        ]

    actions = [
        DoctorAction(
            order=index,
            title=action["title"],
            step_text=action["step_text"],
            label=action["label"],
            risk_level=action["risk_level"],
            source_refs=source_refs if action["label"] != "추론" else source_refs[:1],
        )
        for index, action in enumerate(rule_actions, start=1)
    ]

    return DoctorQueryResponse(
        matched_issue_slug=issue_slug,
        report_issue_recommended=issue is None or issue.status != "resolved",
        actions=actions,
    )
