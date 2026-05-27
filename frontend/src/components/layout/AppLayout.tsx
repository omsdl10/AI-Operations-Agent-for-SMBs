import { NavLink, Outlet } from 'react-router-dom';

const navigation = [
  { to: '/', label: 'Dashboard' },
  { to: '/health', label: 'System Health' },
];

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white px-5 py-6 md:block">
        <div className="text-lg font-semibold">AI Operations</div>
        <nav className="mt-8 space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  'block rounded-md px-3 py-2 text-sm font-medium transition',
                  isActive
                    ? 'bg-cyan-50 text-cyan-700'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-950',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <div className="md:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 px-4 py-4 backdrop-blur md:px-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500">Small business automation</p>
              <h1 className="text-xl font-semibold">Operations Command Center</h1>
            </div>
            <div className="rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-600">
              Stage 1
            </div>
          </div>
        </header>
        <main className="px-4 py-6 md:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

