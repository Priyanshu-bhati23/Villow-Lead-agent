from app.services.scoring_service import LeadScoringService
from app.models.schemas import ICPParseResult

def test_lead_scoring_algorithm():
    icp = ICPParseResult(
        industry="SaaS",
        geography="India",
        employee_range="50-500",
        required_signals=["funding", "hiring"],
        target_keywords=["analytics", "platform"]
    )

    company = {
        "company_name": "TestCorp AI",
        "website": "https://testcorp.ai",
        "description": "Enterprise SaaS analytics platform based in Bengaluru, India.",
        "industry": "SaaS",
        "location": "Bengaluru, India",
        "signals": [
            {"signal_type": "funding", "signal_text": "Raised $10M Series A", "source_url": "https://news.com/1"},
            {"signal_type": "hiring", "signal_text": "Hiring 10 engineers", "source_url": "https://jobs.com/1"}
        ]
    }

    res = LeadScoringService.calculate_score(company, icp)
    assert "total_score" in res
    assert 0 <= res["total_score"] <= 100
    breakdown = res["score_breakdown"]
    assert breakdown.icp_fit > 0
    assert breakdown.signal_strength > 0
    assert breakdown.signal_recency > 0
    assert breakdown.total == res["total_score"]
