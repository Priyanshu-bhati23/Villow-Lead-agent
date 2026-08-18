from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ICPParseResult(BaseModel):
    industry: Optional[str] = None
    geography: Optional[str] = None
    employee_range: Optional[str] = None
    required_signals: List[str] = Field(default_factory=list)
    target_keywords: List[str] = Field(default_factory=list)

class LeadGenerateRequest(BaseModel):
    icp: str = Field(..., description="Ideal Customer Profile prompt text")
    industry: Optional[str] = Field(None, description="Industry override or filter")
    geography: Optional[str] = Field(None, description="Geography override or filter")
    number_of_leads: int = Field(10, ge=1, le=50, description="Target lead count")

class SignalSchema(BaseModel):
    id: Optional[str] = None
    signal_type: str  # funding, hiring, technology, job_posting
    signal_text: str
    source_url: Optional[str] = None
    detected_at: Optional[str] = None

class ScoreBreakdown(BaseModel):
    icp_fit: int = 0          # Max 30
    signal_strength: int = 0  # Max 25
    signal_recency: int = 0   # Max 20
    company_relevance: int = 0# Max 15
    data_confidence: int = 0  # Max 10

    @property
    def total(self) -> int:
        return self.icp_fit + self.signal_strength + self.signal_recency + self.company_relevance + self.data_confidence

class LeadResponse(BaseModel):
    id: Optional[str] = None
    company_name: str
    website: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    signals: List[SignalSchema] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    score: int = 0
    score_breakdown: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    why_this_is_a_good_lead: Optional[str] = None
    why_now: Optional[str] = None
    outreach_hook: Optional[str] = None
    created_at: Optional[str] = None

class LeadGenerateResponse(BaseModel):
    request_id: str
    icp: str
    industry: Optional[str] = None
    geography: Optional[str] = None
    number_of_leads: int
    leads: List[LeadResponse] = Field(default_factory=list)

class ProviderStatusResponse(BaseModel):
    active_provider: str
    is_mock: bool
    has_groq: bool
    groq_model: str
    has_database: bool
