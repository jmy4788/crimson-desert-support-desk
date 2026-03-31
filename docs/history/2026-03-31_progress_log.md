# Crimson Desert Support Desk Progress Log

Updated: 2026-03-31 (Asia/Seoul)

## Purpose

This file is a dated memory log for the project so that work can be resumed quickly without relying on chat history.

## Current Product Status

- Public frontend is deployed on Vercel:
  - https://crimson-desert-support-desk.vercel.app/ko
- Public backend is deployed on Render:
  - https://crimson-desert-support-desk-api.onrender.com/api/health
- Repository is pushed to GitHub:
  - https://github.com/jmy4788/crimson-desert-support-desk

## What Was Built

### Monorepo structure

- `frontend`: React + Vite + TypeScript + Tailwind
- `backend`: FastAPI + SQLModel
- `data`: sample seed data and runtime DB path
- `scripts`: local seed, import, backend run, official notice fetch
- `raw_sources`: import templates and generated official markdown drafts

### Backend MVP

- Implemented APIs:
  - `GET /api/health`
  - `GET /api/patches`
  - `GET /api/patches/{version}`
  - `GET /api/issues`
  - `GET /api/issues/{slug}`
  - `GET /api/faq`
  - `GET /api/search`
  - `POST /api/settings-doctor/query`
  - `POST /api/admin/seed` in non-production only
- Implemented schema:
  - `sources`
  - `patches`
  - `issues`
  - `patch_issue_links`
  - `faq_entries`
  - `workaround_steps`
  - `landing_pages`
- Added SQLite FTS search with non-SQLite fallback search logic
- Added deterministic Settings Doctor rule engine
- Added patch diff logic against previous patch version

### Frontend MVP

- Implemented locale-prefixed routes:
  - `/ko`
  - `/ko/patches`
  - `/ko/patches/:version`
  - `/ko/issues`
  - `/ko/issues/:slug`
  - `/ko/faq`
  - `/ko/settings-doctor`
  - `/ko/search`
- Added unofficial disclaimer and legal pages:
  - privacy
  - disclaimer
  - affiliate disclosure
- Added source references, latest checked timestamps, and trust-label presentation

### Import and official-content pipeline

- Added markdown frontmatter import CLI
- Added templates for:
  - patch notes
  - known issues
  - FAQ
- Added official notice auto-fetch pipeline from the Crimson Desert official notice board
- Added generated draft output under `raw_sources/incoming/auto`
- Added one-click sync BAT workflow for local refresh

### Deployment readiness

- Added Vercel config:
  - `frontend/vercel.json`
- Added Render blueprint:
  - `render.yaml`
- Added deployment docs:
  - `docs/launch/04_vercel_render_setup.md`
- Added canonical URL and SEO asset generation:
  - `robots.txt`
  - `sitemap.xml`
- Added Postgres connection normalization for Render
- Added CORS env parsing for deployed frontend domain

## What Was Deployed Today

### Git

- Initialized first real remote push to GitHub
- Renamed branch to `main`
- First pushed commit:
  - `3577dd3`

### Render

- Created Render web service and Render Postgres through `render.yaml`
- Verified production health endpoint
- Imported official notice data into the Render Postgres database

### Vercel

- Deployed frontend from GitHub repo
- Connected frontend to Render API via `VITE_API_BASE_URL`
- Set site base URL via `VITE_SITE_URL`
- Confirmed live frontend rendering against deployed backend

## Important Production Notes

- The site is deployed and reachable publicly now.
- Browser cache caused an initial false negative in one non-incognito session.
- Production data currently comes from official auto-import only, not from the richer local sample dataset.
- As of this log, production health reported:

```json
{
  "status": "ok",
  "environment": "prod",
  "counts": {
    "sources": 10,
    "patches": 7,
    "issues": 37,
    "faq_entries": 1,
    "landing_pages": 0
  }
}
```

## Decisions Made

- Public positioning:
  - `비공식 Crimson Desert 지원 허브`
- Launch scope:
  - Korean-first launch now
  - English expansion later
- Hosting direction:
  - Vercel for frontend
  - Render for backend and Postgres
- Current posture:
  - soft private deployment / pre-launch validation
  - not yet final polished public launch

## Hosting Notes Checked On 2026-03-31

- Vercel Hobby:
  - free
  - intended for personal and non-commercial use
  - includes 1M edge requests per month
  - includes 100 GB fast data transfer per month
- Render free web service:
  - 512 MB RAM
  - 0.1 CPU
  - included bandwidth is 100 GB per month at Hobby tier
- Render free Postgres:
  - free tier has a 30-day limit
  - 256 MB RAM
  - 0.1 CPU
  - 100 connection limit

Practical conclusion:

- good enough for test deployment and small soft-launch validation
- not good enough for long-lived monetized production without upgrades

## Known Gaps As Of 2026-03-31

- Production FAQ is still too thin because the official FAQ auto-fetch currently compresses too much into a single FAQ entry
- Production landing page metadata is still not populated
- Official issue slugs are long and auto-generated; they need editorial cleanup later
- Search Console, analytics, and custom domain are not set up yet
- Legal copy exists, but final branding and trust wording may still need refinement

## Follow-up Work Added Later The Same Day

- Implemented improved official FAQ extraction logic so one official FAQ notice can now generate multiple FAQ entries instead of a single giant merged entry
- Implemented automatic landing metadata generation for auto-fetched patch and issue documents
- Implemented frontend rendering of landing-page FAQ snippets on patch detail and issue detail pages
- Verified new fetch pipeline locally with:
  - `Fetched notices: 10`
  - `Generated drafts: 60`
  - FAQ entries now split into multiple documents during draft generation
- These improvements are committed locally, but production will not reflect them until:
  1. updated code is pushed
  2. Vercel / Render redeploy
  3. official notices are re-imported into the Render production database

## Files And Docs That Matter Most

- Main launch docs:
  - `docs/launch/01_status.md`
  - `docs/launch/02_strategy.md`
  - `docs/launch/03_web_research_brief.md`
  - `docs/launch/04_vercel_render_setup.md`
- Deployment root files:
  - `render.yaml`
  - `frontend/vercel.json`
- Official content pipeline:
  - `scripts/fetch_official_notices.py`
  - `scripts/import_official_source.py`
  - `backend/app/services/official_notice_fetcher.py`
  - `backend/app/services/importer.py`

## Immediate Next Priorities

1. Improve FAQ extraction so official FAQ turns into multiple usable FAQ entries
2. Generate or populate landing metadata for top issue and patch detail pages
3. Re-import improved content into production database
4. Add analytics and Search Console
5. Add custom domain
6. Curate top issue pages manually before broader launch

## Resume Prompt

If work resumes later, start from this checklist:

1. Verify Vercel frontend still renders live data
2. Verify Render health endpoint and production counts
3. Check latest official notices for new patch / issue updates
4. Continue FAQ + landing-page enhancement pipeline
5. Re-import improved content into production after verification
