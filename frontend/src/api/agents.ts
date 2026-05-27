import { apiClient } from './client';
import type { MessageAgentResult } from '../types/agent';

type ApiEnvelope<T> = {
  data: T;
};

export async function runMessageAgent(messageId: string) {
  const response = await apiClient.post<ApiEnvelope<MessageAgentResult>>(
    `/agents/messages/${messageId}/run`,
  );
  return response.data.data;
}

