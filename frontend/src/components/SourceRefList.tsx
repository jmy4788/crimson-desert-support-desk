import type { SourceRef } from '../types/api';
import { formatShortDate } from '../lib/format';

interface SourceRefListProps {
  sources: SourceRef[];
}

export function SourceRefList({ sources }: SourceRefListProps) {
  return (
    <div className="space-y-3">
      {sources.map((source) => (
        <a
          key={`${source.source_url}-${source.published_at}`}
          href={source.source_url}
          target="_blank"
          rel="noreferrer"
          className="block rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 transition hover:border-amber-300 hover:bg-amber-50"
        >
          <div className="text-sm font-semibold text-zinc-900">{source.title}</div>
          <div className="mt-1 text-xs text-zinc-600">
            {source.source_type} · 게시 {formatShortDate(source.published_at)} · 확인 {formatShortDate(source.fetched_at)}
          </div>
        </a>
      ))}
    </div>
  );
}

