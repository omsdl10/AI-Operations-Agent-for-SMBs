export const dashboardStats = [
  { label: 'Total leads', value: '128', detail: '+14 this week', tone: 'cyan' },
  { label: 'Unread WhatsApp', value: '18', detail: '6 urgent replies', tone: 'amber' },
  { label: 'Pending follow-ups', value: '32', detail: '9 due today', tone: 'violet' },
  { label: 'Overdue invoices', value: '7', detail: '$4,820 outstanding', tone: 'red' },
  { label: 'Appointments today', value: '11', detail: '3 unconfirmed', tone: 'emerald' },
  { label: 'Revenue summary', value: '$18.4k', detail: '+8.2% this month', tone: 'slate' },
];

export const aiActivityLogs = [
  {
    title: 'Pricing inquiry handled',
    detail: 'Generated WhatsApp reply for Maya Johnson',
    time: '4 min ago',
    status: 'success',
  },
  {
    title: 'Follow-up scheduled',
    detail: 'Created reminder for teeth whitening lead',
    time: '18 min ago',
    status: 'queued',
  },
  {
    title: 'Invoice risk flagged',
    detail: 'Overdue payment reminder needs review',
    time: '42 min ago',
    status: 'review',
  },
  {
    title: 'Appointment confirmed',
    detail: 'Updated calendar slot from WhatsApp response',
    time: '1 hr ago',
    status: 'success',
  },
];

export const todaysAppointments = [
  { customer: 'Maya Johnson', service: 'Whitening consult', time: '10:30 AM', status: 'Confirmed' },
  { customer: 'Ethan Brooks', service: 'Repair estimate', time: '12:00 PM', status: 'Pending' },
  { customer: 'Priya Shah', service: 'Follow-up call', time: '3:15 PM', status: 'Confirmed' },
];

export const revenueRows = [
  { label: 'Paid invoices', value: '$12,640' },
  { label: 'Pending invoices', value: '$8,210' },
  { label: 'Overdue amount', value: '$4,820' },
];

export const customers = [
  { name: 'Maya Johnson', phone: '+1 555 765 4321', tags: 'vip, whatsapp', lastSeen: 'Today' },
  { name: 'Ethan Brooks', phone: '+1 555 332 9011', tags: 'new lead', lastSeen: 'Yesterday' },
  { name: 'Priya Shah', phone: '+1 555 884 1020', tags: 'invoice due', lastSeen: '2 days ago' },
  { name: 'Luis Martinez', phone: '+1 555 456 9012', tags: 'returning', lastSeen: '5 days ago' },
];

export const leads = [
  { title: 'Whitening package', customer: 'Maya Johnson', status: 'interested', value: '$299' },
  { title: 'Monthly maintenance', customer: 'Ethan Brooks', status: 'contacted', value: '$1,200' },
  { title: 'Consultation bundle', customer: 'Nora Lee', status: 'new', value: '$450' },
  { title: 'Annual service plan', customer: 'Owen Clark', status: 'converted', value: '$2,400' },
];

export const messages = [
  { customer: 'Maya Johnson', channel: 'WhatsApp', preview: 'Can I book for tomorrow?', status: 'Unread' },
  { customer: 'Priya Shah', channel: 'WhatsApp', preview: 'I paid the invoice.', status: 'Open' },
  { customer: 'Luis Martinez', channel: 'WhatsApp', preview: 'Please send available slots.', status: 'Replied' },
];

export const invoices = [
  { number: 'INV-1001', customer: 'Maya Johnson', amount: '$299', status: 'sent', due: 'May 31' },
  { number: 'INV-1002', customer: 'Priya Shah', amount: '$820', status: 'overdue', due: 'May 20' },
  { number: 'INV-1003', customer: 'Owen Clark', amount: '$2,400', status: 'paid', due: 'May 25' },
];
