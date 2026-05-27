export type DailySummary = {
  id: string;
  business_id: string;
  summary_date: string;
  content: string;
  metrics: Record<string, number | string>;
  recommendations: string[];
  created_at: string;
  updated_at: string;
};

