type StatCardProps = {
  label: string;
  value: string;
  detail: string;
  tone: string;
};

const toneClasses: Record<string, string> = {
  amber: 'border-amber-200 bg-amber-50 text-amber-800',
  cyan: 'border-cyan-200 bg-cyan-50 text-cyan-800',
  emerald: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  red: 'border-red-200 bg-red-50 text-red-800',
  slate: 'border-slate-200 bg-slate-50 text-slate-800',
  violet: 'border-violet-200 bg-violet-50 text-violet-800',
};

export function StatCard({ label, value, detail, tone }: StatCardProps) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-600">{label}</p>
      <div className="mt-3 flex items-end justify-between gap-3">
        <p className="text-3xl font-semibold text-slate-950">{value}</p>
        <span
          className={[
            'rounded-md border px-2 py-1 text-xs font-semibold',
            toneClasses[tone] ?? toneClasses.slate,
          ].join(' ')}
        >
          {detail}
        </span>
      </div>
    </article>
  );
}

