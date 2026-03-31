# 01 Status

Updated: 2026-03-31 (Asia/Seoul)

## Executive Summary

**Verified from own build**

This project is no longer a concept-only mockup.

What exists now is:

- a working local MVP
- a real API + database
- a Korean-first support UI
- an official notice fetch/import pipeline
- local Windows run scripts

The main gap is no longer product architecture.
The main gap is launch readiness, editorial quality, and public-service operations.

## Product Definition

**Verified from own build**

Current product intent:

- unofficial Crimson Desert support hub
- Korean-first
- official notice based
- support / issue / patch / FAQ oriented
- search and troubleshooting first

## What Is Implemented

**Verified from own build**

Frontend stack:

- React
- Vite
- TypeScript

Backend stack:

- FastAPI
- SQLModel
- SQLite
- SQLite FTS5 search

Implemented frontend routes:

- `/ko`
- `/ko/patches`
- `/ko/patches/:version`
- `/ko/issues`
- `/ko/issues/:slug`
- `/ko/faq`
- `/ko/search`
- `/ko/settings-doctor`

Implemented backend APIs:

- `GET /api/health`
- `GET /api/patches`
- `GET /api/patches/{version}`
- `GET /api/issues`
- `GET /api/issues/{slug}`
- `GET /api/faq`
- `GET /api/search`
- `POST /api/settings-doctor/query`
- `POST /api/admin/seed`

Implemented product features:

- patch hub
- issue hub
- FAQ page
- unified search
- deterministic settings doctor
- patch diff logic
- official source traceability

## Local Runtime

**Verified from own build**

Current local addresses:

- frontend: `http://127.0.0.1:4173`
- backend: `http://127.0.0.1:8017`

Current Windows helpers:

- `run_support_desk.bat`
- `run_backend.bat`
- `run_frontend.bat`
- `fetch_official_notices.bat`
- `sync_official_notices.bat`

Recent runtime fixes already applied:

- backend port moved off generic local defaults
- frontend/backend CORS aligned for `4173`
- backend startup no longer relies on fragile ASGI module-string boot only
- rerunning backend now exits cleanly if the API is already running

## Data and Content Pipeline

**Verified from own build**

Current content pipeline:

1. fetch official notices
2. generate importable markdown drafts
3. validate drafts
4. import into SQLite

Implemented files:

- `scripts/fetch_official_notices.py`
- `scripts/import_official_source.py`
- `backend/app/services/official_notice_fetcher.py`
- `backend/app/services/importer.py`

Current generated draft directory:

- `raw_sources/incoming/auto`

Current generated draft count:

- `44` markdown files

Last verified database snapshot after sync:

- `sources`: 15
- `patches`: 6
- `issues`: 44
- `faq_entries`: 11
- `workaround_steps`: 16
- `landing_pages`: 6

## What Is Strong Already

**Verified from own build**

These are real strengths now:

- clear information architecture
- official-source-first structure
- Korean-first UX
- working ingestion/import workflow
- actual troubleshooting product shape
- usable prototype, not just wireframes

## Current Gaps

**Verified from own build**

Content quality gaps:

- many auto-imported issue titles/slugs are rough
- known issues are heuristic splits from one official notice
- workaround steps are still sparse on imported official issues
- landing pages are not production-quality SEO assets
- related links between issues/patches/FAQ are shallow

Ops gaps:

- no production deployment
- no monitoring
- no backups strategy documented
- no analytics / Search Console setup
- no public incident/update process

Legal/trust gaps:

- no privacy page
- no disclaimer page
- no affiliate disclosure page
- no explicit trust-label policy on the public product
- no public-facing wording review for unofficial branding risk

Growth gaps:

- no keyword map
- no launch KPI baseline
- no acquisition loop
- no newsletter / Discord / subscriber capture

## What This Document Is Not Claiming

**Needs web verification**

These should not be treated as proven by the local build:

- real market size
- best monetization path
- search volume and keyword economics
- legal safety of public branding
- competitive ranking difficulty

Those belong in external research, not in this file.
