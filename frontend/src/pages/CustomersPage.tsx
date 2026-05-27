import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { createCustomer, deleteCustomer, fetchCustomers } from '../api/crm';
import { CustomerForm } from '../components/crm/CustomerForm';
import { PaginationControls } from '../components/crm/PaginationControls';
import { PageHeader } from '../components/ui/PageHeader';
import { TableShell } from '../components/ui/TableShell';
import type { Customer, CustomerPayload, PaginatedResponse } from '../types/crm';

export function CustomersPage() {
  const [data, setData] = useState<PaginatedResponse<Customer> | null>(null);
  const [search, setSearch] = useState('');
  const [tag, setTag] = useState('');
  const [page, setPage] = useState(1);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const customers = await fetchCustomers({ search, tag, page, page_size: 10 });
      setData(customers);
    } catch {
      setError('Unable to load customers.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadCustomers();
  }, [page]);

  const handleSearch = () => {
    setPage(1);
    void loadCustomers();
  };

  const handleCreate = async (payload: CustomerPayload) => {
    try {
      await createCustomer(payload);
      setShowForm(false);
      await loadCustomers();
    } catch {
      setError('Unable to save customer.');
    }
  };

  const handleDelete = async (customerId: string) => {
    try {
      await deleteCustomer(customerId);
      await loadCustomers();
    } catch {
      setError('Unable to delete customer.');
    }
  };

  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Customers"
        description="Create, search, tag, and manage customer records."
      />
      {!showForm && (
        <button
          type="button"
          onClick={() => setShowForm(true)}
          className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-800"
        >
          Add customer
        </button>
      )}

      {showForm && <CustomerForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />}

      <div className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-[1fr_220px_auto]">
        <input
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Search name, email, or phone"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <input
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Filter by tag"
          value={tag}
          onChange={(event) => setTag(event.target.value)}
        />
        <button
          type="button"
          onClick={handleSearch}
          className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700"
        >
          Apply
        </button>
      </div>

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      {loading && <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600">Loading customers...</div>}

      {!loading && data && (
        <TableShell>
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50 text-left text-slate-600">
              <tr>
                <th className="px-4 py-3 font-semibold">Name</th>
                <th className="px-4 py-3 font-semibold">Phone</th>
                <th className="px-4 py-3 font-semibold">Tags</th>
                <th className="px-4 py-3 font-semibold">Updated</th>
                <th className="px-4 py-3 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data.items.map((customer) => (
                <tr key={customer.id}>
                  <td className="px-4 py-4">
                    <Link to={`/customers/${customer.id}`} className="font-medium text-cyan-700 hover:text-cyan-800">
                      {customer.full_name}
                    </Link>
                    <p className="text-xs text-slate-500">{customer.email}</p>
                  </td>
                  <td className="px-4 py-4 text-slate-600">{customer.phone}</td>
                  <td className="px-4 py-4 text-slate-600">{customer.tags.join(', ') || 'None'}</td>
                  <td className="px-4 py-4 text-slate-600">{new Date(customer.updated_at).toLocaleDateString()}</td>
                  <td className="px-4 py-4">
                    <button
                      type="button"
                      onClick={() => void handleDelete(customer.id)}
                      className="text-sm font-semibold text-red-700 hover:text-red-800"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <PaginationControls page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </TableShell>
      )}
    </section>
  );
}
