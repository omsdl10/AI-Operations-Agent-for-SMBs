export type MessageAgentResult = {
  message_id?: string | null;
  intent?: string | null;
  confidence_score?: number | null;
  suggested_reply?: string | null;
  action_required?: string | null;
  follow_up_required?: boolean | null;
  follow_up_id?: string | null;
  lead_id?: string | null;
  appointment_data?: Record<string, unknown> | null;
  invoice_data?: Record<string, unknown> | null;
  requires_human_review?: boolean | null;
  sent_message_id?: string | null;
  ai_reasoning?: string | null;
  error_message?: string | null;
};

