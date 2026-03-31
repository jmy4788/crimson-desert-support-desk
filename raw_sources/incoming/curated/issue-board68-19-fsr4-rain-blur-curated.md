---
source_type: known_issue
preserve_source_record: true
title: "FSR4 사용 시 비 오는 장면이 흐려지거나 왜곡되는 문제"
source_url: "https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=68"
published_at: "2026-03-19T22:20:00+00:00"
fetched_at: "2026-03-31T22:45:00+09:00"
slug: "fsr4-업스케일링-사용-시-비-오는-환경에서-빗줄기가-사라지고-화면이-흐려지거나-왜곡되는-현상이-확인됩니다"
symptom_summary: "FSR4 업스케일링 사용 시 비 오는 장면에서 빗줄기가 사라지거나 화면이 흐려지고 왜곡되는 문제가 공식 known issue에 올라와 있습니다."
category: "visual"
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
    step_text: "비 오는 같은 장면에서 FSR4를 끄거나 다른 업스케일러로 바꿔 증상이 사라지는지 먼저 비교하세요."
    risk_level: "low"
  - step_order: 2
    label: "공식 안내 기반 해석"
    step_text: "문제가 FSR4 사용 시에만 재현되는지 확인하려면 다른 그래픽 옵션은 최대한 그대로 둔 상태에서 업스케일러만 바꿔 보는 편이 좋습니다."
    risk_level: "low"
  - step_order: 3
    label: "공식 안내 기반 해석"
    step_text: "증상이 남으면 패치 버전과 재현된 날씨 장면을 함께 기록해 두고 공식 오류 제보 시 첨부하세요."
    risk_level: "low"
landing:
  title: "붉은사막 FSR4 비 오는 장면 흐림·왜곡 문제 정리"
  meta_description: "비 오는 장면에서 FSR4 사용 시 화면이 흐려지거나 왜곡될 때 공식 기준으로 확인할 항목을 정리했습니다."
  canonical_path: "/ko/issues/fsr4-업스케일링-사용-시-비-오는-환경에서-빗줄기가-사라지고-화면이-흐려지거나-왜곡되는-현상이-확인됩니다"
  body_markdown: |
    이 문제는 FSR4 업스케일링을 켠 상태에서 비 오는 장면의 빗줄기가 사라지거나, 화면이 흐려지고 왜곡되는 형태로 나타납니다.

    공식 known issue 문구가 원인을 FSR4 사용 조건과 직접 연결하고 있기 때문에, 가장 먼저 확인할 것은 같은 장면에서 업스케일러를 바꿨을 때 증상이 사라지는지 여부입니다. 다른 그래픽 옵션까지 한꺼번에 바꾸면 비교가 어려워집니다.

    현재는 모니터링 단계로 보는 것이 안전하며, 패치가 올라올 때마다 같은 장면에서 다시 확인하는 방식이 좋습니다.
  faq_items:
    - question: "비 오는 장면에서만 확인하면 되나요?"
      answer: "공식 문구가 비 오는 환경을 직접 언급하고 있으므로, 재현 확인도 같은 조건에서 하는 것이 가장 정확합니다."
    - question: "FSR4를 끄면 문제가 사라지면 바로 원인을 특정할 수 있나요?"
      answer: "최소한 현재 세팅 조합에서 FSR4 조건과 함께 재현된다는 점은 빠르게 확인할 수 있습니다."
---
수작업 큐레이션 override 문서입니다.
자동 수집된 공식 원문 source record는 preserve_source_record 설정으로 유지합니다.
