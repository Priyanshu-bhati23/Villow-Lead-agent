from app.providers.mock import MockProvider
from app.models.schemas import ICPParseResult
from app.agents.lead_agent import LeadAgent

def test_mock_provider_returns_companies():
    provider = MockProvider()
    icp = ICPParseResult(industry="SaaS", geography="India")
    companies = provider.search_companies(icp, limit=3)
    assert len(companies) == 3
    assert provider.is_mock() is True

def test_duplicate_removal_in_lead_agent():
    agent = LeadAgent(force_mock=True)
    res = agent.run_pipeline("Find SaaS companies in India", number_of_leads=5)
    leads = res["leads"]
    domains = [l.get("website") for l in leads if l.get("website")]
    assert len(domains) == len(set(domains)), "Pipeline must deduplicate companies by domain."
