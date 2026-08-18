import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database.models import LeadGenerationRequest, Lead, LeadSignal
from app.models.schemas import LeadResponse, SignalSchema, ScoreBreakdown, LeadGenerateResponse

logger = logging.getLogger(__name__)

class LeadPersistenceService:
    """Handles SQLAlchemy persistence for requests, leads, and signals."""

    @staticmethod
    def save_lead_generation(
        db: Session,
        icp: str,
        industry: Optional[str],
        geography: Optional[str],
        number_of_leads: int,
        leads_data: List[Dict[str, Any]]
    ) -> LeadGenerateResponse:
        # Create LeadGenerationRequest record
        req = LeadGenerationRequest(
            icp=icp,
            industry=industry,
            geography=geography,
            number_of_leads=number_of_leads
        )
        db.add(req)
        db.flush()  # populate req.id

        saved_lead_responses: List[LeadResponse] = []

        for comp in leads_data:
            breakdown_dict = comp.get("score_breakdown")
            if isinstance(breakdown_dict, ScoreBreakdown):
                json_breakdown = breakdown_dict.model_dump()
            elif isinstance(breakdown_dict, dict):
                json_breakdown = breakdown_dict
            else:
                json_breakdown = {}

            lead_db = Lead(
                request_id=req.id,
                company_name=comp.get("company_name", "Unknown"),
                website=comp.get("website"),
                description=comp.get("description"),
                industry=comp.get("industry"),
                location=comp.get("location"),
                score=comp.get("score", 0),
                score_breakdown=json_breakdown,
                why_this_is_a_good_lead=comp.get("why_this_is_a_good_lead"),
                why_now=comp.get("why_now"),
                outreach_hook=comp.get("outreach_hook")
            )
            db.add(lead_db)
            db.flush()

            # Save signals
            signal_responses: List[SignalSchema] = []
            sources_set = set()
            if comp.get("source_url"):
                sources_set.add(comp.get("source_url"))

            for sig in comp.get("signals", []):
                sig_db = LeadSignal(
                    lead_id=lead_db.id,
                    signal_type=sig.get("signal_type", "general"),
                    signal_text=sig.get("signal_text", ""),
                    source_url=sig.get("source_url")
                )
                db.add(sig_db)
                db.flush()

                if sig.get("source_url"):
                    sources_set.add(sig.get("source_url"))

                signal_responses.append(SignalSchema(
                    id=sig_db.id,
                    signal_type=sig_db.signal_type,
                    signal_text=sig_db.signal_text,
                    source_url=sig_db.source_url,
                    detected_at=sig_db.detected_at.isoformat() if sig_db.detected_at else None
                ))

            # Build LeadResponse
            sb = ScoreBreakdown(**json_breakdown) if json_breakdown else ScoreBreakdown()
            saved_lead_responses.append(LeadResponse(
                id=lead_db.id,
                company_name=lead_db.company_name,
                website=lead_db.website,
                description=lead_db.description,
                industry=lead_db.industry,
                location=lead_db.location,
                signals=signal_responses,
                sources=list(sources_set),
                score=lead_db.score,
                score_breakdown=sb,
                why_this_is_a_good_lead=lead_db.why_this_is_a_good_lead,
                why_now=lead_db.why_now,
                outreach_hook=lead_db.outreach_hook,
                created_at=lead_db.created_at.isoformat() if lead_db.created_at else None
            ))

        db.commit()
        logger.info(f"Persisted request {req.id} with {len(saved_lead_responses)} leads to DB.")

        return LeadGenerateResponse(
            request_id=req.id,
            icp=req.icp,
            industry=req.industry,
            geography=req.geography,
            number_of_leads=req.number_of_leads,
            leads=saved_lead_responses
        )

    @staticmethod
    def get_request_by_id(db: Session, request_id: str) -> Optional[LeadGenerateResponse]:
        req = db.query(LeadGenerationRequest).filter(LeadGenerationRequest.id == request_id).first()
        if not req:
            return None

        lead_responses: List[LeadResponse] = []
        for lead in req.leads:
            signals = []
            sources = set()
            if lead.website:
                sources.add(lead.website)

            for sig in lead.signals:
                signals.append(SignalSchema(
                    id=sig.id,
                    signal_type=sig.signal_type,
                    signal_text=sig.signal_text,
                    source_url=sig.source_url,
                    detected_at=sig.detected_at.isoformat() if sig.detected_at else None
                ))
                if sig.source_url:
                    sources.add(sig.source_url)

            sb_data = lead.score_breakdown if isinstance(lead.score_breakdown, dict) else {}
            sb = ScoreBreakdown(**sb_data) if sb_data else ScoreBreakdown()

            lead_responses.append(LeadResponse(
                id=lead.id,
                company_name=lead.company_name,
                website=lead.website,
                description=lead.description,
                industry=lead.industry,
                location=lead.location,
                signals=signals,
                sources=list(sources),
                score=lead.score,
                score_breakdown=sb,
                why_this_is_a_good_lead=lead.why_this_is_a_good_lead,
                why_now=lead.why_now,
                outreach_hook=lead.outreach_hook,
                created_at=lead.created_at.isoformat() if lead.created_at else None
            ))

        return LeadGenerateResponse(
            request_id=req.id,
            icp=req.icp,
            industry=req.industry,
            geography=req.geography,
            number_of_leads=req.number_of_leads,
            leads=lead_responses
        )

    @staticmethod
    def get_lead_by_id(db: Session, lead_id: str) -> Optional[LeadResponse]:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None

        signals = []
        sources = set()
        if lead.website:
            sources.add(lead.website)

        for sig in lead.signals:
            signals.append(SignalSchema(
                id=sig.id,
                signal_type=sig.signal_type,
                signal_text=sig.signal_text,
                source_url=sig.source_url,
                detected_at=sig.detected_at.isoformat() if sig.detected_at else None
            ))
            if sig.source_url:
                sources.add(sig.source_url)

        sb_data = lead.score_breakdown if isinstance(lead.score_breakdown, dict) else {}
        sb = ScoreBreakdown(**sb_data) if sb_data else ScoreBreakdown()

        return LeadResponse(
            id=lead.id,
            company_name=lead.company_name,
            website=lead.website,
            description=lead.description,
            industry=lead.industry,
            location=lead.location,
            signals=signals,
            sources=list(sources),
            score=lead.score,
            score_breakdown=sb,
            why_this_is_a_good_lead=lead.why_this_is_a_good_lead,
            why_now=lead.why_now,
            outreach_hook=lead.outreach_hook,
            created_at=lead.created_at.isoformat() if lead.created_at else None
        )
