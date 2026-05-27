import { apiClient } from './client';
import type { Customer, CustomerPayload, Lead, LeadPayload, LeadStatus, PaginatedResponse } from '../types/crm';

type ApiEnvelope<T> = {
  data: T;
};

export async function fetchCustomers(params: {
  search?: string;
  tag?: string;
  page?: number;
  page_size?: number;
}) {
  const response = await apiClient.get<ApiEnvelope<PaginatedResponse<Customer>>>('/customers', {
    params,
  });
  return response.data.data;
}

export async function fetchCustomer(id: string) {
  const response = await apiClient.get<ApiEnvelope<Customer>>(`/customers/${id}`);
  return response.data.data;
}

export async function createCustomer(payload: CustomerPayload) {
  const response = await apiClient.post<ApiEnvelope<Customer>>('/customers', payload);
  return response.data.data;
}

export async function updateCustomer(id: string, payload: Partial<CustomerPayload>) {
  const response = await apiClient.put<ApiEnvelope<Customer>>(`/customers/${id}`, payload);
  return response.data.data;
}

export async function deleteCustomer(id: string) {
  await apiClient.delete(`/customers/${id}`);
}

export async function fetchLeads(params: {
  search?: string;
  status?: LeadStatus | '';
  page?: number;
  page_size?: number;
}) {
  const response = await apiClient.get<ApiEnvelope<PaginatedResponse<Lead>>>('/leads', {
    params,
  });
  return response.data.data;
}

export async function fetchLead(id: string) {
  const response = await apiClient.get<ApiEnvelope<Lead>>(`/leads/${id}`);
  return response.data.data;
}

export async function createLead(payload: LeadPayload) {
  const response = await apiClient.post<ApiEnvelope<Lead>>('/leads', payload);
  return response.data.data;
}

export async function updateLead(id: string, payload: Partial<LeadPayload>) {
  const response = await apiClient.put<ApiEnvelope<Lead>>(`/leads/${id}`, payload);
  return response.data.data;
}

export async function deleteLead(id: string) {
  await apiClient.delete(`/leads/${id}`);
}

