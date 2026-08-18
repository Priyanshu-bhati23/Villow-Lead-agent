"""
========================================================================================
VILLOW ADAPTER (FOUNDING PUBLISHER PROGRAM)
========================================================================================
IMPORTANT NOTICE:
Replace this adapter implementation with the official Villow SDK integration once the
official Villow SDK specification and documentation are provided.

Do NOT invent actual Villow SDK methods or endpoints in this module.
========================================================================================
"""

import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.villow.schemas import VillowJobRequest, VillowJobResponse
from app.models.schemas import LeadGenerateRequest, LeadGenerateResponse
from app.agents.lead_agent import LeadAgent
from app.services.lead_service import LeadPersistenceService

logger = logging.getLogger(__name__)

class VillowAdapter:
    """
    Adapter bridging the Villow Founding Publisher Program job specifications with
    the core Lead Generation Agent pipeline.
    """

    def __init__(self, lead_agent: Optional[LeadAgent] = None):
        self.lead_agent = lead_agent or LeadAgent()

    def receive_villow_job(self, raw_job_payload: Dict[str, Any]) -> VillowJobRequest:
        """Parse raw incoming Villow payload into structured VillowJobRequest."""
        logger.info(f"VillowAdapter received job payload: {raw_job_payload.get('job_id')}")
        return VillowJobRequest(**raw_job_payload)

    def convert_to_internal_request(self, job_req: VillowJobRequest) -> LeadGenerateRequest:
        """Convert Villow input format to internal LeadGenerateRequest schema."""
        return LeadGenerateRequest(
            icp=job_req.icp_description,
            industry=job_req.target_industry,
            geography=job_req.target_geography,
            number_of_leads=job_req.max_leads
        )

    def run_lead_generation_workflow(
        self,
        internal_req: LeadGenerateRequest,
        db: Optional[Session] = None
    ) -> LeadGenerateResponse:
        """Execute core pipeline and optionally persist results."""
        pipeline_output = self.lead_agent.run_pipeline(
            icp_prompt=internal_req.icp,
            industry=internal_req.industry,
            geography=internal_req.geography,
            number_of_leads=internal_req.number_of_leads
        )

        leads_data = pipeline_output["leads"]

        if db is not None:
            return LeadPersistenceService.save_lead_generation(
                db=db,
                icp=internal_req.icp,
                industry=internal_req.industry,
                geography=internal_req.geography,
                number_of_leads=internal_req.number_of_leads,
                leads_data=leads_data
            )
        else:
            # Non-persisted transient response
            from app.models.schemas import LeadResponse, ScoreBreakdown, SignalSchema
            lead_responses = []
            for comp in leads_data:
                sb_data = comp.get("score_breakdown", {})
                sb = ScoreBreakdown(**sb_data) if isinstance(sb_data, dict) else ScoreBreakdown()
                signals = [SignalSchema(**s) for s in comp.get("signals", [])]
                lead_responses.append(LeadResponse(
                    company_name=comp.get("company_name", "Unknown"),
                    website=comp.get("website"),
                    description=comp.get("description"),
                    industry=comp.get("industry"),
                    location=comp.get("location"),
                    signals=signals,
                    sources=[comp.get("source_url")] if comp.get("source_url") else [],
                    score=comp.get("score", 0),
                    score_breakdown=sb,
                    why_this_is_a_good_lead=comp.get("why_this_is_a_good_lead"),
                    why_now=comp.get("why_now"),
                    outreach_hook=comp.get("outreach_hook")
                ))

            return LeadGenerateResponse(
                request_id="transient-villow-req",
                icp=internal_req.icp,
                industry=internal_req.industry,
                geography=internal_req.geography,
                number_of_leads=internal_req.number_of_leads,
                leads=lead_responses
            )

    def convert_to_villow_response(
        self,
        job_id: str,
        gen_res: LeadGenerateResponse
    ) -> VillowJobResponse:
        """Convert internal LeadGenerateResponse into structured VillowJobResponse format."""
        results = [lead.model_dump() for lead in gen_res.leads]
        return VillowJobResponse(
            job_id=job_id,
            status="completed",
            lead_count=len(results),
            request_id=gen_res.request_id,
            results=results
        )

    def process_job(self, raw_job_payload: Dict[str, Any], db: Optional[Session] = None) -> VillowJobResponse:
        """Full end-to-end execution helper for Villow jobs."""
        job_req = self.receive_villow_job(raw_job_payload)
        internal_req = self.convert_to_internal_request(job_req)
        gen_res = self.run_lead_generation_workflow(internal_req, db=db)
        return self.convert_to_villow_response(job_req.job_id, gen_res)
