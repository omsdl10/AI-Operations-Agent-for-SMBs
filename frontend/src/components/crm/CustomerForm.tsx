import { FormEvent, useState } from 'react';

import type { Customer, CustomerPayload } from '../../types/crm';

type CustomerFormProps = {
  initialCustomer?: Customer;
  onSubmit: (payload: CustomerPayload) => Promise<void>;
  onCancel: () => void;
};

export function CustomerForm({ initialCustomer, onSubmit, onCancel }: CustomerFormProps) {
  const [fullName, setFullName] = useState(initialCustomer?.full_name ?? '');
  const [phone, setPhone] = useState(initialCustomer?.phone ?? '');
  const [email, setEmail] = useState(initialCustomer?.email ?? '');
  const [notes, setNotes] = useState(initialCustomer?.notes ?? '');
  const [tags, setTags] = useState(initialCustomer?.tags.join(', ') ?? '');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    try {
      await onSubmit({
        full_name: fullName,
        phone: phone || undefined,
        email: email || undefined,
        notes: notes || undefined,
        tags: tags
          .split(',')
          .map((tag) => tag.trim())
          .filter(Boolean),
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Full name</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={fullName} onChange={(event) => setFullName(event.target.value)} required />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Phone</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={phone} onChange={(event) => setPhone(event.target.value)} />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Email</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Tags</span>
          <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" value={tags} onChange={(event) => setTags(event.target.value)} placeholder="vip, whatsapp" />
        </label>
        <label className="block sm:col-span-2">
          <span className="text-sm font-medium text-slate-700">Notes</span>
          <textarea className="mt-1 min-h-24 w-full rounded-md border border-slate-300 px-3 py-2" value={notes} onChange={(event) => setNotes(event.target.value)} />
        </label>
      </div>
      <div className="mt-5 flex gap-3">
        <button type="submit" disabled={saving} className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-400">
          {saving ? 'Saving...' : 'Save customer'}
        </button>
        <button type="button" onClick={onCancel} className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700">
          Cancel
        </button>
      </div>
    </form>
  );
}
