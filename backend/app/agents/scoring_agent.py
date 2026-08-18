import logging
from typing import Dict, Any, List
from app.services.scoring_service import LeadScoringService
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class ScoringAgent:
    """Agent responsible for lead qualification, transparent scoring (0-100), and ranking."""

    def __init__(self, scoring_service=LeadScoringService):
        self.scoring_service = scoring_service

    def score_company(self, company: Dict[str, Any], icp: ICPParseResult) -> Dict[str, Any]:
        scored_res = self.scoring_service.calculate_score(company, icp)
        company["score"] = scored_res["total_score"]
        company["score_breakdown"] = scored_res["score_breakdown"]
        return company

    def rank_companies(self, companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank companies in descending order of score."""
        sorted_companies = sorted(companies, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_companies
