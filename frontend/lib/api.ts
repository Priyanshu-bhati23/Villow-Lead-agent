import { LeadGenerateRequest, LeadGenerateResponse, ProviderStatusResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchProviderStatus(): Promise<ProviderStatusResponse> {
  const res = await fetch(`${API_BASE_URL}/api/providers/status`, {
    cache: 'no-store',
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch provider status: ${res.statusText}`);
  }
  return res.json();
}

export async function generateLeads(data: LeadGenerateRequest): Promise<LeadGenerateResponse> {
  const res = await fetch(`${API_BASE_URL}/api/leads/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Error generating leads: ${res.statusText}`);
  }

  return res.json();
}
