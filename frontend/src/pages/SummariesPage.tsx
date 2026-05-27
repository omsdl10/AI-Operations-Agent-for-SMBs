import { useEffect, useMemo, useState } from 'react';

import { fetchSummaries, generateSummary } from '../api/summaries';
import { PageHeader } from '../components/ui/PageHeader';
import { StatCard } from '../components/ui/StatCard';
import type { DailySummary } from '../types/summary';

const metricLabels: Record<string, string> = {
  new_leads: 'New leads',
  conversations_handled: 'Conversations',
  invoices_paid: 'Invoices paid',
  overdue_invoices: 'Overdue invoices',
  pending_follow_ups: 'Pending follow-ups',
  appointments_completed: 'Appointments done',
  appointments_today: 'Appointments today',
  revenue_cents: 'Revenue',
};

export function SummariesPage() {
  const [summaries, setSummaries] = useState<DailySummary[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedSummary = useMemo(
    () => summaries.find((summary) => summary.id === selectedId) ?? summaries[0] ?? null,
    [summaries, selectedId],
  );

  const loadSummaries = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSummaries();
      setSummaries(data);
      setSelectedId((current) => current ?? data[0]?.id ?? null);
    } catch {
      setError('Unable to load daily summaries.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadSummaries();
  }, []);

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);
    try {
      const summary = await generateSummary();
      const data = await fetchSummaries();
      setSummaries(data);
      setSelectedId(summary.id);
    } catch {
      setError('Unable to generate today’s summary.');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!selectedSummary) return;
    const report = [
      `Daily Summary - ${selectedSummary.summary_date}`,
      '',
      selectedSummary.content,
      '',
      'Metrics',
      ...Object.entries(selectedSummary.metrics).map(([key, value]) => `- ${metricLabels[key] ?? key}: ${formatMetric(key, value)}`),
      '',
      'Recommendations',
      ...selectedSummary.recommendations.map((item) => `- ${item}`),
    ].join('\n');
    const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `daily-summary-${selectedSummary.summary_date}.txt`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Daily summaries"
        description="Generate, review, and download AI business summaries."
      />

      <div className="flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={handleGenerate}
          disabled={generating}
          className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-400"
        >
          {generating ? 'Generating...' : 'Generate today'}
        </button>
        <button
          type="button"
          onClick={handleDownload}
          disabled={!selectedSummary}
          className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 disabled:opacity-50"
        >
          Download report
        </button>
      </div>

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      {loading && <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600">Loading summaries...</div>}

      {!loading && (
        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
            {summaries.length === 0 && <div className="p-4 text-sm text-slate-600">No summaries yet.</div>}
            {summaries.map((summary) => (
              <button
                key={summary.id}
                type="button"
                onClick={() => setSelectedId(summary.id)}
                className={[
                  'block w-full border-b border-slate-100 px-4 py-4 text-left hover:bg-slate-50',
                  selectedSummary?.id === summary.id ? 'bg-cyan-50' : '',
                ].join(' ')}
              >
                <p className="font-medium text-slate-950">{summary.summary_date}</p>
                <p className="mt-1 line-clamp-2 text-sm text-slate-600">{summary.content}</p>
              </button>
            ))}
          </div>

          {selectedSummary && (
            <div className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {Object.entries(selectedSummary.metrics).slice(0, 8).map(([key, value]) => (
                  <StatCard
                    key={key}
                    label={metricLabels[key] ?? key}
                    value={formatMetric(key, value)}
                    detail={selectedSummary.summary_date}
                    tone={key.includes('overdue') ? 'red' : 'cyan'}
                  />
                ))}
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="text-base font-semibold text-slate-950">Summary</h3>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-700">{selectedSummary.content}</p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="text-base font-semibold text-slate-950">AI recommendations</h3>
                <ul className="mt-3 space-y-2 text-sm text-slate-700">
                  {selectedSummary.recommendations.map((item) => (
                    <li key={item} className="rounded-md bg-slate-50 px-3 py-2">{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

function formatMetric(key: string, value: number | string) {
  if (key === 'revenue_cents' && typeof value === 'number') {
    return `$${(value / 100).toLocaleString()}`;
  }
  return String(value);
}

