import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link } from 'react-router-dom';

import { SectionCard } from '../components/SectionCard';
import { SourceRefList } from '../components/SourceRefList';
import { StatusBadge } from '../components/StatusBadge';
import { usePageMeta } from '../hooks/usePageMeta';
import { api } from '../lib/api';
import { officialSetupNotes } from '../lib/officialSetupNotes';
import type { DoctorQueryInput, DoctorQueryResponse } from '../types/api';

const INITIAL_FORM: DoctorQueryInput = {
  platform: 'PC',
  gpu_vendor: 'NVIDIA',
  upscaler_mode: 'DLSS',
  symptom: '',
};

export function SettingsDoctorPage() {
  const [form, setForm] = useState<DoctorQueryInput>(INITIAL_FORM);
  const [result, setResult] = useState<DoctorQueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  usePageMeta('Settings Doctor', '플랫폼과 GPU 조합에 따른 안전한 점검 순서를 제시합니다.', '/ko/settings-doctor');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await api.queryDoctor(form);
      setResult(response);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : '진단에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <SectionCard>
        <h2 className="text-3xl font-semibold text-zinc-950">Settings Doctor</h2>
        <p className="mt-2 max-w-3xl text-sm text-zinc-600">
          위험한 트윅 없이, 공식 안내와 저위험 추론만으로 정리한 점검 순서를 제공합니다.
        </p>
        <form onSubmit={handleSubmit} className="mt-6 grid gap-4 md:grid-cols-2">
          <label className="text-sm font-medium text-zinc-700">
            플랫폼
            <select
              value={form.platform}
              onChange={(event) => setForm({ ...form, platform: event.target.value })}
              className="mt-2 w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3"
            >
              {['PC', 'PS5', 'Xbox Series X|S', 'Xbox PC App'].map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <label className="text-sm font-medium text-zinc-700">
            GPU 벤더
            <select
              value={form.gpu_vendor}
              onChange={(event) => setForm({ ...form, gpu_vendor: event.target.value })}
              className="mt-2 w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3"
            >
              {['NVIDIA', 'AMD', 'Intel Arc', 'Console SoC'].map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <label className="text-sm font-medium text-zinc-700">
            업스케일러
            <select
              value={form.upscaler_mode}
              onChange={(event) => setForm({ ...form, upscaler_mode: event.target.value })}
              className="mt-2 w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3"
            >
              {['DLSS', 'FSR', 'XeSS', 'TSR', 'Native'].map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <label className="text-sm font-medium text-zinc-700 md:col-span-2">
            증상 설명
            <input
              value={form.symptom}
              onChange={(event) => setForm({ ...form, symptom: event.target.value })}
              className="mt-2 w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3"
              placeholder="예: DLSS 켜면 하늘이 깜빡여요"
            />
          </label>
          <button
            type="submit"
            disabled={loading || !form.symptom.trim()}
            className="rounded-2xl bg-ink px-5 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-zinc-400"
          >
            {loading ? '진단 중...' : '진단 시작'}
          </button>
        </form>
      </SectionCard>

      <SectionCard>
        <div className="flex flex-wrap items-center gap-3">
          <h3 className="text-2xl font-semibold text-zinc-950">공식 기준 추천 설정 메모</h3>
          <span className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-semibold text-zinc-600">한국어 우선 런치용 수동 큐레이션</span>
        </div>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-zinc-600">
          이 섹션은 “최고 설정”을 단정하지 않습니다. 공식 FAQ와 알려진 문제점 공지에서 바로 근거를 뽑을 수 있는 항목만
          먼저 정리합니다. 커뮤니티 추천 세팅은 별도 라벨 체계로 분리하는 편이 더 안전합니다.
        </p>
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {officialSetupNotes.map((note) => (
            <div key={note.id} className="rounded-[24px] border border-zinc-200 bg-zinc-50 px-5 py-4">
              <div className="flex flex-wrap items-center gap-3">
                <StatusBadge value={note.label} kind="evidence" />
                <span className="text-xs uppercase tracking-[0.18em] text-zinc-500">{note.focus}</span>
              </div>
              <h4 className="mt-3 text-base font-semibold text-zinc-950">{note.title}</h4>
              <div className="mt-3 flex flex-wrap gap-2">
                {note.platforms.map((platform) => (
                  <span key={platform} className="rounded-full border border-zinc-300 px-3 py-1 text-xs font-medium text-zinc-600">
                    {platform}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-sm leading-7 text-zinc-700">{note.body}</p>
              <div className="mt-4">
                <SourceRefList sources={note.source_refs} />
              </div>
            </div>
          ))}
        </div>
      </SectionCard>

      {error ? (
        <SectionCard>
          <p className="text-sm text-rose-700">{error}</p>
        </SectionCard>
      ) : null}

      {result ? (
        <div className="grid gap-6 lg:grid-cols-[1.1fr,0.9fr]">
          <SectionCard>
            <div className="flex flex-wrap items-center gap-3">
              <h3 className="text-2xl font-semibold text-zinc-950">권장 조치</h3>
              {result.matched_issue_slug ? (
                <Link
                  to={`/ko/issues/${result.matched_issue_slug}`}
                  className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800"
                >
                  연결 이슈: {result.matched_issue_slug}
                </Link>
              ) : null}
            </div>
            <div className="mt-5 space-y-4">
              {result.actions.map((action) => (
                <div key={action.order} className="rounded-[24px] border border-zinc-200 bg-zinc-50 px-5 py-4">
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-zinc-900 text-sm font-semibold text-white">
                      {action.order}
                    </span>
                    <StatusBadge value={action.label} kind="evidence" />
                    <span className="text-xs uppercase tracking-[0.18em] text-zinc-500">Risk {action.risk_level}</span>
                  </div>
                  <h4 className="mt-3 text-base font-semibold text-zinc-950">{action.title}</h4>
                  <p className="mt-2 text-sm leading-7 text-zinc-700">{action.step_text}</p>
                </div>
              ))}
            </div>
          </SectionCard>

          <div className="space-y-6">
            <SectionCard>
              <h3 className="text-2xl font-semibold text-zinc-950">판단 메모</h3>
              <p className="mt-4 text-sm leading-7 text-zinc-700">
                {result.report_issue_recommended
                  ? '기본 조치 후에도 문제가 남으면 플랫폼, 패치 버전, GPU, 재현 장면을 함께 기록해 공식 지원 채널로 넘기는 편이 안전합니다.'
                  : '현재 응답 기준으로는 우선 로컬 점검만으로 충분합니다.'}
              </p>
            </SectionCard>
            <SectionCard>
              <h3 className="text-2xl font-semibold text-zinc-950">근거 출처</h3>
              <div className="mt-4">
                <SourceRefList
                  sources={result.actions.flatMap((action) => action.source_refs).filter((source, index, array) => {
                    return array.findIndex((candidate) => candidate.source_url === source.source_url) === index;
                  })}
                />
              </div>
            </SectionCard>
          </div>
        </div>
      ) : null}
    </div>
  );
}
