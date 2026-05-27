type StatusBadgeProps = {
  label: string;
};

const statusClasses: Record<string, string> = {
  confirmed: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  contacted: 'bg-cyan-50 text-cyan-700 ring-cyan-200',
  converted: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  interested: 'bg-violet-50 text-violet-700 ring-violet-200',
  lost: 'bg-slate-100 text-slate-700 ring-slate-200',
  new: 'bg-amber-50 text-amber-700 ring-amber-200',
  open: 'bg-cyan-50 text-cyan-700 ring-cyan-200',
  paid: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  pending: 'bg-amber-50 text-amber-700 ring-amber-200',
  review: 'bg-amber-50 text-amber-700 ring-amber-200',
  sent: 'bg-slate-100 text-slate-700 ring-slate-200',
  unread: 'bg-red-50 text-red-700 ring-red-200',
  overdue: 'bg-red-50 text-red-700 ring-red-200',
};

export function StatusBadge({ label }: StatusBadgeProps) {
  const key = label.toLowerCase();

  return (
    <span
      className={[
        'inline-flex rounded-md px-2 py-1 text-xs font-semibold ring-1 ring-inset',
        statusClasses[key] ?? 'bg-slate-100 text-slate-700 ring-slate-200',
      ].join(' ')}
    >
      {label}
    </span>
  );
}
