import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { TableShell } from '../components/ui/TableShell';
import { invoices } from '../data/dashboard';

export function InvoicesPage() {
  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Invoices" description="Payment status, reminders, and overdue balances." action="New invoice" />
      <TableShell>
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-slate-600">
            <tr>
              <th className="px-4 py-3 font-semibold">Invoice</th>
              <th className="px-4 py-3 font-semibold">Customer</th>
              <th className="px-4 py-3 font-semibold">Amount</th>
              <th className="px-4 py-3 font-semibold">Status</th>
              <th className="px-4 py-3 font-semibold">Due</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {invoices.map((invoice) => (
              <tr key={invoice.number}>
                <td className="px-4 py-4 font-medium text-slate-950">{invoice.number}</td>
                <td className="px-4 py-4 text-slate-600">{invoice.customer}</td>
                <td className="px-4 py-4 font-semibold text-slate-950">{invoice.amount}</td>
                <td className="px-4 py-4">
                  <StatusBadge label={invoice.status} />
                </td>
                <td className="px-4 py-4 text-slate-600">{invoice.due}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </TableShell>
    </section>
  );
}

