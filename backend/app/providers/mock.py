import logging
from typing import List, Dict, Any
from app.providers.base import BaseLeadProvider
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class MockProvider(BaseLeadProvider):
    """
    Universal Mock lead provider utilized when SEARCH_API_KEY is not configured or in unit test mode.
    Provides realistic B2B company profiles across ALL major industries (Healthcare, Manufacturing, E-Commerce, Real Estate, Fintech, SaaS).
    """

    MOCK_COMPANIES = [
        {
            "company_name": "PerfStack AI",
            "website": "https://perfstack.io",
            "description": "B2B SaaS application performance monitoring platform tailored for microservices and cloud infrastructure.",
            "industry": "SaaS & Technology",
            "location": "Bengaluru, India",
            "source_url": "https://perfstack.io/about",
            "signals": [
                {
                    "signal_type": "funding",
                    "signal_text": "PerfStack AI raised $12M Series A led by Peak XV Partners.",
                    "source_url": "https://techcrunch.com/perfstack-series-a"
                },
                {
                    "signal_type": "hiring",
                    "signal_text": "Currently hiring 12 backend & AI infrastructure engineers.",
                    "source_url": "https://perfstack.io/careers"
                }
            ]
        },
        {
            "company_name": "BioHealth Diagnostics",
            "website": "https://biohealthdiag.com",
            "description": "AI-powered molecular diagnostics and clinical laboratory solutions provider expanding diagnostic centers across Asia.",
            "industry": "Healthcare & Biotech",
            "location": "Mumbai, India",
            "source_url": "https://biohealthdiag.com",
            "signals": [
                {
                    "signal_type": "expansion",
                    "signal_text": "Received FDA ISO-13485 certification and opened 5 new regional diagnostic centers.",
                    "source_url": "https://healthjournal.com/biohealth-expansion"
                },
                {
                    "signal_type": "hiring",
                    "signal_text": "Actively recruiting Medical Directors and Laboratory Operations Specialists.",
                    "source_url": "https://biohealthdiag.com/careers"
                }
            ]
        },
        {
            "company_name": "Apex Precision Manufacturing",
            "website": "https://apexprecision.tech",
            "description": "Automotive and aerospace component precision machining facility specializing in electric vehicle power units.",
            "industry": "Manufacturing & Industrial",
            "location": "Pune, India",
            "source_url": "https://apexprecision.tech",
            "signals": [
                {
                    "signal_type": "expansion",
                    "signal_text": "Commissioned a new 100,000 sq ft automated manufacturing plant in Pune Industrial Corridor.",
                    "source_url": "https://economictimes.com/apex-new-plant"
                },
                {
                    "signal_type": "hiring",
                    "signal_text": "Posted open requisitions for Plant Operations Managers & Quality Assurance Engineers.",
                    "source_url": "https://apexprecision.tech/jobs"
                }
            ]
        },
        {
            "company_name": "UrbanBlend D2C Brands",
            "website": "https://urbanblend.in",
            "description": "Fast-growing D2C consumer goods brand specializing in sustainable personal care and organic lifestyle products.",
            "industry": "E-Commerce & Retail",
            "location": "Gurugram, India",
            "source_url": "https://urbanblend.in",
            "signals": [
                {
                    "signal_type": "funding",
                    "signal_text": "Secured $8M Series A funding to expand retail footprint and D2C supply chain.",
                    "source_url": "https://inc42.com/urbanblend-series-a"
                },
                {
                    "signal_type": "hiring",
                    "signal_text": "Recruiting Vice President of Marketing and Performance Marketing Managers.",
                    "source_url": "https://urbanblend.in/careers"
                }
            ]
        },
        {
            "company_name": "Skyline Urban Developers",
            "website": "https://skylinedev.com",
            "description": "Commercial real estate development firm building sustainable LEED-certified office parks and mixed-use complexes.",
            "industry": "Real Estate & Construction",
            "location": "Hyderabad, India",
            "source_url": "https://skylinedev.com",
            "signals": [
                {
                    "signal_type": "expansion",
                    "signal_text": "Broke ground on a 2 Million sq ft Grade-A Commercial Tech Park project.",
                    "source_url": "https://realestatemonitor.com/skyline-tech-park"
                },
                {
                    "signal_type": "hiring",
                    "signal_text": "Hiring Senior Project Architects & Procurement Directors.",
                    "source_url": "https://skylinedev.com/careers"
                }
            ]
        },
        {
            "company_name": "DevPulse Analytics",
            "website": "https://devpulse.dev",
            "description": "Developer productivity intelligence and engineering workflow automation software.",
            "industry": "SaaS & Technology",
            "location": "Bengaluru, India",
            "source_url": "https://devpulse.dev",
            "signals": [
                {
                    "signal_type": "funding",
                    "signal_text": "DevPulse raised $5.5M Seed round to expand product team.",
                    "source_url": "https://yourstory.com/devpulse-funding"
                }
            ]
        }
    ]

    def get_provider_name(self) -> str:
        return "UniversalMockProvider (Multi-Industry Local Dev & Test Fallback)"

    def is_mock(self) -> bool:
        return True

    def search_companies(self, icp: ICPParseResult, limit: int = 10) -> List[Dict[str, Any]]:
        logger.info(f"[UniversalMockProvider] Returning candidates across industry: '{icp.industry}' in region: '{icp.geography}'")
        
        results = []
        icp_ind_lower = (icp.industry or "").lower()

        # Prioritize matching industry records, then fallback to general list
        matching_companies = [
            c for c in self.MOCK_COMPANIES 
            if icp_ind_lower in c["industry"].lower() or any(term in c["industry"].lower() for term in icp_ind_lower.split())
        ]
        
        non_matching = [c for c in self.MOCK_COMPANIES if c not in matching_companies]
        ordered_candidates = matching_companies + non_matching

        for company in ordered_candidates:
            comp_copy = dict(company)
            # Adapt location if geography explicitly passed
            if icp.geography and "global" not in icp.geography.lower() and icp.geography.lower() not in comp_copy["location"].lower():
                comp_copy["location"] = f"{comp_copy['location'].split(',')[0]}, {icp.geography}"
            
            results.append(comp_copy)

        return results[:limit]

    def enrich_company(self, raw_company: Dict[str, Any]) -> Dict[str, Any]:
        return raw_company
