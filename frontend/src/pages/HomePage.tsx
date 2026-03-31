import { Link, useNavigate } from 'react-router-dom';

import { EmptyState } from '../components/EmptyState';
import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SearchBar } from '../components/SearchBar';
import { SectionCard } from '../components/SectionCard';
import { StatusBadge } from '../components/StatusBadge';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate } from '../lib/format';


export function HomePage() {
  const navigate = useNavigate();
  const patchesState = useApi(() => api.getPatches({ page_size: 1 }), []);
  const issuesState = useApi(() => api.getIssues({ page_size: 5 }), []);
  const faqState = useApi(() => api.getFaq({ page_size: 3 }), []);
  usePageMeta(
    '붉은사막 지원 허브',
    '최신 패치, 활성 known issues, 설정 진단을 한 화면에서 확인하는 비공식 지원 허브',
    '/ko',
  );

  if (patchesState.loading || issuesState.loading || faqState.loading) {
    return <LoadingState />;
  }

  if (patchesState.error || issuesState.error || faqState.error) {
    return (
      <SectionCard>
        <h2 className="text-xl font-semibold">데이터를 불러오지 못했습니다</h2>
        <p className="mt-3 text-sm text-zinc-600">
          {[patchesState.error, issuesState.error, faqState.error].filter(Boolean).join(' / ')}
        </p>
      </SectionCard>
    );
  }

  const latestPatch = patchesState.data?.items[0];
  const issues = issuesState.data?.items ?? [];
  const faqs = faqState.data?.items ?? [];

  return (
    <div className="space-y-6">
      <SectionCard className="overflow-hidden bg-[radial-gradient(circle_at_top_left,_rgba(180,83,9,0.18),_transparent_38%),linear-gradient(135deg,#fffaf2_0%,#ffffff_58%,#f0ebe1_100%)]">
        <div className="grid gap-6 lg:grid-cols-[1.7fr,1fr]">
          <div className="space-y-5">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-amber-700">Launch-Phase Command Deck</p>
              <h2 className="mt-3 max-w-3xl font-display text-4xl font-semibold tracking-tight text-zinc-950">
                “이거 고쳐졌나?”를 가장 빨리 판단할 수 있게 정리한 지원 허브
              </h2>
            </div>
            <SearchBar onSubmit={(value) => navigate(`/ko/search?q=${encodeURIComponent(value)}`)} />
            <div className="flex flex-wrap gap-2">
              {['PC', 'PS5', 'Xbox Series X|S', 'Xbox PC App'].map((platform) => (
                <button
                  key={platform}
                  type="button"
                  onClick={() => navigate(`/ko/issues?platform=${encodeURIComponent(platform)}`)}
                  className="rounded-full border border-zinc-300 bg-white/80 px-4 py-2 text-xs font-semibold text-zinc-800 transition hover:border-amber-400 hover:bg-amber-50"
                >
                  {platform}
                </button>
              ))}
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
            <div className="rounded-[24px] border border-zinc-200 bg-white/90 p-5">
              <div className="text-sm text-zinc-500">활성 known issues</div>
              <div className="mt-2 text-4xl font-semibold text-zinc-950">{issuesState.data?.open_count ?? 0}</div>
              <p className="mt-2 text-sm text-zinc-600">현재 unresolved 또는 monitoring 상태로 남아 있는 이슈 수</p>
            </div>
            {latestPatch ? (
              <div className="rounded-[24px] border border-zinc-200 bg-zinc-950 p-5 text-white">
                <div className="text-sm text-zinc-400">최신 패치</div>
                <div className="mt-2 text-2xl font-semibold">{latestPatch.version}</div>
                <p className="mt-2 text-sm text-zinc-300">{latestPatch.title}</p>
                <p className="mt-4 text-xs text-zinc-400">확인 {formatDate(latestPatch.latest_checked_at)}</p>
              </div>
            ) : null}
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
        <SectionCard>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-semibold text-zinc-950">최근 업데이트된 이슈</h3>
              <p className="mt-2 text-sm text-zinc-600">최신 확인 시각과 관련 패치 버전을 함께 확인하세요.</p>
            </div>
            <Link to="/ko/issues" className="text-sm font-semibold text-amber-700">
              전체 보기
            </Link>
          </div>
          <div className="mt-6 space-y-4">
            {issues.length > 0 ? (
              issues.map((issue) => (
                <Link
                  key={issue.slug}
                  to={`/ko/issues/${issue.slug}`}
                  className="block rounded-[24px] border border-zinc-200 bg-zinc-50 px-5 py-4 transition hover:border-amber-300 hover:bg-amber-50"
                >
                  <div className="flex flex-wrap items-center gap-3">
                    <StatusBadge value={issue.status} />
                    <span className="text-xs text-zinc-500">확인 {formatDate(issue.latest_checked_at)}</span>
                  </div>
                  <h4 className="mt-3 text-lg font-semibold text-zinc-950">{issue.title}</h4>
                  <p className="mt-2 text-sm text-zinc-600">{issue.symptom_summary}</p>
                  <div className="mt-4 flex flex-wrap items-center gap-3">
                    <PlatformChips platforms={issue.platforms} />
                  </div>
                </Link>
              ))
            ) : (
              <EmptyState title="이슈 데이터 없음" description="샘플 데이터 적재 이후 다시 확인해 주세요." />
            )}
          </div>
        </SectionCard>

        <div className="space-y-6">
          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">빠른 이동</h3>
            <div className="mt-5 grid gap-3">
              {[
                { to: '/ko/patches', title: 'Patch Hub', description: '버전별 diff와 영향 이슈 확인' },
                { to: '/ko/issues', title: 'Known Issues', description: '증상 기반 필터와 상태 보기' },
                { to: '/ko/faq', title: 'FAQ Hub', description: '공식 FAQ와 관련 이슈 연결' },
                { to: '/ko/settings-doctor', title: 'Settings Doctor', description: '플랫폼과 GPU 기준 조치 순서 안내' },
              ].map((item) => (
                <Link
                  key={item.to}
                  to={item.to}
                  className="rounded-[22px] border border-zinc-200 bg-white px-5 py-4 transition hover:border-amber-300 hover:bg-amber-50"
                >
                  <div className="font-semibold text-zinc-950">{item.title}</div>
                  <p className="mt-1 text-sm text-zinc-600">{item.description}</p>
                </Link>
              ))}
            </div>
          </SectionCard>

          <SectionCard>
            <div className="flex items-center justify-between">
              <h3 className="text-2xl font-semibold text-zinc-950">FAQ 하이라이트</h3>
              <Link to="/ko/faq" className="text-sm font-semibold text-amber-700">
                FAQ 허브
              </Link>
            </div>
            <div className="mt-5 space-y-3">
              {faqs.map((faq) => (
                <div key={faq.id} className="rounded-[22px] border border-zinc-200 bg-zinc-50 px-5 py-4">
                  <div className="text-sm font-semibold text-zinc-900">{faq.question}</div>
                  <p className="mt-2 text-sm text-zinc-600">{faq.answer}</p>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

