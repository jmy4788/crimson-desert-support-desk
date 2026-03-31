export interface SourceRef {
  title: string;
  source_type: string;
  source_url: string;
  published_at: string;
  fetched_at: string;
}

export interface LandingFAQItem {
  question: string;
  answer: string;
}

export interface LandingMeta {
  route_key: string;
  title: string;
  meta_description: string;
  body_markdown: string;
  canonical_path: string;
  faq_items: LandingFAQItem[];
  updated_at: string;
}

export interface WorkaroundStep {
  step_order: number;
  label: string;
  step_text: string;
  risk_level: string;
}

export interface RelatedPatchSummary {
  version: string;
  title: string;
  published_at: string;
}

export interface RelatedIssueSummary {
  slug: string;
  title: string;
  status: string;
  category: string;
  last_seen_at: string;
}

export interface PatchDiffEntry {
  category: string;
  current_text?: string | null;
  previous_text?: string | null;
}

export interface PatchDiff {
  initial_release: boolean;
  added: PatchDiffEntry[];
  changed: PatchDiffEntry[];
  removed: PatchDiffEntry[];
}

export interface PatchSection {
  category: string;
  items: string[];
}

export interface PatchSummary {
  version: string;
  title: string;
  published_at: string;
  platforms: string[];
  summary: string;
  latest_checked_at: string;
  related_issue_slugs: string[];
}

export interface PatchDetail extends PatchSummary {
  source_refs: SourceRef[];
  sections: PatchSection[];
  diff: PatchDiff;
  related_issues: RelatedIssueSummary[];
  landing_page?: LandingMeta | null;
}

export interface PatchListResponse {
  items: PatchSummary[];
  total: number;
  page: number;
  page_size: number;
}

export interface IssueSummary {
  slug: string;
  title: string;
  symptom_summary: string;
  category: string;
  status: string;
  platforms: string[];
  last_seen_at: string;
  latest_checked_at: string;
  related_patch_versions: string[];
}

export interface IssueDetail extends IssueSummary {
  source_refs: SourceRef[];
  workaround_steps: WorkaroundStep[];
  related_patches: RelatedPatchSummary[];
  landing_page?: LandingMeta | null;
  escalation_recommendation: string;
}

export interface IssueListResponse {
  items: IssueSummary[];
  total: number;
  page: number;
  page_size: number;
  open_count: number;
}

export interface FAQItem {
  id: number;
  question: string;
  answer: string;
  tags: string[];
  related_issue_slugs: string[];
  related_patch_versions: string[];
  latest_checked_at: string;
  source_refs: SourceRef[];
}

export interface FAQListResponse {
  items: FAQItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface SearchResultItem {
  type: string;
  title: string;
  slug_or_version: string;
  snippet: string;
  platforms: string[];
  updated_at: string;
  url: string;
}

export interface SearchResponse {
  query: string;
  count: number;
  items: SearchResultItem[];
}

export interface DoctorQueryInput {
  platform: string;
  gpu_vendor: string;
  upscaler_mode: string;
  symptom: string;
}

export interface DoctorAction {
  order: number;
  title: string;
  step_text: string;
  label: string;
  risk_level: string;
  source_refs: SourceRef[];
}

export interface DoctorQueryResponse {
  matched_issue_slug?: string | null;
  report_issue_recommended: boolean;
  actions: DoctorAction[];
}

export interface HealthResponse {
  status: string;
  environment: string;
  counts: Record<string, number>;
}

