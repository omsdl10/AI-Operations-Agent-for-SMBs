import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { createLead, deleteLead, fetchCustomers, fetchLeads } from '../api/crm';
import { LeadForm } from '../components/crm/LeadForm';
import { PaginationControls } from '../components/crm/PaginationControls';
import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { TableShell } from '../components/ui/TableShell';
import type { Customer, Lead, LeadPayload, LeadStatus, PaginatedResponse } from '../types/crm';

const leadStatuses: Array<LeadStatus | ''> = ['', 'new', 'contacted', 'interested', 'converted', 'lost'];

export function LeadsPage() {
  const [data, setData] = useState<PaginatedResponse<Lead> | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<LeadStatus | ''>('');
  const [page, setPage] = useState(1);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadLeads = async () => {
    setLoading(true);
    setError(null);
    try {
      const [leads, customerList] = await Promise.all([
        fetchLeads({ search, status, page, page_size: 10 }),
        fetchCustomers({ page: 1, page_size: 100 }),
      ]);
      setData(leads);
      setCustomers(customerList.items);
    } catch {
      setError('Unable to load leads.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadLeads();
  }, [page]);

  const handleSearch = () => {
    setPage(1);
    void loadLeads();
  };

  const handleCreate = async (payload: LeadPayload) => {
    try {
      await createLead(payload);
      setShowForm(false);
      await loadLeads();
    } catch {
      setError('Unable to save lead.');
    }
  };

  const handleDelete = async (leadId: string) => {
    try {
      await deleteLead(leadId);
      await loadLeads();
    } catch {
      setError('Unable to delete lead.');
    }
  };

  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Leads" description="Manage lead pipeline, statuses, and conversion value." />
      {!showForm && (
        <button
          type="button"
          onClick={() => setShowForm(true)}
          className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-800"
        >
          Add lead
        </button>
      )}

      {showForm && (
        <LeadForm customers={customers} onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
      )}

      <div className="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-[1fr_220px_auto]">
        <input
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Search title, source, or notes"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <select
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={status}
          onChange={(event) => setStatus(event.target.value as LeadStatus | '')}
        >
          {leadStatuses.map((item) => (
            <option key={item || 'all'} value={item}>{item || 'All statuses'}</option>
          ))}
        </select>
        <button
          type="button"
          onClick={handleSearch}
          className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700"
        >
          Apply
        </button>
      </div>

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      {loading && <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600">Loading leads...</div>}

      {!loading && data && (
        <TableShell>
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50 text-left text-slate-600">
              <tr>
                <th className="px-4 py-3 font-semibold">Lead</th>
                <th className="px-4 py-3 font-semibold">Customer</th>
                <th className="px-4 py-3 font-semibold">Status</th>
                <th className="px-4 py-3 font-semibold">Value</th>
                <th className="px-4 py-3 font-semibold">Priority</th>
                <th className="px-4 py-3 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data.items.map((lead) => (
                <tr key={lead.id}>
                  <td className="px-4 py-4">
                    <Link to={`/leads/${lead.id}`} className="font-medium text-cyan-700 hover:text-cyan-800">
                      {lead.title}
                    </Link>
                    <p className="text-xs text-slate-500">{lead.source}</p>
                  </td>
                  <td className="px-4 py-4 text-slate-600">{lead.customer_name ?? 'Unassigned'}</td>
                  <td className="px-4 py-4">
                    <StatusBadge label={lead.status} />
                  </td>
                  <td className="px-4 py-4 font-semibold text-slate-950">${(lead.value_cents / 100).toLocaleString()}</td>
                  <td className="px-4 py-4 text-slate-600">{lead.priority_score}</td>
                  <td className="px-4 py-4">
                    <button
                      type="button"
                      onClick={() => void handleDelete(lead.id)}
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
