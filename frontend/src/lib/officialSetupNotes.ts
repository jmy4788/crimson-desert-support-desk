import type { SourceRef } from '../types/api';

export interface OfficialSetupNote {
  id: string;
  title: string;
  label: string;
  focus: string;
  platforms: string[];
  body: string;
  source_refs: SourceRef[];
}

const FAQ_SOURCE: SourceRef = {
  title: '자주 묻는 질문',
  source_type: 'faq',
  source_url: 'https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=63',
  published_at: '2026-03-12T15:30:00+00:00',
  fetched_at: '2026-03-31T12:20:00+09:00',
};

const KNOWN_ISSUES_SOURCE: SourceRef = {
  title: '알려진 문제점',
  source_type: 'known_issue',
  source_url: 'https://crimsondesert.pearlabyss.com/ko-KR/News/Notice/Detail?_boardNo=68',
  published_at: '2026-03-19T22:20:00+00:00',
  fetched_at: '2026-03-31T12:20:00+09:00',
};

export const officialSetupNotes: OfficialSetupNote[] = [
  {
    id: 'mfg-fps-floor',
    title: 'DLSS Multi Frame Generation은 충분한 기본 FPS에서만 켜는 편이 안전합니다',
    label: '공식 안내',
    focus: '입력 반응성 / 화면 안정성',
    platforms: ['PC', 'NVIDIA'],
    body: '공식 FAQ는 낮은 기본 렌더링 FPS 상태에서 MFG를 켜면 입력 반응성과 화면 안정성이 떨어질 수 있다고 안내합니다. 첫 점검은 MFG를 끈 상태에서 기본 프레임을 확보할 수 있는지부터 보는 것이 좋습니다.',
    source_refs: [FAQ_SOURCE],
  },
  {
    id: 'mfg-vsync',
    title: 'MFG 사용 시에는 V-Sync, G-Sync 계열 수직 동기화 옵션을 우선 끄고 비교하세요',
    label: '공식 안내',
    focus: '프레임 동기화',
    platforms: ['PC', 'NVIDIA'],
    body: '공식 FAQ는 MFG 사용 시 V-Sync, G-Sync 등 수직 동기화 관련 세팅을 끄는 것을 권장합니다. MFG와 동기화 옵션을 동시에 만지기보다, 먼저 동기화를 끄고 프레임 안정성을 확인한 뒤 다시 비교하는 순서가 낫습니다.',
    source_refs: [FAQ_SOURCE],
  },
  {
    id: 'upscaler-caution',
    title: '업스케일링 화면 이상이 보이면 품질 추구보다 안정성 확인부터 하세요',
    label: '공식 안내 기반 해석',
    focus: '업스케일링 / 비주얼 안정성',
    platforms: ['PC', 'PS5', 'Xbox Series X|S'],
    body: '공식 알려진 문제점 공지에는 특정 환경에서 업스케일링 사용 시 그림자, 머리카락, 기술 효과 노이즈, 화면 텍스처 거칠어짐이 발생할 수 있다고 적혀 있습니다. 이런 증상이 있으면 먼저 최신 패치를 적용하고, Native 또는 다른 업스케일러로 바꿔서 안정성부터 확인하는 쪽이 안전합니다.',
    source_refs: [KNOWN_ISSUES_SOURCE],
  },
  {
    id: 'hdmi-21',
    title: '콘솔과 고주사율 디스플레이 조합이면 HDMI 2.1 케이블 여부를 먼저 확인하세요',
    label: '공식 안내',
    focus: '출력 환경',
    platforms: ['PS5', 'Xbox Series X|S'],
    body: '공식 FAQ는 보다 원활한 화면 출력 환경을 위해 HDMI 2.1 지원 케이블 사용을 권장합니다. 콘솔 쪽 흐림이나 출력 이상을 전부 게임 내 설정 탓으로 보기 전에, 케이블과 디스플레이 체인을 먼저 점검하는 것이 맞습니다.',
    source_refs: [FAQ_SOURCE],
  },
];
