import { PageHeader } from '../components/ui/PageHeader';

export function SettingsPage() {
  return (
    <section className="mx-auto max-w-4xl space-y-6">
      <PageHeader title="Settings" description="Business profile, integrations, and notification defaults." />
      <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="grid gap-5 sm:grid-cols-2">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Business name</span>
            <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" defaultValue="Bright Smile Dental" />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Industry</span>
            <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" defaultValue="Dental Clinic" />
          </label>
          <label className="block sm:col-span-2">
            <span className="text-sm font-medium text-slate-700">WhatsApp number</span>
            <input className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2" defaultValue="+1 555 123 4567" />
          </label>
        </div>
        <button type="button" className="mt-5 rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-800">
          Save settings
        </button>
      </div>
    </section>
  );
}
