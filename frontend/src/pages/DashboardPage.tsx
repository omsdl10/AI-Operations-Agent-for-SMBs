import { useEffect, useState } from 'react';

import { PageHeader } from '../components/ui/PageHeader';
import { StatCard } from '../components/ui/StatCard';
import { StatusBadge } from '../components/ui/StatusBadge';
import { aiActivityLogs, dashboardStats, revenueRows, todaysAppointments } from '../data/dashboard';

type DashboardState = 'loading' | 'ready' | 'error';

export function DashboardPage() {
  const [state, setState] = useState<DashboardState>('loading');

  useEffect(() => {
    const timer = window.setTimeout(() => setState('ready'), 250);
    return () => window.clearTimeout(timer);
  }, []);

  if (state === 'loading') {
    return (
      <section className="mx-auto max-w-7xl space-y-6">
        <PageHeader title="Dashboard" description="Live operating view for today." />
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {dashboardStats.map((item) => (
            <div key={item.label} className="h-32 animate-pulse rounded-lg bg-slate-200" />
          ))}
        </div>
      </section>
    );
  }

  if (state === 'error') {
    return (
      <section className="mx-auto max-w-7xl">
        <PageHeader title="Dashboard" description="Live operating view for today." />
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-5 text-sm text-red-700">
          Dashboard data is unavailable.
        </div>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Dashboard"
        description="Track leads, messages, follow-ups, revenue, appointments, and AI activity."
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {dashboardStats.map((item) => (
          <StatCard key={item.label} {...item} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <h3 className="text-base font-semibold text-slate-950">AI activity logs</h3>
            <StatusBadge label="Open" />
          </div>
          <div className="mt-4 divide-y divide-slate-100">
            {aiActivityLogs.map((log) => (
              <div key={log.title} className="flex gap-4 py-4">
                <div className="mt-1 h-2.5 w-2.5 rounded-full bg-cyan-600" />
                <div className="min-w-0 flex-1">
                  <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                    <p className="font-medium text-slate-950">{log.title}</p>
                    <span className="text-xs text-slate-500">{log.time}</span>
                  </div>
                  <p className="mt-1 text-sm text-slate-600">{log.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="text-base font-semibold text-slate-950">Appointments today</h3>
            <div className="mt-4 space-y-3">
              {todaysAppointments.map((appointment) => (
                <div
                  key={`${appointment.customer}-${appointment.time}`}
                  className="rounded-md border border-slate-200 p-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-medium text-slate-950">{appointment.customer}</p>
                      <p className="text-sm text-slate-600">{appointment.service}</p>
                    </div>
                    <StatusBadge label={appointment.status} />
                  </div>
                  <p className="mt-2 text-sm font-medium text-slate-700">{appointment.time}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="text-base font-semibold text-slate-950">Revenue summary</h3>
            <div className="mt-4 space-y-3">
              {revenueRows.map((row) => (
                <div key={row.label} className="flex items-center justify-between text-sm">
                  <span className="text-slate-600">{row.label}</span>
                  <span className="font-semibold text-slate-950">{row.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

