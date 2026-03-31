import { evidenceTone, humanizeStatus, statusTone } from '../lib/format';

interface StatusBadgeProps {
  value: string;
  kind?: 'status' | 'evidence';
}

export function StatusBadge({ value, kind = 'status' }: StatusBadgeProps) {
  const tone = kind === 'status' ? statusTone(value) : evidenceTone(value);
  const label = kind === 'status' ? humanizeStatus(value) : value;
  return <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${tone}`}>{label}</span>;
}

