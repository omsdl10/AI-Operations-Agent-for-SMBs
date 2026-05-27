export type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
};

export type Customer = {
  id: string;
  business_id: string;
  full_name: string;
  phone?: string | null;
  email?: string | null;
  notes?: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
};

export type CustomerPayload = {
  full_name: string;
  phone?: string;
  email?: string;
  notes?: string;
  tags: string[];
};

export type LeadStatus = 'new' | 'contacted' | 'interested' | 'converted' | 'lost';

export type Lead = {
  id: string;
  business_id: string;
  customer_id?: string | null;
  title: string;
  status: LeadStatus;
  source?: string | null;
  value_cents: number;
  priority_score: number;
  notes?: string | null;
  customer_name?: string | null;
  created_at: string;
  updated_at: string;
};

export type LeadPayload = {
  title: string;
  customer_id?: string;
  status: LeadStatus;
  source?: string;
  value_cents: number;
  priority_score: number;
  notes?: string;
};

