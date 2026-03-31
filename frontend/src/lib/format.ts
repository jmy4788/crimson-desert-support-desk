export function formatDate(value: string) {
  return new Intl.DateTimeFormat('ko-KR', {
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}

export function formatShortDate(value: string) {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value));
}

export function humanizeStatus(status: string) {
  return (
    {
      investigating: '조사 중',
      workaround_available: '우회 가능',
      monitoring: '모니터링',
      acknowledged: '인지됨',
      partially_improved: '부분 개선',
      resolved: '해결됨',
    }[status] ?? status
  );
}

export function humanizeCategory(category: string) {
  return (
    {
      visual: '비주얼',
      launch: '실행',
      compatibility: '호환성',
      input: '입력',
      ux: '버전/표시',
      save: '저장',
      performance: '성능',
    }[category] ?? category
  );
}

export function statusTone(status: string) {
  return (
    {
      investigating: 'bg-rose-100 text-rose-700',
      workaround_available: 'bg-amber-100 text-amber-700',
      monitoring: 'bg-sky-100 text-sky-700',
      acknowledged: 'bg-zinc-200 text-zinc-700',
      partially_improved: 'bg-emerald-100 text-emerald-700',
      resolved: 'bg-emerald-200 text-emerald-800',
    }[status] ?? 'bg-zinc-100 text-zinc-700'
  );
}

export function evidenceTone(label: string) {
  return (
    {
      '공식 안내': 'bg-emerald-100 text-emerald-800',
      '공식 안내 기반 해석': 'bg-amber-100 text-amber-800',
      추론: 'bg-zinc-200 text-zinc-800',
    }[label] ?? 'bg-zinc-100 text-zinc-700'
  );
}

