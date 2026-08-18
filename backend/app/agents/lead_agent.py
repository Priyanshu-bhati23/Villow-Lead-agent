import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from app.agents.icp_agent import ICPAgent
from app.agents.scoring_agent import ScoringAgent
from app.agents.outreach_agent import OutreachAgent
from app.providers.factory import get_lead_provider
from app.models.schemas import ICPParseResult, LeadResponse, SignalSchema, ScoreBreakdown

logger = logging.getLogger(__name__)

class LeadAgent:
    """Master orchestrator agent coordinating ICP parsing, discovery, enrichment, scoring, and outreach generation."""

    def __init__(self, force_mock: bool = False):
        self.icp_agent = ICPAgent()
        self.scoring_agent = ScoringAgent()
        self.outreach_agent = OutreachAgent()
        self.provider = get_lead_provider(force_mock=force_mock)

    def run_pipeline(
        self,
        icp_prompt: str,
        industry: Optional[str] = None,
        geography: Optional[str] = None,
        number_of_leads: int = 10
    ) -> Dict[str, Any]:
        logger.info(f"Starting Lead Generation pipeline for prompt: '{icp_prompt}', count: {number_of_leads}")

        # 1. Parse ICP
        parsed_icp: ICPParseResult = self.icp_agent.parse(icp_prompt, industry, geography)

        # 2. Discover companies using search provider
        raw_companies = self.provider.search_companies(parsed_icp, limit=number_of_leads)
        logger.info(f"Discovered {len(raw_companies)} raw company candidates.")

        # 3. Remove duplicates by domain / normalized name
        unique_companies: List[Dict[str, Any]] = []
        seen_domains = set()
        seen_names = set()

        for comp in raw_companies:
            name_norm = comp.get("company_name", "").strip().lower()
            url = comp.get("website", "")
            domain = urlparse(url).netloc.replace("www.", "").lower() if url else name_norm

            if domain in seen_domains or name_norm in seen_names:
                logger.info(f"Filtering duplicate company: {comp.get('company_name')}")
                continue

            seen_domains.add(domain)
            seen_names.add(name_norm)
            unique_companies.append(comp)

        # 4. Enrich each company with signals & sources
        enriched_companies = []
        for comp in unique_companies:
            enriched = self.provider.enrich_company(comp)
            enriched_companies.append(enriched)

        # 5. Score companies (0-100)
        scored_companies = []
        for comp in enriched_companies:
            scored = self.scoring_agent.score_company(comp, parsed_icp)
            scored_companies.append(scored)

        # 6. Rank companies by score
        ranked_companies = self.scoring_agent.rank_companies(scored_companies)

        # Limit to requested lead count
        selected_leads = ranked_companies[:number_of_leads]

        # 7. Generate Why Good, Why Now, and Outreach Hooks
        final_leads: List[Dict[str, Any]] = []
        for comp in selected_leads:
            with_outreach = self.outreach_agent.generate_reasons_and_hook(comp, parsed_icp)
            final_leads.append(with_outreach)

        logger.info(f"Pipeline complete. Generated {len(final_leads)} ranked leads.")

        return {
            "parsed_icp": parsed_icp,
            "leads": final_leads
        }
