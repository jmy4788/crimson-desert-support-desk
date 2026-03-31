import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { HomePage } from '../pages/HomePage';
import { AppLayout } from '../components/AppLayout';
import { DisclaimerPage } from '../pages/DisclaimerPage';
import { IssueDetailPage } from '../pages/IssueDetailPage';
import { SearchPage } from '../pages/SearchPage';
import { SettingsDoctorPage } from '../pages/SettingsDoctorPage';


const fetchMock = vi.fn();


beforeEach(() => {
  vi.stubGlobal('fetch', fetchMock);
});

afterEach(() => {
  fetchMock.mockReset();
});

describe('frontend pages', () => {
  it('renders home summary cards', async () => {
    fetchMock
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            items: [
              {
                version: '1.01.02',
                title: 'Support Desk Readability Update',
                published_at: '2026-03-29T11:30:00+09:00',
                platforms: ['PC'],
                summary: 'summary',
                latest_checked_at: '2026-03-30T20:20:00+09:00',
                related_issue_slugs: ['dlss-flicker'],
              },
            ],
            total: 1,
            page: 1,
            page_size: 1,
          }),
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            items: [
              {
                slug: 'blurry-screen',
                title: '화면이 흐릿하게 보이는 문제',
                symptom_summary: 'summary',
                category: 'visual',
                status: 'workaround_available',
                platforms: ['PC'],
                last_seen_at: '2026-03-30T18:10:00+09:00',
                latest_checked_at: '2026-03-30T18:10:00+09:00',
                related_patch_versions: ['1.01.01'],
              },
            ],
            total: 1,
            page: 1,
            page_size: 5,
            open_count: 8,
          }),
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            items: [
              {
                id: 1,
                question: '패치 노트는 어디서 확인할 수 있나요?',
                answer: '공식 사이트 기준입니다.',
                tags: ['patch'],
                related_issue_slugs: [],
                related_patch_versions: ['1.01.02'],
                latest_checked_at: '2026-03-30T21:05:00+09:00',
                source_refs: [],
              },
            ],
            total: 1,
            page: 1,
            page_size: 3,
          }),
        ),
      );

    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    );

    expect(await screen.findByText('Support Desk Readability Update')).toBeInTheDocument();
    expect(screen.getByText('8')).toBeInTheDocument();
    expect(screen.getByText('FAQ 하이라이트')).toBeInTheDocument();
  });

  it('renders issue detail with evidence labels', async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          slug: 'blurry-screen',
          title: '화면이 흐릿하게 보이는 문제',
          symptom_summary: 'summary',
          category: 'visual',
          status: 'workaround_available',
          platforms: ['PC'],
          last_seen_at: '2026-03-30T18:10:00+09:00',
          latest_checked_at: '2026-03-30T18:10:00+09:00',
          related_patch_versions: ['1.01.01'],
          source_refs: [],
          workaround_steps: [
            {
              step_order: 1,
              label: '공식 안내',
              step_text: '먼저 확인합니다.',
              risk_level: 'low',
            },
          ],
          related_patches: [],
          landing_page: {
            route_key: 'issue:blurry-screen',
            title: 'title',
            meta_description: 'desc',
            body_markdown: 'body',
            canonical_path: '/ko/issues/blurry-screen',
            faq_items: [],
            updated_at: '2026-03-30T18:10:00+09:00',
          },
          escalation_recommendation: 'report',
        }),
      ),
    );

    render(
      <MemoryRouter initialEntries={['/ko/issues/blurry-screen']}>
        <Routes>
          <Route path="/ko/issues/:slug" element={<IssueDetailPage />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(await screen.findByText('권장 조치 순서')).toBeInTheDocument();
    expect(screen.getByText('공식 안내')).toBeInTheDocument();
    expect(screen.getByText('report')).toBeInTheDocument();
  });

  it('submits settings doctor form and renders actions', async () => {
    fetchMock.mockResolvedValueOnce(
      new Response(
        JSON.stringify({
          matched_issue_slug: 'dlss-flicker',
          report_issue_recommended: true,
          actions: [
            {
              order: 1,
              title: '최신 패치 적용 여부 확인',
              step_text: '패치 허브를 확인합니다.',
              label: '공식 안내',
              risk_level: 'low',
              source_refs: [],
            },
          ],
        }),
      ),
    );

    render(
      <MemoryRouter>
        <SettingsDoctorPage />
      </MemoryRouter>,
    );

    expect(screen.getByText('공식 기준 추천 설정 메모')).toBeInTheDocument();
    expect(screen.getByText('DLSS Multi Frame Generation은 충분한 기본 FPS에서만 켜는 편이 안전합니다')).toBeInTheDocument();

    fireEvent.change(screen.getByPlaceholderText('예: DLSS 켜면 하늘이 깜빡여요'), {
      target: { value: 'DLSS 켜면 하늘이 깜빡여요' },
    });
    fireEvent.click(screen.getByRole('button', { name: '진단 시작' }));

    expect(await screen.findByText('권장 조치')).toBeInTheDocument();
    expect(screen.getByText('최신 패치 적용 여부 확인')).toBeInTheDocument();
  });

  it('shows search empty state without query', async () => {
    fetchMock.mockResolvedValueOnce(new Response(JSON.stringify({ query: '', count: 0, items: [] })));

    render(
      <MemoryRouter initialEntries={['/ko/search']}>
        <Routes>
          <Route path="/ko/search" element={<SearchPage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('검색어를 입력해 주세요')).toBeInTheDocument();
    });
  });

  it('renders layout trust notice and legal links', () => {
    render(
      <MemoryRouter initialEntries={['/ko/disclaimer']}>
        <Routes>
          <Route path="/ko" element={<AppLayout />}>
            <Route path="disclaimer" element={<DisclaimerPage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText('비공식 Crimson Desert 지원 허브입니다.')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: '개인정보 처리방침' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: '면책 및 운영 고지' })).toBeInTheDocument();
  });
});
