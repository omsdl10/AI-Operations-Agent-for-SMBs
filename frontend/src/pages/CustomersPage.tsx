import { PageHeader } from '../components/ui/PageHeader';
import { TableShell } from '../components/ui/TableShell';
import { customers } from '../data/dashboard';

export function CustomersPage() {
  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Customers" description="Customer records, tags, and recent activity." action="Add customer" />
      <TableShell>
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-slate-600">
            <tr>
              <th className="px-4 py-3 font-semibold">Name</th>
              <th className="px-4 py-3 font-semibold">Phone</th>
              <th className="px-4 py-3 font-semibold">Tags</th>
              <th className="px-4 py-3 font-semibold">Last active</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {customers.map((customer) => (
              <tr key={customer.phone}>
                <td className="px-4 py-4 font-medium text-slate-950">{customer.name}</td>
                <td className="px-4 py-4 text-slate-600">{customer.phone}</td>
                <td className="px-4 py-4 text-slate-600">{customer.tags}</td>
                <td className="px-4 py-4 text-slate-600">{customer.lastSeen}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </TableShell>
    </section>
  );
}

