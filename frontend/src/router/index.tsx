import { createBrowserRouter } from 'react-router-dom';

import { ProtectedRoute } from '../components/auth/ProtectedRoute';
import { AppLayout } from '../components/layout/AppLayout';
import { AppointmentsPage } from '../pages/AppointmentsPage';
import { CustomersPage } from '../pages/CustomersPage';
import { CustomerDetailPage } from '../pages/CustomerDetailPage';
import { DashboardPage } from '../pages/DashboardPage';
import { HealthPage } from '../pages/HealthPage';
import { InvoicesPage } from '../pages/InvoicesPage';
import { LeadsPage } from '../pages/LeadsPage';
import { LeadDetailPage } from '../pages/LeadDetailPage';
import { LoginPage } from '../pages/LoginPage';
import { MessagesPage } from '../pages/MessagesPage';
import { NotFoundPage } from '../pages/NotFoundPage';
import { SettingsPage } from '../pages/SettingsPage';
import { SignupPage } from '../pages/SignupPage';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/signup',
    element: <SignupPage />,
  },
  {
    path: '/',
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: 'customers',
            element: <CustomersPage />,
          },
          {
            path: 'customers/:customerId',
            element: <CustomerDetailPage />,
          },
          {
            path: 'leads',
            element: <LeadsPage />,
          },
          {
            path: 'leads/:leadId',
            element: <LeadDetailPage />,
          },
          {
            path: 'messages',
            element: <MessagesPage />,
          },
          {
            path: 'invoices',
            element: <InvoicesPage />,
          },
          {
            path: 'appointments',
            element: <AppointmentsPage />,
          },
          {
            path: 'settings',
            element: <SettingsPage />,
          },
          {
            path: 'health',
            element: <HealthPage />,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
