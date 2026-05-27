import type { ReactNode } from 'react';

type TableShellProps = {
  children: ReactNode;
};

export function TableShell({ children }: TableShellProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">{children}</div>
    </div>
  );
}
