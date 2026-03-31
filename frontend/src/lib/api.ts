import type {
  DoctorQueryInput,
  DoctorQueryResponse,
  FAQListResponse,
  HealthResponse,
  IssueDetail,
  IssueListResponse,
  PatchDetail,
  PatchListResponse,
  SearchResponse,
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8017';

function buildUrl(path: string, params?: Record<string, string | number | undefined | null>) {
  const searchParams = new URLSearchParams();
  Object.entries(params ?? {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.set(key, String(value));
    }
  });

  const query = searchParams.toString();
  return `${API_BASE_URL}${path}${query ? `?${query}` : ''}`;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...init,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = (await response.json()) as { detail?: string };
      detail = payload.detail ?? detail;
    } catch {
      detail = response.statusText;
    }
    throw new Error(detail);
  }

  return (await response.json()) as T;
}

export const api = {
  getHealth: () => request<HealthResponse>('/api/health'),
  getPatches: (params?: Record<string, string | number | undefined | null>) =>
    request<PatchListResponse>(buildUrl('/api/patches', params).replace(API_BASE_URL, '')),
  getPatch: (version: string) => request<PatchDetail>(`/api/patches/${encodeURIComponent(version)}`),
  getIssues: (params?: Record<string, string | number | undefined | null>) =>
    request<IssueListResponse>(buildUrl('/api/issues', params).replace(API_BASE_URL, '')),
  getIssue: (slug: string) => request<IssueDetail>(`/api/issues/${encodeURIComponent(slug)}`),
  getFaq: (params?: Record<string, string | number | undefined | null>) =>
    request<FAQListResponse>(buildUrl('/api/faq', params).replace(API_BASE_URL, '')),
  search: (params?: Record<string, string | number | undefined | null>) =>
    request<SearchResponse>(buildUrl('/api/search', params).replace(API_BASE_URL, '')),
  queryDoctor: (payload: DoctorQueryInput) =>
    request<DoctorQueryResponse>('/api/settings-doctor/query', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
