---
source_type: known_issue
preserve_source_record: true
title: "업스케일링 사용 시 깜빡임·노이즈·거친 텍스처가 나타나는 문제"
source_url: "https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=68"
published_at: "2026-03-19T22:20:00+00:00"
fetched_at: "2026-03-31T22:45:00+09:00"
slug: "특정-환경에서-업스케일링-사용-시-그림자-효과-및-캐릭터-머리카락-깜빡임-일부-기술-효과의-노이즈-발생-화면"
symptom_summary: "특정 환경에서 업스케일링 사용 시 그림자, 머리카락, 기술 효과, 화면 텍스처가 깜빡이거나 거칠게 보일 수 있는 문제가 공식 known issue에 올라와 있습니다."
category: "visual"
status: "monitoring"
platforms:
  - "PC"
  - "PS5"
  - "Xbox Series X|S"
first_seen_at: "2026-03-19T22:20:00+00:00"
last_seen_at: "2026-03-31T10:50:00+00:00"
escalation_needed: true
related_patch_versions: []
workaround_steps:
  - step_order: 1
    label: "공식 안내 기반 해석"
    step_text: "증상이 보이는 같은 장면을 기준으로 업스케일링을 한 번 끄거나 다른 업스케일러·프리셋으로 바꿔 비교하세요."
    risk_level: "low"
  - step_order: 2
    label: "추론"
    step_text: "레이 재구성이나 유사한 후처리 옵션을 함께 쓰고 있다면 해당 조합을 잠시 끄고 같은 장면을 다시 확인하세요."
    risk_level: "low"
  - step_order: 3
    label: "공식 안내 기반 해석"
    step_text: "패치 버전, 사용 중인 업스케일러 이름, 증상이 발생한 장면을 기록해 두면 이후 공식 오류 제보 시 도움이 됩니다."
    risk_level: "low"
landing:
  title: "붉은사막 업스케일링 깜빡임·노이즈 문제 정리"
  meta_description: "업스케일링 사용 시 그림자, 머리카락, 효과 노이즈가 생길 때 현재 공식 상태와 안전한 확인 순서를 정리했습니다."
  canonical_path: "/ko/issues/특정-환경에서-업스케일링-사용-시-그림자-효과-및-캐릭터-머리카락-깜빡임-일부-기술-효과의-노이즈-발생-화면"
  body_markdown: |
    이 증상은 업스케일링이 켜진 상태에서 그림자, 머리카락, 기술 효과, 배경 텍스처가 불안정하게 보이는 형태로 나타날 수 있습니다.

    현재 공식 known issue에 올라와 있는 항목이며, 모든 사용자에게 고정적으로 발생하는 문제라기보다 특정 환경 조합에서 재현되는 문제로 정리되어 있습니다. 먼저 같은 장면에서 업스케일러 종류와 프리셋을 크게 바꾸지 말고 한 번씩만 비교해 보는 편이 안전합니다.

    이 페이지는 공식 공지의 핵심을 한국어 기준으로 다시 정리한 비공식 지원 허브입니다. 증상이 계속되면 패치 버전, 업스케일러 이름, 발생 장면을 함께 기록해 두세요.
  faq_items:
    - question: "어떤 항목부터 비교하면 좋나요?"
      answer: "같은 장면에서 업스케일링 On/Off 또는 업스케일러 종류를 한 번씩만 바꿔 보며 증상 차이를 확인하는 것이 가장 빠릅니다."
    - question: "공식 fix가 이미 배포된 상태인가요?"
      answer: "현재는 known issue로 공개된 상태이며, 이 페이지 기준으로는 여전히 모니터링 항목으로 보는 편이 안전합니다."
---
수작업 큐레이션 override 문서입니다.
자동 수집된 공식 원문 source record는 preserve_source_record 설정으로 유지합니다.
