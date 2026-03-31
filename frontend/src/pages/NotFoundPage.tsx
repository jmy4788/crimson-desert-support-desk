import { Link } from 'react-router-dom';

import { SectionCard } from '../components/SectionCard';

export function NotFoundPage() {
  return (
    <SectionCard>
      <h2 className="text-3xl font-semibold text-zinc-950">페이지를 찾을 수 없습니다</h2>
      <p className="mt-3 text-sm text-zinc-600">경로가 바뀌었거나 아직 준비되지 않은 페이지입니다.</p>
      <Link to="/ko" className="mt-5 inline-flex rounded-full bg-ink px-4 py-2 text-sm font-semibold text-white">
        홈으로
      </Link>
    </SectionCard>
  );
}

