import { NavLink, Outlet } from 'react-router-dom';

function navClassName({ isActive }: { isActive: boolean }) {
  return `rounded-full px-4 py-2 text-sm font-medium transition ${
    isActive ? 'bg-ink text-white' : 'text-zinc-700 hover:bg-zinc-200'
  }`;
}

export function AppLayout() {
  return (
    <div className="min-h-screen bg-paper text-ink">
      <div className="mx-auto max-w-7xl px-4 pb-16 pt-6 sm:px-6 lg:px-8">
        <div className="mb-6 rounded-[28px] border border-amber-200 bg-amber-50 px-5 py-4 text-sm leading-6 text-amber-950">
          <div className="font-semibold">비공식 Crimson Desert 지원 허브입니다.</div>
          <div className="mt-1 text-amber-900">
            Pearl Abyss의 공식 고객지원 채널이 아니며, 공식 공지와 FAQ를 한국어 기준으로 재구성해 보여줍니다.
            주요 페이지에는 최신 확인 시각과 출처를 함께 표시합니다.
          </div>
        </div>
        <header className="mb-10 flex flex-col gap-5 rounded-[32px] border border-zinc-200/80 bg-white/85 px-6 py-6 shadow-panel backdrop-blur">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-amber-700">Unofficial Crimson Desert Support Hub</p>
              <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight text-zinc-950">
                한국어 우선으로 운영하는 붉은사막 비공식 지원 허브
              </h1>
            </div>
            <div className="text-sm text-zinc-600">공식 공지 기반, 증상 중심 정리, 출처 표시 우선</div>
          </div>
          <div className="flex flex-wrap gap-2 text-xs font-semibold text-zinc-700">
            {['한국어 우선 런치', '출처 표시', '최신 확인 시각 표시', '해결 보장 없음'].map((item) => (
              <span key={item} className="rounded-full border border-zinc-300 bg-zinc-100 px-3 py-1">
                {item}
              </span>
            ))}
          </div>
          <nav className="flex flex-wrap gap-2">
            <NavLink to="/ko" end className={navClassName}>
              홈
            </NavLink>
            <NavLink to="/ko/patches" className={navClassName}>
              Patch Hub
            </NavLink>
            <NavLink to="/ko/issues" className={navClassName}>
              Known Issues
            </NavLink>
            <NavLink to="/ko/faq" className={navClassName}>
              FAQ
            </NavLink>
            <NavLink to="/ko/settings-doctor" className={navClassName}>
              Settings Doctor
            </NavLink>
            <NavLink to="/ko/search" className={navClassName}>
              Search
            </NavLink>
          </nav>
        </header>
        <Outlet />
        <footer className="mt-10 rounded-[32px] border border-zinc-200/80 bg-white/90 px-6 py-6 shadow-panel">
          <div className="grid gap-6 lg:grid-cols-[1.4fr,0.8fr]">
            <div>
              <h2 className="text-lg font-semibold text-zinc-950">운영 원칙</h2>
              <p className="mt-3 text-sm leading-7 text-zinc-700">
                이 사이트는 공식 공지, FAQ, 패치 노트를 빠르게 찾기 쉽게 정리하는 비공식 팬 운영 허브입니다. 계정,
                결제, 제재, 환불, 법적 분쟁처럼 공식 지원이 필요한 사안은 반드시 Pearl Abyss의 공식 채널을 우선
                이용해야 합니다.
              </p>
              <div className="mt-4 flex flex-wrap gap-2 text-xs text-zinc-600">
                {['공식 안내', '공식 안내 기반 해석', '추론'].map((item) => (
                  <span key={item} className="rounded-full border border-zinc-300 px-3 py-1">
                    신뢰 라벨: {item}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-zinc-950">정책 및 고지</h2>
              <div className="mt-3 grid gap-2 text-sm font-medium text-zinc-700">
                <NavLink to="/ko/privacy" className="rounded-2xl border border-zinc-200 px-4 py-3 transition hover:border-amber-300 hover:bg-amber-50">
                  개인정보 처리방침
                </NavLink>
                <NavLink
                  to="/ko/disclaimer"
                  className="rounded-2xl border border-zinc-200 px-4 py-3 transition hover:border-amber-300 hover:bg-amber-50"
                >
                  면책 및 운영 고지
                </NavLink>
                <NavLink
                  to="/ko/affiliate-disclosure"
                  className="rounded-2xl border border-zinc-200 px-4 py-3 transition hover:border-amber-300 hover:bg-amber-50"
                >
                  제휴 링크 고지
                </NavLink>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
