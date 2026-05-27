const setupItems = [
  'React + TypeScript frontend',
  'Tailwind CSS styling',
  'React Router navigation',
  'Axios API client',
  'FastAPI backend',
  'PostgreSQL and Redis via Docker Compose',
];

export function DashboardPage() {
  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-wide text-cyan-700">Foundation ready</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-tight">AI Operations Agent</h2>
        <p className="mt-3 max-w-2xl text-slate-600">
          Stage 1 establishes the application shell, API foundation, environment configuration,
          and local infrastructure needed for the product stages ahead.
        </p>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {setupItems.map((item) => (
          <div key={item} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-semibold text-slate-900">{item}</div>
            <div className="mt-2 h-2 rounded-full bg-cyan-100">
              <div className="h-2 rounded-full bg-cyan-600" />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

