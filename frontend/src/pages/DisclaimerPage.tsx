import { LegalPageShell } from '../components/LegalPageShell';
import { SectionCard } from '../components/SectionCard';
import { usePageMeta } from '../hooks/usePageMeta';

export function DisclaimerPage() {
  usePageMeta(
    '면책 및 운영 고지',
    '비공식 Crimson Desert 지원 허브의 운영 원칙과 면책 범위를 안내합니다.',
    '/ko/disclaimer',
  );

  return (
    <LegalPageShell
      eyebrow="Disclaimer"
      title="면책 및 운영 고지"
      description="이 서비스는 Pearl Abyss의 공식 고객지원 센터가 아닙니다. 공식 공지와 FAQ를 한국어 기준으로 재구성해 보여주는 비공식 팬 운영 지원 허브입니다."
      updatedAt="2026-03-31"
    >
      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">비공식 서비스임을 명확히 합니다</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>이 사이트는 공식 게임 운영사, 퍼블리셔, 고객지원 채널을 대체하지 않습니다.</p>
          <p>계정, 결제, 환불, 제재, 법적 분쟁, 소유권 문제처럼 공식 확인이 필요한 사안은 반드시 공식 지원 채널을 이용해야 합니다.</p>
        </div>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">우리가 지키려는 운영 원칙</h3>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-sm leading-7 text-zinc-700">
          <li>주요 해결 안내에는 공식 출처와 최신 확인 시각을 함께 표시합니다.</li>
          <li>해결 단계에는 신뢰 라벨을 붙입니다: 공식 안내, 공식 안내 기반 해석, 추론.</li>
          <li>위험한 레지스트리 수정, 출처 불명 커뮤니티 팁, 해결 보장 표현은 기본적으로 사용하지 않습니다.</li>
          <li>공식 공지와 충돌하는 경우 공식 안내를 우선합니다.</li>
        </ul>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">해결 보장은 하지 않습니다</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>이 사이트의 정리와 해석은 문제 해결을 돕기 위한 참고 정보입니다. 모든 환경에서 같은 결과를 보장하지 않습니다.</p>
          <p>특히 성능, 그래픽, 드라이버, 저장 데이터 관련 문제는 플랫폼과 설치 환경에 따라 달라질 수 있습니다.</p>
        </div>
      </SectionCard>
    </LegalPageShell>
  );
}
