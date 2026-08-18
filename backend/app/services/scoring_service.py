from typing import Dict, Any, List
from app.models.schemas import ScoreBreakdown, ICPParseResult

class LeadScoringService:
    """Calculates transparent, deterministic lead score (0-100) and breakdown metrics."""

    @staticmethod
    def calculate_score(company: Dict[str, Any], icp: ICPParseResult) -> Dict[str, Any]:
        industry = (company.get("industry") or "").lower()
        location = (company.get("location") or "").lower()
        description = (company.get("description") or "").lower()
        signals: List[Dict[str, Any]] = company.get("signals", [])
        website = company.get("website", "")

        # 1. ICP Fit (Max 30)
        icp_fit = 10  # Base
        if icp.industry and icp.industry.lower() in industry:
            icp_fit += 10
        elif "saas" in industry or "tech" in industry:
            icp_fit += 6

        if icp.geography and (icp.geography.lower() in location or "global" in icp.geography.lower()):
            icp_fit += 10
        elif "india" in location:
            icp_fit += 8

        icp_fit = min(30, icp_fit)

        # 2. Signal Strength (Max 25)
        # Funding = 15, Hiring = 10, Stack/Posting = 5
        signal_strength = 0
        has_funding = any(s.get("signal_type") == "funding" for s in signals)
        has_hiring = any(s.get("signal_type") in ["hiring", "job_posting"] for s in signals)
        has_tech = any(s.get("signal_type") == "technology" for s in signals)

        if has_funding:
            signal_strength += 15
        if has_hiring:
            signal_strength += 10
        if has_tech:
            signal_strength += 5

        # If no signals extracted yet, base points if company description indicates growth
        if not signals and ("fund" in description or "hir" in description):
            signal_strength = 12

        signal_strength = min(25, signal_strength)

        # 3. Signal Recency (Max 20)
        # Fresh funding or active open jobs boost recency points
        signal_recency = 10  # Default base recency
        if has_funding and has_hiring:
            signal_recency = 20
        elif has_funding or has_hiring:
            signal_recency = 16
        elif len(signals) > 0:
            signal_recency = 14

        signal_recency = min(20, signal_recency)

        # 4. Company Relevance (Max 15)
        company_relevance = 5
        if icp.target_keywords:
            matches = sum(1 for kw in icp.target_keywords if kw.lower() in description or kw.lower() in industry)
            company_relevance += min(10, matches * 3)
        else:
            company_relevance += 8

        company_relevance = min(15, company_relevance)

        # 5. Data Confidence (Max 10)
        data_confidence = 4
        if website and website.startswith("http"):
            data_confidence += 3
        if any(s.get("source_url") for s in signals):
            data_confidence += 3

        data_confidence = min(10, data_confidence)

        breakdown = ScoreBreakdown(
            icp_fit=icp_fit,
            signal_strength=signal_strength,
            signal_recency=signal_recency,
            company_relevance=company_relevance,
            data_confidence=data_confidence
        )

        total_score = breakdown.total

        return {
            "total_score": total_score,
            "score_breakdown": breakdown
        }
