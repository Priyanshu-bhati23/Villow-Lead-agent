import json
import logging
import re
from typing import Dict, Any, Optional, List
from groq import Groq
from app.config import settings
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")

    def is_configured(self) -> bool:
        return self.client is not None and bool(self.api_key)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON object from model text response."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            match_obj = re.search(r"(\{.*\})", text, re.DOTALL)
            if match_obj:
                try:
                    return json.loads(match_obj.group(1))
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Could not parse valid JSON from LLM output: {text[:200]}")

    def parse_icp(self, icp_prompt: str, industry: Optional[str] = None, geography: Optional[str] = None) -> ICPParseResult:
        """Parse natural language ICP prompt into structured parameters across any domain/industry."""
        if not self.is_configured():
            logger.info("Groq API key not configured. Using rule-based fallback for universal ICP parsing.")
            return self._heuristic_parse_icp(icp_prompt, industry, geography)

        system_prompt = (
            "You are an expert universal B2B lead generation AI. Parse the user's Ideal Customer Profile (ICP) "
            "description across ANY industry (Healthcare, E-Commerce, Manufacturing, Real Estate, Legal, Fintech, SaaS, Education, etc.).\n"
            "Extract industry, geography, company size/scale, required buying signals (e.g. funding, hiring, new factory opening, FDA approval, M&A, leadership changes), "
            "and target search keywords.\n"
            "Return JSON matching exact schema:\n"
            "{\n"
            '  "industry": "string or null",\n'
            '  "geography": "string or null",\n'
            '  "employee_range": "string or null",\n'
            '  "required_signals": ["string"],\n'
            '  "target_keywords": ["string"]\n'
            "}\n"
            "Do not restrict yourself to technology; support all business domains."
        )

        user_content = f"ICP Prompt: {icp_prompt}\nExplicit Industry: {industry or 'N/A'}\nExplicit Geography: {geography or 'N/A'}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            raw_content = response.choices[0].message.content
            parsed = self._extract_json(raw_content)

            return ICPParseResult(
                industry=parsed.get("industry") or industry or "General B2B",
                geography=parsed.get("geography") or geography or "Global",
                employee_range=parsed.get("employee_range"),
                required_signals=parsed.get("required_signals", []),
                target_keywords=parsed.get("target_keywords", [])
            )
        except Exception as e:
            logger.error(f"Groq API call for parse_icp failed: {e}. Falling back to universal heuristic parsing.")
            return self._heuristic_parse_icp(icp_prompt, industry, geography)

    def _heuristic_parse_icp(self, icp: str, industry: Optional[str], geography: Optional[str]) -> ICPParseResult:
        icp_lower = icp.lower()
        
        # Universal Industry Detection
        detected_ind = industry
        if not detected_ind:
            if any(k in icp_lower for k in ["health", "bio", "pharma", "clinic", "hospital", "medical"]):
                detected_ind = "Healthcare & Biotech"
            elif any(k in icp_lower for k in ["e-commerce", "ecommerce", "d2c", "retail", "brand"]):
                detected_ind = "E-Commerce & Retail"
            elif any(k in icp_lower for k in ["manufactur", "industrial", "factory", "plant", "machinery"]):
                detected_ind = "Manufacturing & Industrial"
            elif any(k in icp_lower for k in ["real estate", "construction", "property", "developer", "architect"]):
                detected_ind = "Real Estate & Construction"
            elif any(k in icp_lower for k in ["fintech", "bank", "finance", "wealth", "insur"]):
                detected_ind = "Fintech & Financial Services"
            elif any(k in icp_lower for k in ["legal", "law", "attorney", "consulting", "accounting"]):
                detected_ind = "Legal & Professional Services"
            elif any(k in icp_lower for k in ["edtech", "school", "education", "university"]):
                detected_ind = "Education & EdTech"
            elif "saas" in icp_lower or "software" in icp_lower or "tech" in icp_lower:
                detected_ind = "SaaS & Technology"
            else:
                detected_ind = "Commercial B2B"

        # Geography Detection
        detected_geo = geography
        if not detected_geo:
            if "india" in icp_lower:
                detected_geo = "India"
            elif any(k in icp_lower for k in ["us", "united states", "america", "california", "texas", "new york"]):
                detected_geo = "United States"
            elif any(k in icp_lower for k in ["europe", "uk", "germany", "france", "london"]):
                detected_geo = "Europe"
            elif any(k in icp_lower for k in ["asia", "singapore", "dubai", "uae"]):
                detected_geo = "Asia-Pacific / Middle East"
            else:
                detected_geo = "Global"

        # Scale / Size Range
        match_emp = re.search(r"(\d+[\s\-\+]+\d*|\d+\+)\s*(?:employees|people|staff|bed|revenue)?", icp_lower)
        emp_range = match_emp.group(1) if match_emp else "50-500"

        # Universal Signals Detection
        signals = []
        if any(k in icp_lower for k in ["fund", "series", "raised", "capital", "seed", "invest"]):
            signals.append("recent funding / capital raise")
        if any(k in icp_lower for k in ["hir", "recruit", "expand", "headcount", "roles"]):
            signals.append("active hiring / team expansion")
        if any(k in icp_lower for k in ["factory", "plant", "office", "store", "expansion"]):
            signals.append("facility & physical expansion")
        if any(k in icp_lower for k in ["approval", "fda", "iso", "license", "compliance"]):
            signals.append("regulatory approval / compliance milestone")
        if any(k in icp_lower for k in ["launch", "product", "acquisition", "m&a", "partnership"]):
            signals.append("product launch / strategic milestone")

        keywords = [word for word in icp.split() if len(word) > 4 and word.lower() not in {"companies", "in", "with", "that", "and", "are", "from", "looking"}]

        return ICPParseResult(
            industry=detected_ind,
            geography=detected_geo,
            employee_range=emp_range,
            required_signals=signals,
            target_keywords=keywords[:6]
        )

    def analyze_lead_reasoning(
        self,
        company_name: str,
        website: str,
        description: str,
        signals: List[Dict[str, Any]],
        icp_info: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate verifiable explanations across any business domain: Why good lead, Why now, and Outreach hook."""
        if not self.is_configured():
            return self._heuristic_lead_reasoning(company_name, signals, icp_info)

        system_prompt = (
            "You are an elite universal B2B growth strategist. Based strictly on the provided company facts and signals, "
            "generate three concise fields in JSON format for ANY industry (Healthcare, E-Commerce, Manufacturing, Real Estate, SaaS, etc.):\n"
            "1. 'why_this_is_a_good_lead': Explanation of why this company matches the target ICP criteria.\n"
            "2. 'why_now': Explanation of why the company is warm RIGHT NOW based on recent signals (funding, hiring, facility expansion, FDA approval, product launch, M&A).\n"
            "3. 'outreach_hook': A highly personalized, non-spammy outreach opening line citing specific real facts.\n\n"
            "IMPORTANT CRITICAL RULES:\n"
            "- Do NOT invent facts not present in the input context.\n"
            "- If evidence for recent signals is missing, write 'Not available' for why_now.\n"
            "- Return exact JSON object with keys: 'why_this_is_a_good_lead', 'why_now', 'outreach_hook'."
        )

        user_content = json.dumps({
            "company_name": company_name,
            "website": website,
            "description": description,
            "signals": signals,
            "icp_criteria": icp_info
        }, indent=2)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            raw_content = response.choices[0].message.content
            parsed = self._extract_json(raw_content)
            return {
                "why_this_is_a_good_lead": parsed.get("why_this_is_a_good_lead") or f"Strong fit operating in {icp_info.get('industry', 'target domain')} in {icp_info.get('geography', 'target region')}.",
                "why_now": parsed.get("why_now") or "Not available",
                "outreach_hook": parsed.get("outreach_hook") or f"Hi, noticed {company_name}'s recent operational momentum in {icp_info.get('industry', 'your market')}..."
            }
        except Exception as e:
            logger.error(f"Groq API call for analyze_lead_reasoning failed: {e}")
            return self._heuristic_lead_reasoning(company_name, signals, icp_info)

    def _heuristic_lead_reasoning(self, company_name: str, signals: List[Dict[str, Any]], icp_info: Dict[str, Any]) -> Dict[str, str]:
        signal_texts = [s.get("signal_text", "") for s in signals]
        funding_sig = next((s for s in signal_texts if any(k in s.lower() for k in ["raised", "funding", "series", "capital", "seed", "invest"])), None)
        hiring_sig = next((s for s in signal_texts if any(k in s.lower() for k in ["hiring", "job", "recruiting", "director", "manager", "vp", "head"])), None)
        expansion_sig = next((s for s in signal_texts if any(k in s.lower() for k in ["plant", "factory", "office", "fda", "product", "launched", "store"])), None)

        why_good = f"Strong ICP match operating in {icp_info.get('industry', 'target sector')} with matching location ({icp_info.get('geography', 'Global')})."
        
        if expansion_sig:
            why_now = f"Recent operational milestone: {expansion_sig}."
            hook = f"Saw that {company_name} recently achieved a key milestone: '{expansion_sig}'. This operational shift makes this a timely opportunity to connect."
        elif funding_sig and hiring_sig:
            why_now = f"Company recently {funding_sig.lower()} and is currently {hiring_sig.lower()}, signaling active expansion."
            hook = f"Congrats on {company_name}'s recent momentum ({funding_sig.lower()}) and team expansion ({hiring_sig.lower()}). That trajectory makes this a great moment to explore synergy."
        elif funding_sig:
            why_now = f"Recent capital milestone detected: {funding_sig}."
            hook = f"Noticed {company_name}'s recent capital milestone ({funding_sig}). Growth trajectory makes this a compelling time to connect."
        elif hiring_sig:
            why_now = f"Active hiring and talent acquisition detected: {hiring_sig}."
            hook = f"Noticed {company_name} is actively expanding key roles ({hiring_sig}). As you scale operations, wanted to share..."
        else:
            why_now = "Not available"
            hook = f"Noticed {company_name}'s work in {icp_info.get('industry', 'the market')}. Would love to explore how we support companies in your growth phase."

        return {
            "why_this_is_a_good_lead": why_good,
            "why_now": why_now,
            "outreach_hook": hook
        }

groq_client = GroqClient()
