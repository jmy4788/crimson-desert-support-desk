import type { PropsWithChildren } from 'react';

interface SectionCardProps extends PropsWithChildren {
  className?: string;
}

export function SectionCard({ children, className = '' }: SectionCardProps) {
  return (
    <section className={`rounded-[28px] border border-zinc-200/80 bg-white/90 p-6 shadow-panel ${className}`}>
      {children}
    </section>
  );
}

