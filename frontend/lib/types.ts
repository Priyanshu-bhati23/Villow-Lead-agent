export interface Signal {
  id?: string;
  signal_type: 'funding' | 'hiring' | 'technology' | 'job_posting' | string;
  signal_text: string;
  source_url?: string;
  detected_at?: string;
}

export interface ScoreBreakdown {
  icp_fit: number;
  signal_strength: number;
  signal_recency: number;
  company_relevance: number;
  data_confidence: number;
}

export interface Lead {
  id?: string;
  company_name: string;
  website?: string;
  description?: string;
  industry?: string;
  location?: string;
  signals: Signal[];
  sources: string[];
  score: number;
  score_breakdown: ScoreBreakdown;
  why_this_is_a_good_lead?: string;
  why_now?: string;
  outreach_hook?: string;
  created_at?: string;
}

export interface LeadGenerateRequest {
  icp: string;
  industry?: string;
  geography?: string;
  number_of_leads: number;
}

export interface LeadGenerateResponse {
  request_id: string;
  icp: string;
  industry?: string;
  geography?: string;
  number_of_leads: number;
  leads: Lead[];
}

export interface ProviderStatusResponse {
  active_provider: string;
  is_mock: boolean;
  has_groq: boolean;
  groq_model: string;
  has_database: boolean;
}
