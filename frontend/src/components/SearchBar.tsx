import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

interface SearchBarProps {
  initialValue?: string;
  placeholder?: string;
  buttonLabel?: string;
  onSubmit: (value: string) => void;
}

export function SearchBar({
  initialValue = '',
  placeholder = '증상, 패치, FAQ를 검색하세요',
  buttonLabel = '검색',
  onSubmit,
}: SearchBarProps) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit(value.trim());
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-3 rounded-[24px] border border-zinc-300 bg-white p-4 sm:flex-row"
    >
      <input
        value={value}
        onChange={(event) => setValue(event.target.value)}
        className="min-w-0 flex-1 rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-amber-400 focus:bg-white"
        placeholder={placeholder}
      />
      <button
        type="submit"
        className="rounded-2xl bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-zinc-800"
      >
        {buttonLabel}
      </button>
    </form>
  );
}
