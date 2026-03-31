import { useSearchParams } from 'react-router-dom';

import { EmptyState } from '../components/EmptyState';
import { LoadingState } from '../components/LoadingState';
import { SearchBar } from '../components/SearchBar';
import { SectionCard } from '../components/SectionCard';
import { SourceRefList } from '../components/SourceRefList';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';

export function FaqPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') ?? '';
  const issueSlug = searchParams.get('issue_slug') ?? '';
  const patchVersion = searchParams.get('patch_version') ?? '';
  const faqState = useApi(
    () =>
      api.getFaq({
        q: query,
        issue_slug: issueSlug,
        patch_version: patchVersion,
        page_size: 24,
      }),
    [query, issueSlug, patchVersion],
  );

  usePageMeta('FAQ Hub', '공식 FAQ와 관련 이슈, 패치 연결을 한 번에 보여줍니다.', '/ko/faq');

  function updateQuery(value: string) {
    const params = new URLSearchParams(searchParams);
    if (value) {
      params.set('q', value);
    } else {
      params.delete('q');
    }
    setSearchParams(params);
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <h2 className="text-3xl font-semibold text-zinc-950">FAQ Hub</h2>
        <p className="mt-2 text-sm text-zinc-600">공식 FAQ를 기준으로 관련 이슈와 패치를 재배열했습니다.</p>
        <div className="mt-5">
          <SearchBar initialValue={query} onSubmit={updateQuery} buttonLabel="FAQ 검색" />
        </div>
      </SectionCard>

      {faqState.loading ? <LoadingState /> : null}
      {faqState.error ? (
        <SectionCard>
          <p className="text-sm text-rose-700">{faqState.error}</p>
        </SectionCard>
      ) : null}
      {!faqState.loading && !faqState.error && (faqState.data?.items.length ?? 0) === 0 ? (
        <EmptyState title="FAQ 결과 없음" description="검색어나 필터를 조정해 보세요." />
      ) : null}

      <div className="grid gap-5">
        {faqState.data?.items.map((faq) => (
          <SectionCard key={faq.id}>
            <div className="flex flex-wrap items-center gap-2">
              {faq.tags.map((tag) => (
                <span key={tag} className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-semibold text-zinc-600">
                  {tag}
                </span>
              ))}
            </div>
            <h3 className="mt-4 text-xl font-semibold text-zinc-950">{faq.question}</h3>
            <p className="mt-3 text-sm leading-7 text-zinc-700">{faq.answer}</p>
            <div className="mt-4 flex flex-wrap gap-2 text-xs text-zinc-500">
              {faq.related_issue_slugs.map((slug) => (
                <span key={slug} className="rounded-full border border-zinc-300 px-3 py-1">
                  issue:{slug}
                </span>
              ))}
              {faq.related_patch_versions.map((version) => (
                <span key={version} className="rounded-full border border-zinc-300 px-3 py-1">
                  patch:{version}
                </span>
              ))}
            </div>
            <div className="mt-5">
              <SourceRefList sources={faq.source_refs} />
            </div>
          </SectionCard>
        ))}
      </div>
    </div>
  );
}

