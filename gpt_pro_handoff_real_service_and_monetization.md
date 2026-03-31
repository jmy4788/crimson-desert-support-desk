# Crimson Desert Support Desk: Current Status, Next Steps, and Revenue Path

Note:

This file is now a mixed handoff/archive document.
For the cleaner launch-ready split, use:

- `docs/launch/01_status.md`
- `docs/launch/02_strategy.md`
- `docs/launch/03_web_research_brief.md`

Updated: 2026-03-31 (Asia/Seoul)

## 1. What This Project Is

This is an unofficial fan support desk for Crimson Desert.

The goal is:

- Aggregate official patch notes, known issues, and FAQ into one Korean-first support hub
- Make troubleshooting easier than the official notice flow
- Turn that support demand into searchable traffic and eventually revenue

## 2. Current Build Status

### Product status

The MVP exists locally and is usable as a prototype.

Implemented:

- React + Vite + TypeScript frontend
- FastAPI + SQLModel + SQLite backend
- SQLite FTS5 unified search
- Patch hub
- Known issues hub
- FAQ page
- Settings Doctor
- Patch diff logic
- Official notice fetch -> markdown draft generation -> database import flow

### Frontend routes implemented

- `/ko`
- `/ko/patches`
- `/ko/patches/:version`
- `/ko/issues`
- `/ko/issues/:slug`
- `/ko/faq`
- `/ko/search`
- `/ko/settings-doctor`

### Backend APIs implemented

- `GET /api/health`
- `GET /api/patches`
- `GET /api/patches/{version}`
- `GET /api/issues`
- `GET /api/issues/{slug}`
- `GET /api/faq`
- `GET /api/search`
- `POST /api/settings-doctor/query`
- `POST /api/admin/seed`

### Local run status

Current local ports:

- Frontend: `http://127.0.0.1:4173`
- Backend: `http://127.0.0.1:8017`

Windows helpers exist:

- `run_support_desk.bat`
- `run_backend.bat`
- `run_frontend.bat`
- `fetch_official_notices.bat`
- `sync_official_notices.bat`

### Important recent fixes

- Fixed backend port collision by moving this app away from generic local defaults
- Fixed CORS so the frontend on `4173` can call the backend
- Replaced fragile ASGI string import boot with a direct Python runner for backend startup
- Added auto-detection so rerunning backend does not fail noisily if the API is already up

## 3. Data / Content Status

### Seed data

The project originally used sample seed data for demo purposes.

### Official content pipeline now implemented

Official notices can now be fetched from Pearl Abyss notice pages and turned into importable markdown drafts automatically.

Current flow:

1. Fetch official notices
2. Convert them into structured markdown files
3. Validate against importer schema
4. Import into local SQLite database

Implemented files:

- `scripts/fetch_official_notices.py`
- `scripts/import_official_source.py`
- `backend/app/services/official_notice_fetcher.py`
- `backend/app/services/importer.py`

### Current imported data snapshot

After running the official sync flow, the local database count reached:

- `sources`: 15
- `patches`: 6
- `issues`: 44
- `faq_entries`: 11
- `workaround_steps`: 16
- `landing_pages`: 6

### Auto-generated official drafts currently available

`raw_sources/incoming/auto` contains 44 generated markdown files at the moment.

These include:

- Recent patch notes
- One official FAQ-derived item
- Known issues split into multiple issue pages from the official notice

## 4. What Is Good Enough Already

These parts are already strong enough for a serious prototype:

- Information architecture
- Core API shape
- Local demo UX
- Search foundation
- Official-source traceability
- Manual-to-semi-automatic content operations
- Korean-first routing and structure

## 5. What Is Still Not Good Enough for Real Service

This is the critical gap list.

### Content quality / trust layer

- Auto-imported known issues are heuristic splits from one official notice
- Some issue titles/slugs are rough and need editorial cleanup
- Workaround steps for official auto-imported issues are mostly empty
- Landing pages are still sample-oriented, not production SEO assets
- Related links between patches/issues/FAQ are still shallow

### Product / ops layer

- No production deployment yet
- No uptime monitoring
- No error monitoring
- No analytics or event tracking
- No Google Search Console / Bing Webmaster / sitemap / robots flow
- No editorial review queue
- No admin moderation dashboard
- No user feedback loop from the live site

### Business / legal layer

- No privacy policy
- No affiliate disclosure
- No ad policy / monetization policy
- No explicit unofficial-fan-site trust/legal copy strategy
- No trademark-risk review

### Growth layer

- No keyword map
- No programmatic SEO page plan
- No internal linking strategy
- No newsletter or Discord capture
- No community acquisition loop

## 6. What I Think We Should Do Next

If the goal is to get to a real public service quickly, I would do this in order.

### Phase 1: Make the product safe to publish

Priority:

1. Deploy frontend and backend publicly
2. Add real domain, HTTPS, uptime monitoring, and backups
3. Add analytics, Search Console, and sitemap
4. Add legal minimum pages:
   - Privacy
   - Disclaimer
   - Affiliate disclosure placeholder
   - Contact / issue report
5. Add visible disclaimer that this is an unofficial fan support desk built from official notices

### Phase 2: Improve content quality so SEO traffic can stick

Priority:

1. Review all imported issue slugs/titles manually once
2. Build issue templates that convert official notices into cleaner:
   - symptom
   - affected platform
   - current status
   - workaround
   - official source
   - latest checked time
3. Expand FAQ coverage around:
   - blurry graphics
   - stutter
   - crashes
   - preorder bonuses
   - platform/version confusion
4. Generate SEO-grade landing pages for top issue clusters

### Phase 3: Build the traffic loop

Priority:

1. Publish issue pages fast when official notices change
2. Add stronger internal linking:
   - issue -> related patch
   - patch -> unresolved issues
   - FAQ -> relevant issues
   - home -> latest unresolved issues
3. Build page clusters around high-intent fix queries
4. Start collecting email or Discord subscribers

## 7. Fastest Path to Real Revenue

My current belief is:

The fastest realistic revenue path is not premium SaaS.

The royal road is:

1. Capture search traffic for fix/problem intent
2. Turn that traffic into repeat users through update trust
3. Monetize with low-friction methods first

### Best near-term monetization order

#### Option A: Display ads

Why first:

- Easiest to implement
- Best fit for support/search traffic
- No sales friction

Weakness:

- Needs traffic scale before it matters

#### Option B: Hardware / accessory affiliate links

Why second:

- Fits PC troubleshooting intent naturally
- Can be attached to pages about performance, controllers, SSD space, displays

Weakness:

- Must be careful not to recommend junk just to monetize
- Needs disclosure and trust discipline

#### Option C: Newsletter sponsorship later

Why third:

- Better once there is recurring audience
- Good if official patch cadence stays active

Weakness:

- Not useful until you have subscribers and open rates

### Monetization paths I would deprioritize for now

- Paid membership immediately
- Premium app immediately
- Donation-only as primary model
- Broad gaming media expansion before this niche wins

## 8. Why This Niche May Work

Current public signals suggest:

- The game is already released and live on Steam
- Official patch cadence is active
- Official known issues and FAQ content exist
- Third-party media and guide sites are already publishing fix/optimization content

That means there is likely active search demand around:

- crashes
- blurry graphics
- stutter
- platform-specific fixes
- patch note interpretation
- known issue status tracking

This is good for a support/SEO product, but it also means competition is already real.

## 9. What I Need a Web-Capable GPT Pro Analysis To Answer

I want a web-researched answer to these questions:

1. What is the fastest path from this prototype to a real public site with traffic?
2. What is the best 30-day roadmap for launch if I am a solo founder/operator?
3. Which traffic channels are most realistic first:
   - Google SEO
   - Reddit
   - Steam community / forums
   - Discord
   - YouTube shorts / clips
4. Which monetization model is the fastest to first revenue:
   - display ads
   - affiliate
   - sponsorship
   - premium tools
   - newsletter
5. What are the biggest legal / trust risks of operating an unofficial support site around Crimson Desert?
6. Which exact page types should be built first for SEO and revenue?
7. What KPI targets should define success in the first 30 / 60 / 90 days?

## 10. Paste-Ready Prompt for Web GPT Pro

Use this exact context:

---
I built a local MVP called "Crimson Desert Support Desk," an unofficial fan-operated support hub for Crimson Desert.

Current stack:
- Frontend: React + Vite + TypeScript
- Backend: FastAPI + SQLModel + SQLite
- Search: SQLite FTS5

Current routes:
- /ko
- /ko/patches
- /ko/patches/:version
- /ko/issues
- /ko/issues/:slug
- /ko/faq
- /ko/search
- /ko/settings-doctor

Current backend APIs:
- GET /api/health
- GET /api/patches
- GET /api/patches/{version}
- GET /api/issues
- GET /api/issues/{slug}
- GET /api/faq
- GET /api/search
- POST /api/settings-doctor/query
- POST /api/admin/seed

Current implemented product behavior:
- Korean-first support hub
- patch notes hub
- known issues hub
- FAQ
- unified search
- deterministic settings doctor
- official-source traceability
- official notice fetch -> markdown draft -> import pipeline

Current local data status after sync:
- sources: 15
- patches: 6
- issues: 44
- faq_entries: 11
- workaround_steps: 16
- landing_pages: 6

Current official-content pipeline:
- fetch official notices from Pearl Abyss notice pages
- generate structured markdown drafts
- validate them
- import into local SQLite

Current gaps:
- no production deployment
- no uptime/error monitoring
- no analytics or search console
- no privacy/disclaimer/affiliate disclosure pages
- auto-imported known issues are heuristic and need editorial cleanup
- landing pages are not production-quality SEO pages yet
- monetization is not implemented
- no growth loop yet

My goal:
- launch a real public version quickly
- get to first real revenue as fast as possible
- stay focused on one niche instead of broad gaming media
- use official data as the trust backbone

I want you to use current web research and give me:

1. A brutally practical 30-day launch roadmap
2. A 60-day and 90-day growth roadmap
3. The fastest realistic monetization path for this exact product
4. A ranking of monetization models by speed-to-first-revenue and long-term upside
5. A recommended SEO page map for this niche
6. A distribution strategy for first traffic
7. The legal/trust/compliance risks of running an unofficial support site for Crimson Desert
8. A KPI dashboard for the first 90 days
9. A recommendation on whether I should stay narrow on support/issue pages or expand into broader guides/news
10. A final "royal road" recommendation with tradeoffs, assumptions, and what to NOT do

Assume:
- solo operator
- low initial budget
- wants fastest path to meaningful revenue
- okay with manual editorial review if it materially improves trust

Please cite current sources and make the recommendation date-specific.
---

## 11. Useful Sources for the External Analysis

- Official notices: `https://crimsondesert.pearlabyss.com/ko-KR/News/Notice`
- Official Steam page: `https://store.steampowered.com/app/3321460/Crimson_Desert/`
- Existing repo has local scripts and batches for fetch/sync/import

## 12. My Current Opinion in One Line

If the goal is fastest revenue, the winning path is:

launch a very trustworthy, search-oriented unofficial support hub first, monetize low-friction traffic before building anything premium, and only widen into broader guides after the support niche already wins.
