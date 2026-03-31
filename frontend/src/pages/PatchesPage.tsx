import { useSearchParams, Link } from 'react-router-dom';

import { EmptyState } from '../components/EmptyState';
import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SearchBar } from '../components/SearchBar';
import { SectionCard } from '../components/SectionCard';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate } from '../lib/format';

const PLATFORMS = ['all', 'PC', 'PS5', 'Xbox Series X|S', 'Xbox PC App'];

export function PatchesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const platform = searchParams.get('platform') ?? '';
  const query = searchParams.get('q') ?? '';
  const patchesState = useApi(
    () =>
      api.getPatches({
        platform,
        q: query,
        page_size: 24,
      }),
    [platform, query],
  );

  usePageMeta('Patch Hub', '버전별 패치 요약과 이전 버전 대비 diff를 확인합니다.', '/ko/patches');

  function updateParams(nextPlatform: string, nextQuery: string) {
    const next = new URLSearchParams();
    if (nextPlatform) next.set('platform', nextPlatform);
    if (nextQuery) next.set('q', nextQuery);
    setSearchParams(next);
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <h2 className="text-3xl font-semibold text-zinc-950">Patch Hub</h2>
        <p className="mt-2 text-sm text-zinc-600">최신 패치, 변경 카테고리, 관련 이슈를 버전 단위로 연결합니다.</p>
        <div className="mt-5">
          <SearchBar initialValue={query} onSubmit={(value) => updateParams(platform, value)} buttonLabel="패치 검색" />
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {PLATFORMS.map((item) => {
            const active = (item === 'all' ? '' : item) === platform;
            return (
              <button
                key={item}
                type="button"
                onClick={() => updateParams(item === 'all' ? '' : item, query)}
                className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                  active ? 'bg-ink text-white' : 'border border-zinc-300 bg-white text-zinc-700 hover:border-amber-400'
                }`}
              >
                {item === 'all' ? '전체 플랫폼' : item}
              </button>
            );
          })}
        </div>
      </SectionCard>

      {patchesState.loading ? <LoadingState /> : null}
      {patchesState.error ? (
        <SectionCard>
          <p className="text-sm text-rose-700">{patchesState.error}</p>
        </SectionCard>
      ) : null}
      {!patchesState.loading && !patchesState.error && (patchesState.data?.items.length ?? 0) === 0 ? (
        <EmptyState title="패치가 없습니다" description="필터를 바꾸거나 샘플 데이터를 다시 적재해 주세요." />
      ) : null}

      <div className="grid gap-5">
        {patchesState.data?.items.map((patch) => (
          <Link
            key={patch.version}
            to={`/ko/patches/${patch.version}`}
            className="block rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-panel transition hover:border-amber-300"
          >
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-amber-700">{patch.version}</p>
                <h3 className="mt-2 text-2xl font-semibold text-zinc-950">{patch.title}</h3>
              </div>
              <div className="text-sm text-zinc-500">확인 {formatDate(patch.latest_checked_at)}</div>
            </div>
            <p className="mt-3 max-w-3xl text-sm text-zinc-600">{patch.summary}</p>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <PlatformChips platforms={patch.platforms} />
              <span className="text-xs text-zinc-500">관련 이슈 {patch.related_issue_slugs.length}건</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

