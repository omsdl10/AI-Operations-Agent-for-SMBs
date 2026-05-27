import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import { fetchCustomer, updateCustomer } from '../api/crm';
import { CustomerForm } from '../components/crm/CustomerForm';
import { PageHeader } from '../components/ui/PageHeader';
import type { Customer, CustomerPayload } from '../types/crm';

export function CustomerDetailPage() {
  const { customerId } = useParams();
  const navigate = useNavigate();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCustomer = async () => {
    if (!customerId) return;
    setLoading(true);
    setError(null);
    try {
      setCustomer(await fetchCustomer(customerId));
    } catch {
      setError('Unable to load customer.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadCustomer();
  }, [customerId]);

  const handleUpdate = async (payload: CustomerPayload) => {
    if (!customerId) return;
    try {
      setCustomer(await updateCustomer(customerId, payload));
      setEditing(false);
    } catch {
      setError('Unable to update customer.');
    }
  };

  if (loading) {
    return <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600">Loading customer...</div>;
  }

  if (error || !customer) {
    return (
      <section className="mx-auto max-w-4xl space-y-4">
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error ?? 'Customer not found.'}</div>
        <button type="button" onClick={() => navigate('/customers')} className="text-sm font-semibold text-cyan-700">Back to customers</button>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-4xl space-y-6">
      <PageHeader title={customer.full_name} description="Customer profile, notes, and tags." />
      <Link to="/customers" className="text-sm font-semibold text-cyan-700">Back to customers</Link>
      {editing ? (
        <CustomerForm initialCustomer={customer} onSubmit={handleUpdate} onCancel={() => setEditing(false)} />
      ) : (
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <p className="text-sm text-slate-500">Phone</p>
              <p className="font-medium text-slate-950">{customer.phone || 'Not set'}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Email</p>
              <p className="font-medium text-slate-950">{customer.email || 'Not set'}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Tags</p>
              <p className="font-medium text-slate-950">{customer.tags.join(', ') || 'None'}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Updated</p>
              <p className="font-medium text-slate-950">{new Date(customer.updated_at).toLocaleString()}</p>
            </div>
            <div className="sm:col-span-2">
              <p className="text-sm text-slate-500">Notes</p>
              <p className="mt-1 whitespace-pre-wrap text-slate-700">{customer.notes || 'No notes yet.'}</p>
            </div>
          </div>
          <button type="button" onClick={() => setEditing(true)} className="mt-5 rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white">
            Edit customer
          </button>
        </div>
      )}
    </section>
  );
}
