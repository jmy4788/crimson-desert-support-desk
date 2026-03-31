# 04 Vercel + Render Setup

Updated: 2026-03-31 (Asia/Seoul)

## Goal

Use:

- Vercel for frontend
- Render for backend + Postgres

This is the simplest low-cost launch path for the current repo.

## What Is Already Prepared in Code

- `frontend/vercel.json`
- `render.yaml`
- `frontend/.env.example`
- `.env.example`
- `frontend/scripts/generate-seo.mjs`

## Why This Setup

- frontend is a static SPA and fits Vercel well
- backend is a simple FastAPI app and fits Render well
- Render Postgres is a cleaner production path than SQLite-on-free-web-service

## Important Limits

### Vercel

Use Vercel for the public frontend.

Good fit for first launch because:

- easy repo-based deploy
- custom domain support
- managed TLS/SSL
- hobby plan is good enough for initial static frontend launch

### Render

Use Render for testing and initial public launch carefully.

Free-tier caveats to remember:

- Free web services spin down after 15 minutes of idle time
- free web services can take around a minute to wake back up
- free web services use an ephemeral filesystem
- free Postgres has a 30-day limit

So the Render free tier is good for test launch and validation, but not for stable long-term service.

## What You Need To Do Manually

You still need to do these yourself:

1. Create or connect a Git repository if needed
2. Create a Vercel account
3. Create a Render account
4. Choose the public domain
5. Add environment variables in both dashboards

## Vercel Setup

### Recommended project settings

- Framework preset: Vite
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

### Required environment variables

- `VITE_API_BASE_URL=https://your-render-service.onrender.com`
- `VITE_SITE_URL=https://your-domain.example`

### What the app expects

- SPA rewrite support is already configured in `frontend/vercel.json`
- `robots.txt` and `sitemap.xml` are generated during build
- canonical URLs now use `VITE_SITE_URL`

## Render Setup

### Recommended service type

- Web service for API
- Postgres database for data

### Fastest path

Use `render.yaml` from the repo root.

That file already sets:

- Python runtime
- build command
- start command
- health check path
- Postgres connection wiring

### Environment variables to check manually

- `SUPPORT_DESK_CORS_ORIGINS`

Set this to the final Vercel domain list, for example:

```text
["https://your-domain.example","https://www.your-domain.example"]
```

### Seed behavior

For public deploy, `SUPPORT_DESK_AUTO_SEED_ON_START=false` is the safer default.

Use the official sync/import workflow instead of demo seeding.

## Recommended First Deployment Order

1. Deploy backend to Render
2. Copy the Render service URL
3. Deploy frontend to Vercel with `VITE_API_BASE_URL`
4. Add final frontend domain into `SUPPORT_DESK_CORS_ORIGINS` on Render
5. Re-deploy backend if needed
6. Smoke test:
   - home
   - patch hub
   - issue hub
   - FAQ
   - disclaimer/privacy pages
   - API health

## Recommended Next Work After Deployment

1. Analytics
2. Search Console
3. sitemap submission
4. issue-page manual cleanup
5. top-query landing page refinement
