export type Conversation = {
  customer_id: string;
  customer_name: string;
  phone?: string | null;
  last_message: string;
  last_message_at: string;
  unread_count: number;
  status: string;
};

export type Message = {
  id: string;
  business_id: string;
  customer_id?: string | null;
  direction: 'inbound' | 'outbound';
  channel: string;
  status: string;
  body: string;
  external_id?: string | null;
  sent_at?: string | null;
  created_at: string;
  updated_at: string;
};

