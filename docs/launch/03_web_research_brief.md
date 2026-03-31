# 03 Web Research Brief

Updated: 2026-03-31 (Asia/Seoul)

## Purpose

**Needs web verification**

This document exists only for external web-capable research.

Use it when asking:

- what to do next after the prototype
- what the best launch plan is
- what the fastest path to real revenue is

## What Is Already Verified Internally

**Verified from own build**

Current product:

- local MVP exists
- Korean-first routes exist
- support/issue/patch/FAQ/search/settings-doctor structure exists
- official notice sync pipeline exists
- local DB already contains imported official content

Current verified local snapshot:

- sources: 15
- patches: 6
- issues: 44
- faq_entries: 11
- workaround_steps: 16
- landing_pages: 6

## What Needs External Verification

**Needs web verification**

Research these specifically:

1. true search demand around Crimson Desert support queries
2. who already ranks for crash / blur / stutter / patch note queries
3. legal/trademark risk of unofficial support branding
4. best monetization model by speed-to-first-revenue
5. best launch geography and language order
6. best traffic acquisition channels for this niche
7. realistic KPI targets for 30 / 60 / 90 days

## Working Hypotheses to Test

**Inference / hypothesis**

- support-intent SEO is the best first acquisition channel
- trust and source traceability matter more than content volume
- affiliate revenue may land earlier than meaningful ad revenue
- broad gaming content would dilute focus too early
- Korea-first support positioning is stronger than immediate global sprawl

## Research Questions

**Needs web verification**

Ask the external model to answer:

1. What is the fastest realistic 30-day launch roadmap for a solo operator?
2. Which pages should be built first for traffic and monetization?
3. Which monetization model should be prioritized first, second, and third?
4. What public brand wording is safest for an unofficial support property?
5. What should be the first KPI dashboard?
6. Which distribution channels should be ignored at first?
7. What are the biggest legal and trust risks?

## Paste-Ready Prompt

Use this exact prompt:

---
I built a local MVP called "Crimson Desert Support Desk," an unofficial fan-operated support hub for Crimson Desert.

What is internally verified:

- React + Vite + TypeScript frontend
- FastAPI + SQLModel + SQLite backend
- SQLite FTS5 unified search
- Korean-first routes for home, patches, issues, FAQ, search, and settings doctor
- official notice fetch -> markdown draft -> import pipeline
- local data snapshot after sync:
  - sources: 15
  - patches: 6
  - issues: 44
  - faq_entries: 11
  - workaround_steps: 16
  - landing_pages: 6

What is not yet launch-ready:

- no production deployment
- no monitoring
- no analytics / Search Console
- no privacy/disclaimer/affiliate disclosure pages
- imported issue pages need editorial cleanup
- landing pages are not yet strong SEO assets
- monetization is not live

Strategic hypothesis:

- This should win as a trustworthy unofficial Korean support hub, not as a general game guide site
- The moat is official-source traceability, issue update speed, Korean editing quality, and trust labels

I want you to use current web research and produce:

1. A 30-day launch roadmap with ruthless scope cuts
2. A 60-day and 90-day roadmap
3. A monetization ranking by:
   - easiest to implement
   - fastest to first revenue
   - best long-term upside
4. The best SEO page map for this niche
5. A channel strategy for first traffic
6. The biggest legal/trust/compliance risks
7. Public branding/naming recommendations for an unofficial support site
8. KPI targets for 30 / 60 / 90 days
9. A final "royal road" recommendation with tradeoffs and explicit assumptions

Assume:

- solo operator
- low budget
- wants fastest path to real revenue
- is willing to do manual editorial cleanup if it improves trust

Please clearly separate:

- verified facts
- inference
- items that still need market verification

Please cite current sources and make the answer date-specific.
---

## Useful External Sources

**Needs web verification**

- Official notices: `https://crimsondesert.pearlabyss.com/ko-KR/News/Notice`
- Official Steam page: `https://store.steampowered.com/app/3321460/Crimson_Desert/`
- Current repo context is a local prototype with ingestion scripts and run batches
