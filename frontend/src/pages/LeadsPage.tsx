import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { TableShell } from '../components/ui/TableShell';
import { leads } from '../data/dashboard';

export function LeadsPage() {
  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Leads" description="Pipeline status, customer intent, and deal value." action="Add lead" />
      <TableShell>
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-slate-600">
            <tr>
              <th className="px-4 py-3 font-semibold">Lead</th>
              <th className="px-4 py-3 font-semibold">Customer</th>
              <th className="px-4 py-3 font-semibold">Status</th>
              <th className="px-4 py-3 font-semibold">Value</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {leads.map((lead) => (
              <tr key={lead.title}>
                <td className="px-4 py-4 font-medium text-slate-950">{lead.title}</td>
                <td className="px-4 py-4 text-slate-600">{lead.customer}</td>
                <td className="px-4 py-4">
                  <StatusBadge label={lead.status} />
                </td>
                <td className="px-4 py-4 font-semibold text-slate-950">{lead.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </TableShell>
    </section>
  );
}

