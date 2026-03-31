import { useEffect, useState } from 'react';

interface ApiState<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

export function useApi<T>(loader: () => Promise<T>, deps: unknown[]): ApiState<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isActive = true;
    setLoading(true);
    setError(null);

    loader()
      .then((value) => {
        if (isActive) {
          setData(value);
        }
      })
      .catch((reason: unknown) => {
        if (isActive) {
          setError(reason instanceof Error ? reason.message : '요청에 실패했습니다.');
        }
      })
      .finally(() => {
        if (isActive) {
          setLoading(false);
        }
      });

    return () => {
      isActive = false;
    };
  }, deps);

  return { data, error, loading };
}

