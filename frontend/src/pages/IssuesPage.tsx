import { Link, useSearchParams } from 'react-router-dom';

import { EmptyState } from '../components/EmptyState';
import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SearchBar } from '../components/SearchBar';
import { SectionCard } from '../components/SectionCard';
import { StatusBadge } from '../components/StatusBadge';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate, humanizeCategory } from '../lib/format';

const PLATFORMS = ['all', 'PC', 'PS5', 'Xbox Series X|S', 'Xbox PC App'];
const STATUSES = ['all', 'investigating', 'workaround_available', 'monitoring', 'acknowledged', 'partially_improved'];
const CATEGORIES = ['all', 'visual', 'launch', 'compatibility', 'input', 'ux', 'save', 'performance'];

export function IssuesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const platform = searchParams.get('platform') ?? '';
  const status = searchParams.get('status') ?? '';
  const category = searchParams.get('category') ?? '';
  const query = searchParams.get('q') ?? '';
  const issuesState = useApi(
    () =>
      api.getIssues({
        platform,
        status,
        category,
        q: query,
        page_size: 24,
      }),
    [platform, status, category, query],
  );
  usePageMeta('Known Issues Hub', '증상, 플랫폼, 상태 기준으로 known issues를 필터링합니다.', '/ko/issues');

  function updateParams(next: Record<string, string>) {
    const params = new URLSearchParams();
    Object.entries(next).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    setSearchParams(params);
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-3xl font-semibold text-zinc-950">Known Issues Hub</h2>
            <p className="mt-2 text-sm text-zinc-600">증상 기반으로 이슈를 찾고, 현재 상태와 안전한 우회 조치를 확인합니다.</p>
          </div>
          <div className="rounded-full bg-zinc-950 px-4 py-2 text-sm font-semibold text-white">
            활성 이슈 {issuesState.data?.open_count ?? 0}건
          </div>
        </div>
        <div className="mt-5">
          <SearchBar initialValue={query} onSubmit={(value) => updateParams({ platform, status, category, q: value })} buttonLabel="증상 검색" />
        </div>
        <div className="mt-5 space-y-3">
          <div className="flex flex-wrap gap-2">
            {PLATFORMS.map((item) => {
              const value = item === 'all' ? '' : item;
              const active = value === platform;
              return (
                <button
                  key={item}
                  type="button"
                  onClick={() => updateParams({ platform: value, status, category, q: query })}
                  className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                    active ? 'bg-ink text-white' : 'border border-zinc-300 bg-white text-zinc-700'
                  }`}
                >
                  {item === 'all' ? '전체 플랫폼' : item}
                </button>
              );
            })}
          </div>
          <div className="flex flex-wrap gap-2">
            {STATUSES.map((item) => {
              const value = item === 'all' ? '' : item;
              const active = value === status;
              return (
                <button
                  key={item}
                  type="button"
                  onClick={() => updateParams({ platform, status: value, category, q: query })}
                  className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                    active ? 'bg-zinc-900 text-white' : 'border border-zinc-300 bg-white text-zinc-700'
                  }`}
                >
                  {item === 'all' ? '전체 상태' : item}
                </button>
              );
            })}
          </div>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((item) => {
              const value = item === 'all' ? '' : item;
              const active = value === category;
              return (
                <button
                  key={item}
                  type="button"
                  onClick={() => updateParams({ platform, status, category: value, q: query })}
                  className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                    active ? 'bg-amber-700 text-white' : 'border border-zinc-300 bg-white text-zinc-700'
                  }`}
                >
                  {item === 'all' ? '전체 카테고리' : humanizeCategory(item)}
                </button>
              );
            })}
          </div>
        </div>
      </SectionCard>

      {issuesState.loading ? <LoadingState /> : null}
      {issuesState.error ? (
        <SectionCard>
          <p className="text-sm text-rose-700">{issuesState.error}</p>
        </SectionCard>
      ) : null}
      {!issuesState.loading && !issuesState.error && (issuesState.data?.items.length ?? 0) === 0 ? (
        <EmptyState title="조건에 맞는 이슈 없음" description="검색어 또는 필터를 바꿔 보세요." />
      ) : null}

      <div className="grid gap-5">
        {issuesState.data?.items.map((issue) => (
          <Link
            key={issue.slug}
            to={`/ko/issues/${issue.slug}`}
            className="block rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-panel transition hover:border-amber-300"
          >
            <div className="flex flex-wrap items-center gap-3">
              <StatusBadge value={issue.status} />
              <span className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
                {humanizeCategory(issue.category)}
              </span>
              <span className="text-xs text-zinc-500">확인 {formatDate(issue.latest_checked_at)}</span>
            </div>
            <h3 className="mt-3 text-2xl font-semibold text-zinc-950">{issue.title}</h3>
            <p className="mt-2 text-sm text-zinc-600">{issue.symptom_summary}</p>
            <div className="mt-4 flex flex-wrap items-center gap-3">
              <PlatformChips platforms={issue.platforms} />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
