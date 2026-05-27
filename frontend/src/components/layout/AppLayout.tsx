import { NavLink, Outlet, useNavigate } from 'react-router-dom';

import { useAuthStore } from '../../store/authStore';

const navigation = [
  { to: '/', label: 'Dashboard' },
  { to: '/health', label: 'System Health' },
];

export function AppLayout() {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

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
              <h1 className="text-xl font-semibold">
                {user?.business?.name ?? 'Operations Command Center'}
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden text-right text-sm sm:block">
                <p className="font-medium text-slate-900">{user?.full_name}</p>
                <p className="text-slate-500">{user?.role}</p>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                className="rounded-md border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                Log out
              </button>
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
