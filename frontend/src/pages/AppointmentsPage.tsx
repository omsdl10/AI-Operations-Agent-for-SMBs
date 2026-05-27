import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { todaysAppointments } from '../data/dashboard';

export function AppointmentsPage() {
  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Appointments" description="Today’s schedule and confirmation status." action="Add appointment" />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {todaysAppointments.map((appointment) => (
          <article key={`${appointment.customer}-${appointment.time}`} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-semibold text-slate-950">{appointment.customer}</p>
                <p className="mt-1 text-sm text-slate-600">{appointment.service}</p>
              </div>
              <StatusBadge label={appointment.status} />
            </div>
            <p className="mt-5 text-2xl font-semibold text-slate-950">{appointment.time}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

