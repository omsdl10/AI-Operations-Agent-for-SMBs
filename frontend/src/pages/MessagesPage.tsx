import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { messages } from '../data/dashboard';

export function MessagesPage() {
  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Messages" description="WhatsApp conversations and AI reply status." />
      <div className="grid gap-4 lg:grid-cols-[320px_1fr]">
        <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
          {messages.map((message) => (
            <button
              key={message.customer}
              type="button"
              className="block w-full border-b border-slate-100 px-4 py-4 text-left hover:bg-slate-50"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-medium text-slate-950">{message.customer}</p>
                  <p className="mt-1 text-sm text-slate-600">{message.preview}</p>
                </div>
                <StatusBadge label={message.status} />
              </div>
            </button>
          ))}
        </div>
        <div className="min-h-[420px] rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div className="border-b border-slate-200 pb-4">
            <p className="font-semibold text-slate-950">Maya Johnson</p>
            <p className="text-sm text-slate-500">WhatsApp conversation</p>
          </div>
          <div className="mt-5 space-y-4">
            <div className="max-w-md rounded-lg bg-slate-100 px-4 py-3 text-sm text-slate-700">
              Hi, what is the price for teeth whitening?
            </div>
            <div className="ml-auto max-w-md rounded-lg bg-cyan-700 px-4 py-3 text-sm text-white">
              Whitening starts at $299. I can also help book a consultation slot for tomorrow.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

