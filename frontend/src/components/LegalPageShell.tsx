import type { PropsWithChildren } from 'react';

import { SectionCard } from './SectionCard';

interface LegalPageShellProps extends PropsWithChildren {
  eyebrow: string;
  title: string;
  description: string;
  updatedAt: string;
}

export function LegalPageShell({ eyebrow, title, description, updatedAt, children }: LegalPageShellProps) {
  return (
    <div className="space-y-6">
      <SectionCard className="bg-[radial-gradient(circle_at_top_left,_rgba(180,83,9,0.16),_transparent_38%),linear-gradient(135deg,#fffaf2_0%,#ffffff_60%,#f0ebe1_100%)]">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-amber-700">{eyebrow}</p>
        <h2 className="mt-3 font-display text-4xl font-semibold tracking-tight text-zinc-950">{title}</h2>
        <p className="mt-4 max-w-3xl text-sm leading-7 text-zinc-700">{description}</p>
        <p className="mt-4 text-xs font-medium text-zinc-500">마지막 갱신: {updatedAt}</p>
      </SectionCard>
      {children}
    </div>
  );
}
