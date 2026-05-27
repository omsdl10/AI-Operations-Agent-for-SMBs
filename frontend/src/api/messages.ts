import { apiClient } from './client';
import type { Conversation, Message } from '../types/message';

type ApiEnvelope<T> = {
  data: T;
};

export async function fetchConversations() {
  const response = await apiClient.get<ApiEnvelope<Conversation[]>>('/messages/conversations');
  return response.data.data;
}

export async function fetchConversationMessages(customerId: string) {
  const response = await apiClient.get<ApiEnvelope<Message[]>>(
    `/messages/conversations/${customerId}`,
  );
  return response.data.data;
}

export async function sendMessage(customerId: string, body: string) {
  const response = await apiClient.post<ApiEnvelope<Message>>('/messages/send', {
    customer_id: customerId,
    body,
  });
  return response.data.data;
}

