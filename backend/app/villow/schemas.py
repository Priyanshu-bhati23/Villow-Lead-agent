from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class VillowJobRequest(BaseModel):
    """
    Placeholder schema for incoming Villow Founding Publisher Program job payload.
    NOTE: Replace this schema once official Villow SDK specification is released.
    """
    job_id: str = Field(..., description="Unique job identifier issued by Villow platform")
    icp_description: str = Field(..., description="Ideal customer profile prompt text")
    target_industry: Optional[str] = None
    target_geography: Optional[str] = None
    max_leads: int = 10
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class VillowJobResponse(BaseModel):
    """
    Placeholder schema for Villow Founding Publisher Program job execution output.
    NOTE: Replace this schema once official Villow SDK specification is released.
    """
    job_id: str
    status: str = "completed"  # completed, failed
    lead_count: int
    request_id: str
    results: List[Dict[str, Any]]
    error_message: Optional[str] = None
