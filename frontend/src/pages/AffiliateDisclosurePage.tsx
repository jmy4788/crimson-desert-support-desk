import { LegalPageShell } from '../components/LegalPageShell';
import { SectionCard } from '../components/SectionCard';
import { usePageMeta } from '../hooks/usePageMeta';

export function AffiliateDisclosurePage() {
  usePageMeta(
    '제휴 링크 고지',
    '비공식 Crimson Desert 지원 허브의 제휴 링크 및 수익화 원칙을 안내합니다.',
    '/ko/affiliate-disclosure',
  );

  return (
    <LegalPageShell
      eyebrow="Affiliate Disclosure"
      title="제휴 링크 고지"
      description="이 페이지는 향후 제휴 링크와 수익화 요소를 도입할 때 적용할 원칙을 설명합니다. 공개 초기에는 수익화보다 신뢰도를 우선합니다."
      updatedAt="2026-03-31"
    >
      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">현재 상태</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>현재 이 사이트에는 활성화된 제휴 링크가 기본적으로 포함되어 있지 않습니다.</p>
          <p>향후 광고 또는 제휴 링크를 도입할 경우, 해당 요소는 본문과 명확히 구분되도록 표시할 예정입니다.</p>
        </div>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">도입 시 원칙</h3>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-sm leading-7 text-zinc-700">
          <li>제휴 링크는 관련성이 높은 페이지에만 제한적으로 배치합니다.</li>
          <li>문제 해결 단계보다 제휴 요소가 더 눈에 띄게 배치되지 않도록 합니다.</li>
          <li>성능, 주변기기, 저장장치처럼 실제 사용자 의사결정에 도움이 되는 범위에서만 검토합니다.</li>
          <li>추천 자체가 제휴 여부에 의해 왜곡되지 않도록 운영합니다.</li>
        </ul>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">공개 시 표시 방식</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>제휴 링크가 활성화되는 경우, 링크 주변 또는 해당 섹션 상단에 제휴 사실을 직접 표기합니다.</p>
          <p>사용자가 어떤 링크가 수익화와 연결되는지 한눈에 이해할 수 있게 만드는 것이 기본 원칙입니다.</p>
        </div>
      </SectionCard>
    </LegalPageShell>
  );
}
