import { Link, useParams } from 'react-router-dom';

import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SectionCard } from '../components/SectionCard';
import { SourceRefList } from '../components/SourceRefList';
import { StatusBadge } from '../components/StatusBadge';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate } from '../lib/format';

export function PatchDetailPage() {
  const { version = '' } = useParams();
  const patchState = useApi(() => api.getPatch(version), [version]);
  const patch = patchState.data;

  usePageMeta(
    patch ? `${patch.version} 패치 상세` : '패치 상세',
    patch?.landing_page?.meta_description ?? '버전별 패치 상세와 diff를 확인합니다.',
    patch?.landing_page?.canonical_path,
  );

  if (patchState.loading) return <LoadingState />;
  if (patchState.error || !patch) {
    return (
      <SectionCard>
        <p className="text-sm text-rose-700">{patchState.error ?? '패치를 찾지 못했습니다.'}</p>
      </SectionCard>
    );
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-amber-700">{patch.version}</p>
        <h2 className="mt-3 text-3xl font-semibold text-zinc-950">{patch.title}</h2>
        <p className="mt-3 max-w-4xl text-sm text-zinc-600">{patch.summary}</p>
        <div className="mt-5 flex flex-wrap items-center gap-4">
          <PlatformChips platforms={patch.platforms} />
          <span className="text-sm text-zinc-500">게시 {formatDate(patch.published_at)}</span>
          <span className="text-sm text-zinc-500">최신 확인 {formatDate(patch.latest_checked_at)}</span>
        </div>
      </SectionCard>

      <div className="grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
        <div className="space-y-6">
          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">패치 요약</h3>
            <article className="mt-4 whitespace-pre-line text-sm leading-7 text-zinc-700">
              {patch.landing_page?.body_markdown ?? patch.summary}
            </article>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">세부 변경 항목</h3>
            <div className="mt-5 space-y-5">
              {patch.sections.map((section) => (
                <div key={section.category} className="rounded-[22px] border border-zinc-200 bg-zinc-50 px-5 py-4">
                  <div className="text-sm font-semibold uppercase tracking-[0.18em] text-zinc-500">{section.category}</div>
                  <ul className="mt-3 space-y-2 text-sm text-zinc-700">
                    {section.items.map((item) => (
                      <li key={item}>• {item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">이전 패치 대비 diff</h3>
            <div className="mt-5 grid gap-4 xl:grid-cols-3">
              <div className="rounded-[22px] border border-emerald-200 bg-emerald-50 p-5">
                <div className="text-sm font-semibold text-emerald-800">Added</div>
                <ul className="mt-3 space-y-2 text-sm text-emerald-900">
                  {patch.diff.added.map((item, index) => (
                    <li key={`${item.category}-${index}`}>• {item.current_text}</li>
                  ))}
                </ul>
              </div>
              <div className="rounded-[22px] border border-amber-200 bg-amber-50 p-5">
                <div className="text-sm font-semibold text-amber-800">Changed</div>
                <ul className="mt-3 space-y-2 text-sm text-amber-900">
                  {patch.diff.changed.map((item, index) => (
                    <li key={`${item.category}-${index}`}>
                      • {item.previous_text} → {item.current_text}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-[22px] border border-zinc-300 bg-zinc-100 p-5">
                <div className="text-sm font-semibold text-zinc-700">Removed</div>
                <ul className="mt-3 space-y-2 text-sm text-zinc-800">
                  {patch.diff.removed.map((item, index) => (
                    <li key={`${item.category}-${index}`}>• {item.previous_text}</li>
                  ))}
                </ul>
              </div>
            </div>
          </SectionCard>

          {patch.landing_page?.faq_items.length ? (
            <SectionCard>
              <h3 className="text-2xl font-semibold text-zinc-950">핵심 질문</h3>
              <div className="mt-5 space-y-4">
                {patch.landing_page.faq_items.map((item) => (
                  <div key={item.question} className="rounded-[24px] border border-zinc-200 bg-zinc-50 px-5 py-4">
                    <div className="text-sm font-semibold text-zinc-950">{item.question}</div>
                    <p className="mt-3 text-sm leading-7 text-zinc-700">{item.answer}</p>
                  </div>
                ))}
              </div>
            </SectionCard>
          ) : null}
        </div>

        <div className="space-y-6">
          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">관련 known issues</h3>
            <div className="mt-4 space-y-3">
              {patch.related_issues.map((issue) => (
                <Link
                  key={issue.slug}
                  to={`/ko/issues/${issue.slug}`}
                  className="block rounded-[22px] border border-zinc-200 bg-zinc-50 px-5 py-4 transition hover:border-amber-300"
                >
                  <div className="flex items-center gap-3">
                    <StatusBadge value={issue.status} />
                    <span className="text-xs text-zinc-500">{formatDate(issue.last_seen_at)}</span>
                  </div>
                  <div className="mt-3 text-base font-semibold text-zinc-950">{issue.title}</div>
                </Link>
              ))}
            </div>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">출처</h3>
            <div className="mt-4">
              <SourceRefList sources={patch.source_refs} />
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}
