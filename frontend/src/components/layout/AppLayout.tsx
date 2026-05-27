import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';

import { useAppStore } from '../../store/appStore';
import { useAuthStore } from '../../store/authStore';

const navigation = [
  { to: '/', label: 'Dashboard' },
  { to: '/customers', label: 'Customers' },
  { to: '/leads', label: 'Leads' },
  { to: '/messages', label: 'Messages' },
  { to: '/invoices', label: 'Invoices' },
  { to: '/appointments', label: 'Appointments' },
  { to: '/settings', label: 'Settings' },
  { to: '/health', label: 'System Health' },
];

export function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const sidebarOpen = useAppStore((state) => state.sidebarOpen);
  const setSidebarOpen = useAppStore((state) => state.setSidebarOpen);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const pageTitle = navigation.find((item) => item.to === location.pathname)?.label ?? 'Dashboard';

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  const navLinks = (
    <nav className="mt-8 space-y-1 px-3">
      {navigation.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          onClick={() => setSidebarOpen(false)}
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
  );

  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white py-6 md:block">
        <div className="px-5 text-lg font-semibold">AI Operations</div>
        {navLinks}
      </aside>

      {sidebarOpen && (
        <div className="fixed inset-0 z-30 bg-slate-950/30 md:hidden" onClick={() => setSidebarOpen(false)} />
      )}
      <aside
        className={[
          'fixed inset-y-0 left-0 z-40 w-72 border-r border-slate-200 bg-white py-6 transition md:hidden',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        ].join(' ')}
      >
        <div className="flex items-center justify-between px-5">
          <span className="text-lg font-semibold">AI Operations</span>
          <button
            type="button"
            onClick={() => setSidebarOpen(false)}
            className="rounded-md border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700"
          >
            Close
          </button>
        </div>
        <div className="mt-2">{navLinks}</div>
      </aside>

      <div className="md:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 px-4 py-4 backdrop-blur md:px-8">
          <div className="flex items-center justify-between">
            <div className="flex min-w-0 items-center gap-3">
              <button
                type="button"
                onClick={toggleSidebar}
                className="rounded-md border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 md:hidden"
              >
                Menu
              </button>
              <div className="min-w-0">
              <p className="text-sm text-slate-500">Small business automation</p>
                <h1 className="truncate text-xl font-semibold">
                  {user?.business?.name ?? pageTitle}
                </h1>
              </div>
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
