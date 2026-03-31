import { useEffect } from 'react';

import { absoluteUrl } from '../lib/site';

export function usePageMeta(title: string, description: string, canonicalPath?: string) {
  useEffect(() => {
    const previousTitle = document.title;
    document.title = title;

    let descriptionTag = document.querySelector('meta[name="description"]');
    if (!descriptionTag) {
      descriptionTag = document.createElement('meta');
      descriptionTag.setAttribute('name', 'description');
      document.head.appendChild(descriptionTag);
    }
    const previousDescription = descriptionTag.getAttribute('content');
    descriptionTag.setAttribute('content', description);

    let canonicalTag = document.querySelector('link[rel="canonical"]');
    if (!canonicalTag) {
      canonicalTag = document.createElement('link');
      canonicalTag.setAttribute('rel', 'canonical');
      document.head.appendChild(canonicalTag);
    }
    const previousCanonical = canonicalTag.getAttribute('href');
    if (canonicalPath) {
      canonicalTag.setAttribute('href', absoluteUrl(canonicalPath));
    }

    return () => {
      document.title = previousTitle;
      if (previousDescription) {
        descriptionTag?.setAttribute('content', previousDescription);
      }
      if (previousCanonical) {
        canonicalTag?.setAttribute('href', previousCanonical);
      }
    };
  }, [title, description, canonicalPath]);
}
