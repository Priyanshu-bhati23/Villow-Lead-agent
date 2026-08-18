"""initial_tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-08-18 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'lead_generation_requests',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('icp', sa.Text(), nullable=False),
        sa.Column('industry', sa.String(length=255), nullable=True),
        sa.Column('geography', sa.String(length=255), nullable=True),
        sa.Column('number_of_leads', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_generation_requests_created_at'), 'lead_generation_requests', ['created_at'], unique=False)

    op.create_table(
        'leads',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('request_id', sa.String(length=36), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('website', sa.String(length=512), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('industry', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score_breakdown', sa.JSON(), nullable=True),
        sa.Column('why_this_is_a_good_lead', sa.Text(), nullable=True),
        sa.Column('why_now', sa.Text(), nullable=True),
        sa.Column('outreach_hook', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['request_id'], ['lead_generation_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leads_company_name'), 'leads', ['company_name'], unique=False)
    op.create_index(op.f('ix_leads_created_at'), 'leads', ['created_at'], unique=False)
    op.create_index(op.f('ix_leads_request_id'), 'leads', ['request_id'], unique=False)
    op.create_index(op.f('ix_leads_score'), 'leads', ['score'], unique=False)

    op.create_table(
        'lead_signals',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('lead_id', sa.String(length=36), nullable=False),
        sa.Column('signal_type', sa.String(length=100), nullable=False),
        sa.Column('signal_text', sa.Text(), nullable=False),
        sa.Column('source_url', sa.String(length=512), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_signals_lead_id'), 'lead_signals', ['lead_id'], unique=False)

def downgrade() -> None:
    op.drop_table('lead_signals')
    op.drop_table('leads')
    op.drop_table('lead_generation_requests')
