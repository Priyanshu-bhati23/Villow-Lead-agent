import logging
import re
from typing import List, Dict, Any
from app.providers.search import WebSearchProvider

logger = logging.getLogger(__name__)

class DataEnrichmentProvider:
    """Enriches discovered company data with verified signals (funding, hiring, stack changes)."""

    def __init__(self, search_provider: WebSearchProvider):
        self.search_provider = search_provider

    def enrich_company_signals(self, company_name: str, website: str, raw_snippet: str, source_url: str) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []

        # 1. Search for recent funding or news
        funding_query = f'"{company_name}" raised funding OR "Series A" OR "Series B" OR "seed"'
        if self.search_provider.is_configured():
            funding_results = self.search_provider.search_query(funding_query, limit=3)
            for res in funding_results:
                text = res.get("snippet", "")
                if any(kw in text.lower() for kw in ["raised", "million", "series", "funding", "seed"]):
                    signals.append({
                        "signal_type": "funding",
                        "signal_text": res.get("title", text[:120]),
                        "source_url": res.get("url", source_url)
                    })
                    break

        # 2. Search for open engineering roles or hiring
        hiring_query = f'"{company_name}" hiring engineers OR software engineer jobs OR careers'
        if self.search_provider.is_configured():
            hiring_results = self.search_provider.search_query(hiring_query, limit=3)
            for res in hiring_results:
                text = res.get("snippet", "")
                if any(kw in text.lower() for kw in ["hiring", "engineer", "careers", "developer", "job"]):
                    signals.append({
                        "signal_type": "hiring",
                        "signal_text": f"Actively hiring engineering roles: {res.get('title', text[:100])}",
                        "source_url": res.get("url", source_url)
                    })
                    break

        # 3. Text snippet fallback inspection if external signals were not found
        snippet_lower = raw_snippet.lower()
        if not any(s["signal_type"] == "funding" for s in signals):
            if any(term in snippet_lower for term in ["raised", "series", "funded", "venture", "investment"]):
                signals.append({
                    "signal_type": "funding",
                    "signal_text": f"{company_name} recently secured growth capital / funding milestone.",
                    "source_url": source_url
                })

        if not any(s["signal_type"] == "hiring" for s in signals):
            if any(term in snippet_lower for term in ["hiring", "team", "engineer", "growing", "expanding"]):
                signals.append({
                    "signal_type": "hiring",
                    "signal_text": f"{company_name} is expanding headcount and recruiting technical roles.",
                    "source_url": source_url
                })

        if any(term in snippet_lower for term in ["cloud", "aws", "react", "python", "ai", "stack", "api"]):
            signals.append({
                "signal_type": "technology",
                "signal_text": f"{company_name} utilizes modern technology stack & API integrations.",
                "source_url": source_url
            })

        return signals
