import { apiClient } from './client';
import type { DailySummary } from '../types/summary';

type ApiEnvelope<T> = {
  data: T;
};

export async function fetchSummaries() {
  const response = await apiClient.get<ApiEnvelope<DailySummary[]>>('/summaries');
  return response.data.data;
}

export async function generateSummary(summaryDate?: string) {
  const response = await apiClient.post<ApiEnvelope<DailySummary>>('/summaries/generate', {
    summary_date: summaryDate || null,
  });
  return response.data.data;
}

