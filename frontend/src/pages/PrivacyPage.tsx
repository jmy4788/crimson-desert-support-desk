import { LegalPageShell } from '../components/LegalPageShell';
import { SectionCard } from '../components/SectionCard';
import { usePageMeta } from '../hooks/usePageMeta';

export function PrivacyPage() {
  usePageMeta(
    '개인정보 처리방침',
    '비공식 Crimson Desert 지원 허브의 개인정보 처리방침과 현재 수집 범위를 안내합니다.',
    '/ko/privacy',
  );

  return (
    <LegalPageShell
      eyebrow="Privacy"
      title="개인정보 처리방침"
      description="이 페이지는 비공식 Crimson Desert 지원 허브의 현재 개인정보 처리 범위를 설명합니다. 현재 서비스는 한국어 우선 공개를 준비하는 단계이며, 수집 범위가 바뀌면 이 문서를 함께 갱신합니다."
      updatedAt="2026-03-31"
    >
      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">현재 기본 원칙</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>현재 이 서비스는 회원가입, 결제, 사용자 계정 프로필 기능을 제공하지 않습니다.</p>
          <p>따라서 로컬 프로토타입 단계에서는 이름, 이메일, 결제정보 같은 계정성 개인정보를 별도로 저장하지 않습니다.</p>
          <p>공개 배포 단계에서는 운영 안정성을 위해 접속 로그, 기본 브라우저 정보, 오류 로그, 방문 통계가 수집될 수 있으며, 실제 수집이 시작되면 이 문서를 구체적으로 업데이트합니다.</p>
        </div>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">수집 가능 정보</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>공개 운영 시 수집될 수 있는 최소 정보는 아래 범위를 넘지 않도록 설계할 예정입니다.</p>
          <ul className="list-disc space-y-2 pl-5">
            <li>접속 시간</li>
            <li>요청한 페이지 주소</li>
            <li>브라우저 및 운영체제 정보</li>
            <li>기본적인 오류 추적 로그</li>
            <li>익명 또는 가명 처리된 방문 통계</li>
          </ul>
        </div>
      </SectionCard>

      <SectionCard>
        <h3 className="text-xl font-semibold text-zinc-950">하지 않는 것</h3>
        <div className="mt-4 space-y-3 text-sm leading-7 text-zinc-700">
          <p>이 서비스는 계정 비밀번호, 결제 수단 정보, 주민등록번호 등 민감한 개인정보를 요청하거나 저장하는 방향으로 운영하지 않을 예정입니다.</p>
          <p>공식 고객지원이 필요한 계정, 결제, 제재, 환불 문제는 이 사이트가 아닌 Pearl Abyss의 공식 채널에서 처리해야 합니다.</p>
        </div>
      </SectionCard>
    </LegalPageShell>
  );
}
