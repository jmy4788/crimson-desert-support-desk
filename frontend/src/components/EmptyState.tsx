interface EmptyStateProps {
  title: string;
  description: string;
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="rounded-[28px] border border-dashed border-zinc-300 bg-white/80 p-8 text-center">
      <div className="text-base font-semibold text-zinc-900">{title}</div>
      <p className="mt-2 text-sm text-zinc-600">{description}</p>
    </div>
  );
}

