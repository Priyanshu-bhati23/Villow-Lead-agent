import logging
from typing import Dict, Any, List
from app.llm.groq_client import groq_client
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class OutreachAgent:
    """Agent responsible for generating 'Why Good Lead', 'Why Now', and personalized outreach hooks."""

    def __init__(self, groq=groq_client):
        self.groq = groq

    def generate_reasons_and_hook(self, company: Dict[str, Any], icp: ICPParseResult) -> Dict[str, Any]:
        company_name = company.get("company_name", "")
        website = company.get("website", "")
        description = company.get("description", "")
        signals = company.get("signals", [])

        icp_dict = {
            "industry": icp.industry,
            "geography": icp.geography,
            "required_signals": icp.required_signals
        }

        reasoning = self.groq.analyze_lead_reasoning(
            company_name=company_name,
            website=website,
            description=description,
            signals=signals,
            icp_info=icp_dict
        )

        company["why_this_is_a_good_lead"] = reasoning.get("why_this_is_a_good_lead")
        company["why_now"] = reasoning.get("why_now")
        company["outreach_hook"] = reasoning.get("outreach_hook")

        return company
