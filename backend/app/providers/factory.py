import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models.schemas import ICPParseResult
from app.providers.base import BaseLeadProvider
from app.providers.search import WebSearchProvider
from app.providers.enrichment import DataEnrichmentProvider
from app.providers.mock import MockProvider

logger = logging.getLogger(__name__)

class RealLeadProvider(BaseLeadProvider):
    """Production provider leveraging WebSearchProvider and DataEnrichmentProvider."""

    def __init__(self, search_provider: WebSearchProvider, enrichment_provider: DataEnrichmentProvider):
        self.search_provider = search_provider
        self.enrichment_provider = enrichment_provider

    def get_provider_name(self) -> str:
        return "RealWebSearchProvider (Tavily/SerpAPI/WebSearch)"

    def is_mock(self) -> bool:
        return False

    def search_companies(self, icp: ICPParseResult, limit: int = 10) -> List[Dict[str, Any]]:
        return self.search_provider.extract_companies_from_search(icp, limit=limit)

    def enrich_company(self, raw_company: Dict[str, Any]) -> Dict[str, Any]:
        company_name = raw_company.get("company_name", "")
        website = raw_company.get("website", "")
        snippet = raw_company.get("snippet", raw_company.get("description", ""))
        source_url = raw_company.get("source_url", website)

        signals = self.enrichment_provider.enrich_company_signals(
            company_name=company_name,
            website=website,
            raw_snippet=snippet,
            source_url=source_url
        )

        raw_company["signals"] = signals
        return raw_company

def get_lead_provider(force_mock: bool = False) -> BaseLeadProvider:
    """Factory function returning active provider based on environment configuration."""
    if force_mock or not settings.SEARCH_API_KEY:
        logger.info("Using MockProvider (No SEARCH_API_KEY provided or forced mock mode).")
        return MockProvider()

    logger.info("Using RealLeadProvider with configured search API.")
    search_prov = WebSearchProvider()
    enrichment_prov = DataEnrichmentProvider(search_prov)
    return RealLeadProvider(search_prov, enrichment_prov)
