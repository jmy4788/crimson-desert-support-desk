const browserOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://127.0.0.1:4173';

export const SITE_URL = (import.meta.env.VITE_SITE_URL ?? browserOrigin).replace(/\/+$/, '');

export function absoluteUrl(path: string) {
  if (!path) {
    return SITE_URL;
  }
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${SITE_URL}${path.startsWith('/') ? path : `/${path}`}`;
}
