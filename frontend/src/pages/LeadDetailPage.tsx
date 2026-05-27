import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import { fetchCustomers, fetchLead, updateLead } from '../api/crm';
import { LeadForm } from '../components/crm/LeadForm';
import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import type { Customer, Lead, LeadPayload } from '../types/crm';

export function LeadDetailPage() {
  const { leadId } = useParams();
  const navigate = useNavigate();
  const [lead, setLead] = useState<Lead | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadLead = async () => {
    if (!leadId) return;
    setLoading(true);
    setError(null);
    try {
      const [leadData, customerData] = await Promise.all([
        fetchLead(leadId),
        fetchCustomers({ page: 1, page_size: 100 }),
      ]);
      setLead(leadData);
      setCustomers(customerData.items);
    } catch {
      setError('Unable to load lead.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadLead();
  }, [leadId]);

  const handleUpdate = async (payload: LeadPayload) => {
    if (!leadId) return;
    try {
      setLead(await updateLead(leadId, payload));
      setEditing(false);
    } catch {
      setError('Unable to update lead.');
    }
  };

  if (loading) {
    return <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600">Loading lead...</div>;
  }

  if (error || !lead) {
    return (
      <section className="mx-auto max-w-4xl space-y-4">
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error ?? 'Lead not found.'}</div>
        <button type="button" onClick={() => navigate('/leads')} className="text-sm font-semibold text-cyan-700">Back to leads</button>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-4xl space-y-6">
      <PageHeader title={lead.title} description="Lead details, conversion status, and priority." />
      <Link to="/leads" className="text-sm font-semibold text-cyan-700">Back to leads</Link>
      {editing ? (
        <LeadForm customers={customers} initialLead={lead} onSubmit={handleUpdate} onCancel={() => setEditing(false)} />
      ) : (
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <p className="text-sm text-slate-500">Customer</p>
              <p className="font-medium text-slate-950">{lead.customer_name || 'Unassigned'}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Status</p>
              <div className="mt-1"><StatusBadge label={lead.status} /></div>
            </div>
            <div>
              <p className="text-sm text-slate-500">Value</p>
              <p className="font-medium text-slate-950">${(lead.value_cents / 100).toLocaleString()}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Priority score</p>
              <p className="font-medium text-slate-950">{lead.priority_score}</p>
            </div>
            <div className="sm:col-span-2">
              <p className="text-sm text-slate-500">Notes</p>
              <p className="mt-1 whitespace-pre-wrap text-slate-700">{lead.notes || 'No notes yet.'}</p>
            </div>
          </div>
          <button type="button" onClick={() => setEditing(true)} className="mt-5 rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white">
            Edit lead
          </button>
        </div>
      )}
    </section>
  );
}
