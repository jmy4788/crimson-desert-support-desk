import { Link, useParams } from 'react-router-dom';

import { LoadingState } from '../components/LoadingState';
import { PlatformChips } from '../components/PlatformChips';
import { SectionCard } from '../components/SectionCard';
import { SourceRefList } from '../components/SourceRefList';
import { StatusBadge } from '../components/StatusBadge';
import { useApi } from '../hooks/useApi';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { formatDate, humanizeCategory } from '../lib/format';

export function IssueDetailPage() {
  const { slug = '' } = useParams();
  const issueState = useApi(() => api.getIssue(slug), [slug]);
  const issue = issueState.data;

  usePageMeta(
    issue ? issue.title : 'Known Issue',
    issue?.landing_page?.meta_description ?? '붉은사막 known issue 상세',
    issue?.landing_page?.canonical_path,
  );

  if (issueState.loading) return <LoadingState />;
  if (issueState.error || !issue) {
    return (
      <SectionCard>
        <p className="text-sm text-rose-700">{issueState.error ?? '이슈를 찾지 못했습니다.'}</p>
      </SectionCard>
    );
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <div className="flex flex-wrap items-center gap-3">
          <StatusBadge value={issue.status} />
          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
            {humanizeCategory(issue.category)}
          </span>
          <span className="text-xs text-zinc-500">최신 확인 {formatDate(issue.latest_checked_at)}</span>
        </div>
        <h2 className="mt-3 text-3xl font-semibold text-zinc-950">{issue.title}</h2>
        <p className="mt-3 max-w-4xl text-sm text-zinc-600">{issue.symptom_summary}</p>
        <div className="mt-5 flex flex-wrap items-center gap-4">
          <PlatformChips platforms={issue.platforms} />
          <span className="text-sm text-zinc-500">최근 업데이트 {formatDate(issue.last_seen_at)}</span>
        </div>
      </SectionCard>

      <div className="grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
        <div className="space-y-6">
          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">증상 개요</h3>
            <article className="mt-4 whitespace-pre-line text-sm leading-7 text-zinc-700">
              {issue.landing_page?.body_markdown ?? issue.symptom_summary}
            </article>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">권장 조치 순서</h3>
            <div className="mt-5 space-y-4">
              {issue.workaround_steps.map((step) => (
                <div key={step.step_order} className="rounded-[24px] border border-zinc-200 bg-zinc-50 px-5 py-4">
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-zinc-900 text-sm font-semibold text-white">
                      {step.step_order}
                    </span>
                    <StatusBadge value={step.label} kind="evidence" />
                    <span className="text-xs uppercase tracking-[0.18em] text-zinc-500">Risk {step.risk_level}</span>
                  </div>
                  <p className="mt-3 text-sm leading-7 text-zinc-700">{step.step_text}</p>
                </div>
              ))}
            </div>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">에스컬레이션 기준</h3>
            <p className="mt-4 text-sm leading-7 text-zinc-700">{issue.escalation_recommendation}</p>
          </SectionCard>
        </div>

        <div className="space-y-6">
          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">관련 패치</h3>
            <div className="mt-4 space-y-3">
              {issue.related_patches.map((patch) => (
                <Link
                  key={patch.version}
                  to={`/ko/patches/${patch.version}`}
                  className="block rounded-[22px] border border-zinc-200 bg-zinc-50 px-5 py-4 transition hover:border-amber-300"
                >
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-700">{patch.version}</div>
                  <div className="mt-2 text-base font-semibold text-zinc-950">{patch.title}</div>
                  <div className="mt-2 text-xs text-zinc-500">{formatDate(patch.published_at)}</div>
                </Link>
              ))}
            </div>
          </SectionCard>

          <SectionCard>
            <h3 className="text-2xl font-semibold text-zinc-950">출처</h3>
            <div className="mt-4">
              <SourceRefList sources={issue.source_refs} />
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

