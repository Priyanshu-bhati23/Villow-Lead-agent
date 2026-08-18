import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.config import settings
from app.models.schemas import (
    LeadGenerateRequest,
    LeadGenerateResponse,
    LeadResponse,
    ProviderStatusResponse
)
from app.agents.lead_agent import LeadAgent
from app.services.lead_service import LeadPersistenceService
from app.providers.factory import get_lead_provider
from app.llm.groq_client import groq_client
from app.villow.schemas import VillowJobRequest, VillowJobResponse
from app.villow.adapter import VillowAdapter

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@router.get("/api/providers/status", response_model=ProviderStatusResponse)
def get_provider_status():
    """Check active search provider status and Groq LLM availability."""
    provider = get_lead_provider()
    return ProviderStatusResponse(
        active_provider=provider.get_provider_name(),
        is_mock=provider.is_mock(),
        has_groq=groq_client.is_configured(),
        groq_model=settings.GROQ_MODEL,
        has_database=bool(settings.DATABASE_URL)
    )

@router.post("/api/leads/generate", response_model=LeadGenerateResponse, status_code=status.HTTP_200_OK)
def generate_leads(request: LeadGenerateRequest, db: Session = Depends(get_db)):
    """
    Main lead generation endpoint.
    Parses ICP, discovers real candidate companies, enriches signals, scores, ranks, and generates outreach.
    """
    if not request.icp or not request.icp.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ICP field cannot be empty."
        )

    logger.info(f"Received lead generation request: ICP='{request.icp[:50]}...', Industry='{request.industry}', Geography='{request.geography}', Count={request.number_of_leads}")

    try:
        agent = LeadAgent()
        pipeline_output = agent.run_pipeline(
            icp_prompt=request.icp,
            industry=request.industry,
            geography=request.geography,
            number_of_leads=request.number_of_leads
        )

        leads_data = pipeline_output.get("leads", [])
        if not leads_data:
            logger.warning("Lead generation pipeline returned 0 leads.")

        # Persist to Neon PostgreSQL database
        saved_response = LeadPersistenceService.save_lead_generation(
            db=db,
            icp=request.icp,
            industry=request.industry,
            geography=request.geography,
            number_of_leads=request.number_of_leads,
            leads_data=leads_data
        )

        return saved_response

    except Exception as e:
        logger.error(f"Error during lead generation execution: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing lead generation. Please verify provider status and inputs."
        )

@router.get("/api/requests/{request_id}", response_model=LeadGenerateResponse)
def get_request_by_id(request_id: str, db: Session = Depends(get_db)):
    """Fetch previously generated lead request results by request ID."""
    res = LeadPersistenceService.get_request_by_id(db, request_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request with ID '{request_id}' not found."
        )
    return res

@router.get("/api/leads/{lead_id}", response_model=LeadResponse)
def get_lead_by_id(lead_id: str, db: Session = Depends(get_db)):
    """Fetch specific lead details by lead ID."""
    res = LeadPersistenceService.get_lead_by_id(db, lead_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with ID '{lead_id}' not found."
        )
    return res

@router.post("/api/villow/job", response_model=VillowJobResponse)
def process_villow_job(job_request: VillowJobRequest, db: Session = Depends(get_db)):
    """
    Placeholder API endpoint for receiving Villow Founding Publisher Program jobs.
    Uses VillowAdapter to translate input and return structured responses.
    """
    logger.info(f"Received Villow Job execution request: job_id={job_request.job_id}")
    try:
        adapter = VillowAdapter()
        return adapter.process_job(job_request.model_dump(), db=db)
    except Exception as e:
        logger.error(f"Failed to process Villow job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute Villow job request."
        )
