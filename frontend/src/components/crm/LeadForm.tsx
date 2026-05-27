import { FormEvent, useState } from 'react';

import type { Customer, Lead, LeadPayload, LeadStatus } from '../../types/crm';

type LeadFormProps = {
  customers: Customer[];
  initialLead?: Lead;
  onSubmit: (payload: LeadPayload) => Promise<void>;
  onCancel: () => void;
};

const statuses: LeadStatus[] = ['new', 'contacted', 'interested', 'converted', 'lost'];

export function LeadForm({ customers, initialLead, onSubmit, onCancel }: LeadFormProps) {
  const [title, setTitle] = useState(initialLead?.title ?? '');
  const [customerId, setCustomerId] = useState(initialLead?.customer_id ?? '');
  const [status, setStatus] = useState<LeadStatus>(initialLead?.status ?? 'new');
  const [source, setSource] = useState(initialLead?.source ?? 'whatsapp');
  const [value, setValue] = useState(String(Math.round((initialLead?.value_cents ?? 0) / 100)));
  const [priorityScore, setPriorityScore] = useState(String(initialLead?.priority_score ?? 0));
  const [notes, setNotes] = useState(initialLead?.notes ?? '');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    try {
      await onSubmit({
        title,
        customer_id: customerId || undefined,
        status,
        source: source || undefined,
        value_cents: Math.max(Number(value || 0), 0) * 100,
        priority_score: Math.max(Math.min(Number(priorityScore || 0), 100), 0),
        notes: notes || undefined,
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Lead title</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={title} onChange={(event) => setTitle(event.target.value)} required />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Customer</span>
          <select className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={customerId} onChange={(event) => setCustomerId(event.target.value)}>
            <option value="">No customer</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>{customer.full_name}</option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Status</span>
          <select className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={status} onChange={(event) => setStatus(event.target.value as LeadStatus)}>
            {statuses.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Source</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={source} onChange={(event) => setSource(event.target.value)} />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Value</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" type="number" min="0" value={value} onChange={(event) => setValue(event.target.value)} />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Priority score</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" type="number" min="0" max="100" value={priorityScore} onChange={(event) => setPriorityScore(event.target.value)} />
        </label>
        <label className="block sm:col-span-2">
          <span className="text-sm font-medium text-slate-700">Notes</span>
          <textarea className="mt-1 min-h-24 w-full rounded-md border border-slate-300 px-3 py-2" value={notes} onChange={(event) => setNotes(event.target.value)} />
        </label>
      </div>
      <div className="mt-5 flex gap-3">
        <button type="submit" disabled={saving} className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-400">
          {saving ? 'Saving...' : 'Save lead'}
        </button>
        <button type="button" onClick={onCancel} className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700">
          Cancel
        </button>
      </div>
    </form>
  );
}
