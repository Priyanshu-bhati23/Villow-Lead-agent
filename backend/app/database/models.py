import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class LeadGenerationRequest(Base):
    __tablename__ = "lead_generation_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    icp = Column(Text, nullable=False)
    industry = Column(String(255), nullable=True)
    geography = Column(String(255), nullable=True)
    number_of_leads = Column(Integer, default=10, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    leads = relationship("Lead", back_populates="request", cascade="all, delete-orphan")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("lead_generation_requests.id"), nullable=False, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    website = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    industry = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    score = Column(Integer, default=0, nullable=False, index=True)
    score_breakdown = Column(JSON, nullable=True)
    why_this_is_a_good_lead = Column(Text, nullable=True)
    why_now = Column(Text, nullable=True)
    outreach_hook = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    request = relationship("LeadGenerationRequest", back_populates="leads")
    signals = relationship("LeadSignal", back_populates="lead", cascade="all, delete-orphan")

class LeadSignal(Base):
    __tablename__ = "lead_signals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False, index=True)
    signal_type = Column(String(100), nullable=False) # e.g. funding, hiring, technology, job_posting
    signal_text = Column(Text, nullable=False)
    source_url = Column(String(512), nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lead = relationship("Lead", back_populates="signals")
