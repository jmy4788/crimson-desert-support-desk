import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendRoot = path.resolve(__dirname, '..');
const repoRoot = path.resolve(frontendRoot, '..');
const outputDir = path.join(frontendRoot, 'public');
const rawSourcesDir = path.join(repoRoot, 'raw_sources', 'incoming', 'auto');

const siteUrl = normalizeSiteUrl(process.env.VITE_SITE_URL || process.env.SITE_URL || 'https://example.com');
const today = new Date().toISOString();

const routes = new Map();
[
  '/ko',
  '/ko/patches',
  '/ko/issues',
  '/ko/faq',
  '/ko/search',
  '/ko/settings-doctor',
  '/ko/privacy',
  '/ko/disclaimer',
  '/ko/affiliate-disclosure',
].forEach((route) => {
  routes.set(route, today);
});

if (fs.existsSync(rawSourcesDir)) {
  for (const fileName of fs.readdirSync(rawSourcesDir)) {
    if (!fileName.endsWith('.md')) {
      continue;
    }

    const fullPath = path.join(rawSourcesDir, fileName);
    const frontmatter = extractFrontmatter(fs.readFileSync(fullPath, 'utf8'));
    if (!frontmatter) {
      continue;
    }

    const sourceType = readFrontmatterValue(frontmatter, 'source_type');
    const fetchedAt = readFrontmatterValue(frontmatter, 'fetched_at') || readFrontmatterValue(frontmatter, 'published_at') || today;

    if (sourceType === 'patch_note') {
      const version = readFrontmatterValue(frontmatter, 'version');
      if (version) {
        routes.set(`/ko/patches/${version}`, fetchedAt);
      }
    }

    if (sourceType === 'known_issue') {
      const slug = readFrontmatterValue(frontmatter, 'slug');
      if (slug) {
        routes.set(`/ko/issues/${slug}`, fetchedAt);
      }
    }
  }
}

const sitemapEntries = [...routes.entries()]
  .map(([route, lastmod]) => {
    return `  <url>\n    <loc>${escapeXml(`${siteUrl}${route}`)}</loc>\n    <lastmod>${escapeXml(formatLastModified(lastmod))}</lastmod>\n  </url>`;
  })
  .join('\n');

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${sitemapEntries}\n</urlset>\n`;
const robots = `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;

fs.writeFileSync(path.join(outputDir, 'sitemap.xml'), sitemap, 'utf8');
fs.writeFileSync(path.join(outputDir, 'robots.txt'), robots, 'utf8');

function normalizeSiteUrl(value) {
  return value.replace(/\/+$/, '');
}

function extractFrontmatter(fileContent) {
  const match = fileContent.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  return match ? match[1] : null;
}

function readFrontmatterValue(frontmatter, key) {
  const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`^${escapedKey}:\\s*(.+)$`, 'm');
  const match = frontmatter.match(regex);
  if (!match) {
    return null;
  }

  const rawValue = match[1].trim();
  if (rawValue.startsWith('"') && rawValue.endsWith('"')) {
    return rawValue.slice(1, -1).trim();
  }
  return rawValue;
}

function formatLastModified(value) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return new Date().toISOString();
  }
  return parsed.toISOString();
}

function escapeXml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}
