import { Link, useSearchParams } from 'react-router-dom';

import { EmptyState } from '../components/EmptyState';
import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SearchBar } from '../components/SearchBar';
import { SectionCard } from '../components/SectionCard';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate } from '../lib/format';

export function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') ?? '';
  const platform = searchParams.get('platform') ?? '';
  const searchState = useApi(
    () => api.search({ q: query, platform, limit: 20 }),
    [query, platform],
  );
  usePageMeta('통합 검색', '이슈, 패치, FAQ를 하나의 검색 결과로 보여줍니다.', '/ko/search');

  function updateQuery(value: string) {
    const next = new URLSearchParams();
    if (value) next.set('q', value);
    if (platform) next.set('platform', platform);
    setSearchParams(next);
  }

  function setPlatform(value: string) {
    const next = new URLSearchParams();
    if (query) next.set('q', query);
    if (value) next.set('platform', value);
    setSearchParams(next);
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <h2 className="text-3xl font-semibold text-zinc-950">통합 검색</h2>
        <p className="mt-2 text-sm text-zinc-600">패치, FAQ, known issues를 하나의 결과 목록으로 보여줍니다.</p>
        <div className="mt-5">
          <SearchBar initialValue={query} onSubmit={updateQuery} />
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {['', 'PC', 'PS5', 'Xbox Series X|S', 'Xbox PC App'].map((value) => (
            <button
              key={value || 'all'}
              type="button"
              onClick={() => setPlatform(value)}
              className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                platform === value ? 'bg-ink text-white' : 'border border-zinc-300 bg-white text-zinc-700'
              }`}
            >
              {value || '전체 플랫폼'}
            </button>
          ))}
        </div>
      </SectionCard>

      {!query ? <EmptyState title="검색어를 입력해 주세요" description="증상, 패치 버전, FAQ 키워드로 바로 찾을 수 있습니다." /> : null}
      {query && searchState.loading ? <LoadingState /> : null}
      {query && searchState.error ? (
        <SectionCard>
          <p className="text-sm text-rose-700">{searchState.error}</p>
        </SectionCard>
      ) : null}
      {query && !searchState.loading && !searchState.error && (searchState.data?.items.length ?? 0) === 0 ? (
        <EmptyState title="검색 결과 없음" description="다른 키워드나 플랫폼으로 다시 시도해 보세요." />
      ) : null}

      <div className="grid gap-5">
        {searchState.data?.items.map((item) => (
          <Link
            key={`${item.type}-${item.slug_or_version}`}
            to={item.url}
            className="block rounded-[28px] border border-zinc-200 bg-white/90 p-6 shadow-panel transition hover:border-amber-300"
          >
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-semibold uppercase text-zinc-600">
                {item.type}
              </span>
              <span className="text-xs text-zinc-500">업데이트 {formatDate(item.updated_at)}</span>
            </div>
            <h3 className="mt-3 text-xl font-semibold text-zinc-950">{item.title}</h3>
            <p className="mt-2 text-sm text-zinc-600">{item.snippet}</p>
            <div className="mt-4">
              <PlatformChips platforms={item.platforms} />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

