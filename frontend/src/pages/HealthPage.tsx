import { useEffect, useState } from 'react';

import { apiClient } from '../api/client';

type HealthState =
  | { status: 'loading' }
  | { status: 'success'; service: string; apiStatus: string }
  | { status: 'error'; message: string };

export function HealthPage() {
  const [health, setHealth] = useState<HealthState>({ status: 'loading' });

  useEffect(() => {
    apiClient
      .get('/health')
      .then((response) => {
        setHealth({
          status: 'success',
          service: response.data.service,
          apiStatus: response.data.status,
        });
      })
      .catch(() => {
        setHealth({
          status: 'error',
          message: 'Backend health check is unavailable.',
        });
      });
  }, []);

  return (
    <section className="mx-auto max-w-3xl rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold">System Health</h2>
      <div className="mt-4 rounded-md bg-slate-50 p-4">
        {health.status === 'loading' && <p className="text-slate-600">Checking backend status...</p>}
        {health.status === 'success' && (
          <p className="text-emerald-700">
            {health.service} is {health.apiStatus}.
          </p>
        )}
        {health.status === 'error' && <p className="text-red-700">{health.message}</p>}
      </div>
    </section>
  );
}

