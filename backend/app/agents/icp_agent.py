import logging
from typing import Optional
from app.llm.groq_client import groq_client
from app.models.schemas import ICPParseResult

logger = logging.getLogger(__name__)

class ICPAgent:
    """Agent responsible for parsing natural language ICP descriptions into structured criteria."""

    def __init__(self, groq=groq_client):
        self.groq = groq

    def parse(self, icp_text: str, industry: Optional[str] = None, geography: Optional[str] = None) -> ICPParseResult:
        logger.info(f"ICPAgent parsing prompt: '{icp_text}'")
        parsed_result = self.groq.parse_icp(icp_text, industry, geography)
        logger.info(f"ICPAgent parsed result -> Industry: {parsed_result.industry}, Geo: {parsed_result.geography}, Signals: {parsed_result.required_signals}")
        return parsed_result
