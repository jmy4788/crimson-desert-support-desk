---
source_type: known_issue
preserve_source_record: true
title: "DLSS·Ray Reconstruction 옵션을 자주 바꿀 때 프레임 드랍이 생기는 문제"
source_url: "https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=68"
published_at: "2026-03-19T22:20:00+00:00"
fetched_at: "2026-03-31T22:45:00+09:00"
slug: "특정-환경에서-nvidia-ray-reconstruction-및-dlss-옵션을-반복적으로-변경할-경우-프레"
symptom_summary: "NVIDIA Ray Reconstruction과 DLSS 옵션을 반복적으로 바꿀 때 프레임 드랍이 발생할 수 있으며, 공식 공지에서는 다음 패치 개선 예정 항목으로 안내했습니다."
category: "performance"
status: "monitoring"
platforms:
  - "PC"
first_seen_at: "2026-03-19T22:20:00+00:00"
last_seen_at: "2026-03-31T10:50:00+00:00"
escalation_needed: true
related_patch_versions: []
workaround_steps:
  - step_order: 1
    label: "공식 안내 기반 해석"
    step_text: "성능 비교가 필요하더라도 한 세션에서 DLSS와 Ray Reconstruction 조합을 여러 번 반복 변경하지 말고, 최종 조합을 정한 뒤 성능을 확인하세요."
    risk_level: "low"
  - step_order: 2
    label: "추론"
    step_text: "옵션을 여러 번 바꾼 뒤 프레임 드랍이 계속되면 게임을 다시 시작한 후 원하는 조합만 적용해 다시 비교하세요."
    risk_level: "low"
  - step_order: 3
    label: "공식 안내"
    step_text: "공식 공지에서 다음 패치를 통해 개선 예정이라고 안내한 항목이므로, 최신 패치 적용 여부를 계속 확인하세요."
    risk_level: "low"
landing:
  title: "붉은사막 DLSS·RR 반복 변경 프레임 드랍 가이드"
  meta_description: "DLSS와 Ray Reconstruction 옵션을 반복 변경할 때 프레임 드랍이 생기는 경우, 현재 공식 상태와 안전한 확인 순서를 정리했습니다."
  canonical_path: "/ko/issues/특정-환경에서-nvidia-ray-reconstruction-및-dlss-옵션을-반복적으로-변경할-경우-프레"
  body_markdown: |
    이 문제는 DLSS와 Ray Reconstruction 조합을 짧은 시간 안에 반복해서 바꿀 때 프레임이 내려가는 형태로 보고되고 있습니다.

    공식 공지에서는 이 항목을 known issue로 올렸고, 다음 패치를 통해 개선 예정이라고 안내했습니다. 따라서 현재 단계에서는 옵션을 계속 토글하며 비교하는 방식보다, 최종 조합을 정해 두고 성능을 확인하는 방식이 더 안전합니다.

    증상이 재현되면 어떤 조합에서 드랍이 생겼는지 기록해 두는 것이 좋습니다. 이후 패치가 올라오면 같은 장면에서 다시 비교하세요.
  faq_items:
    - question: "이 문제는 PC만 해당하나요?"
      answer: "공식 문구 자체가 NVIDIA Ray Reconstruction과 DLSS 조합을 지목하고 있으므로, 실제 확인 우선순위는 PC 환경입니다."
    - question: "옵션을 원래대로 돌려도 프레임이 회복되지 않으면 어떻게 하나요?"
      answer: "한 번 세션을 정리한 뒤 원하는 조합만 다시 적용해 비교하는 편이 안전합니다."
---
수작업 큐레이션 override 문서입니다.
자동 수집된 공식 원문 source record는 preserve_source_record 설정으로 유지합니다.
