import logging
import httpx
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from app.config import settings
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class WebSearchProvider:
    """Real search provider executing HTTP API queries against Tavily/SerpAPI/Generic search endpoints."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or settings.SEARCH_API_KEY
        self.api_url = api_url or settings.SEARCH_API_URL

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search_query(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform HTTP POST search query against configured search API."""
        if not self.is_configured():
            logger.warning("SEARCH_API_KEY is not set.")
            return []

        headers = {"Content-Type": "application/json"}
        
        # Format payload according to endpoint (Tavily standard API format)
        if "tavily" in self.api_url.lower():
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": min(limit * 2, 20),
                "search_depth": "advanced",
                "include_answer": False
            }
        else:
            # Generic REST Search API format
            payload = {
                "api_key": self.api_key,
                "query": query,
                "limit": limit
            }
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            with httpx.Client(timeout=12.0) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                results = []
                # Handle Tavily response layout
                raw_results = data.get("results", []) if isinstance(data, dict) else []
                for item in raw_results:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("content", item.get("snippet", "")),
                        "score": item.get("score", 0.0)
                    })
                return results
        except Exception as e:
            logger.error(f"HTTP Search API query failed: {e}")
            return []

    def extract_companies_from_search(self, icp: ICPParseResult, limit: int = 10) -> List[Dict[str, Any]]:
        query_parts = []
        if icp.industry:
            query_parts.append(icp.industry)
        if icp.geography:
            query_parts.append(f"companies in {icp.geography}")
        if icp.required_signals:
            query_parts.append(" ".join(icp.required_signals))
        query_parts.append("top startups OR fast growing tech companies")

        query = " ".join(query_parts)
        logger.info(f"Executing real web search query: '{query}'")

        search_results = self.search_query(query, limit=limit)
        
        discovered_companies: List[Dict[str, Any]] = []
        seen_domains = set()

        for item in search_results:
            url = item.get("url", "")
            domain = urlparse(url).netloc.replace("www.", "").lower()
            
            # Skip aggregator / generic directory sites
            if not domain or any(skip in domain for skip in ["google", "wikipedia", "linkedin", "techcrunch", "ycombinator", "glassdoor", "github", "twitter", "medium"]):
                continue

            if domain in seen_domains:
                continue
            seen_domains.add(domain)

            # Derive company name from domain or title
            title = item.get("title", "")
            name_match = title.split("-")[0].split("|")[0].split(":")[0].strip()
            company_name = name_match if len(name_match) > 1 and len(name_match) < 40 else domain.split(".")[0].capitalize()

            discovered_companies.append({
                "company_name": company_name,
                "website": f"https://{domain}",
                "description": item.get("snippet", f"{company_name} is a company operating in {icp.industry or 'the technology sector'}."),
                "industry": icp.industry or "Technology",
                "location": icp.geography or "India",
                "source_url": url,
                "snippet": item.get("snippet", "")
            })

            if len(discovered_companies) >= limit:
                break

        return discovered_companies
