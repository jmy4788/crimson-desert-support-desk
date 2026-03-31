interface PlatformChipsProps {
  platforms: string[];
}

export function PlatformChips({ platforms }: PlatformChipsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {platforms.map((platform) => (
        <span
          key={platform}
          className="rounded-full border border-zinc-300 bg-zinc-50 px-3 py-1 text-xs font-medium text-zinc-700"
        >
          {platform}
        </span>
      ))}
    </div>
  );
}

