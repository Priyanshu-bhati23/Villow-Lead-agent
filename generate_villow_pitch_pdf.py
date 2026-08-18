import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    pdf_filename = r"c:\Users\priya\Desktop\Lead\Villow_Lead_Generation_Agent_Proposal.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#1E1B4B")      # Deep Indigo / Navy
    SECONDARY = colors.HexColor("#4F46E5")    # Indigo Accent
    DARK_TEXT = colors.HexColor("#0F172A")    # Slate 900
    MUTED_TEXT = colors.HexColor("#475569")   # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")     # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#E2E8F0") # Slate 200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15.5,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=3,
        leftIndent=10
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=4
    )

    elements = []

    # Header Title Block
    elements.append(Paragraph("VILLOW FOUNDING PUBLISHER PROGRAM", subtitle_style))
    elements.append(Paragraph("Universal B2B Lead Generation Agent — Proposal & Scope", title_style))
    elements.append(Paragraph("Author: Priyanshu | Full-Stack AI Engineer | Stack: Groq LLM + FastAPI + Neon Postgres + Next.js", ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=MUTED_TEXT, spaceAfter=8)))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    # 1. Executive Summary & Product Scope
    elements.append(Paragraph("1. Executive Summary & Product Vision", heading2_style))
    elements.append(Paragraph(
        "Unlike basic lead tools limited strictly to tech software, the <b>Villow Universal Lead Generation Agent</b> is a comprehensive, multi-industry B2B qualification engine. "
        "It supports <b>ALL commercial sectors</b>—including <b>Healthcare & Biotech</b> (FDA approvals, diagnostic expansions), <b>Manufacturing & Industrial</b> (plant setup, ISO certifications), "
        "<b>E-Commerce & Retail</b> (D2C funding, CMO hiring), <b>Real Estate & Construction</b> (commercial projects, architectural hiring), <b>Financial Services & Fintech</b>, and <b>SaaS & Technology</b>.",
        body_style
    ))

    # Core Principle Callout Box
    principle_data = [[
        Paragraph("<b>UNIVERSAL PRODUCT WORKFLOW:</b><br/><b>Any Industry ICP Prompt</b> → <b>Live Web Discovery</b> → <b>Multi-Sector Data Enrichment</b> → <b>Verifiable Signals</b> → <b>0-100 Score Matrix</b> → <b>Groq LLM Reasoning</b> → <b>Personalized Hooks & Neon DB</b>", callout_style)
    ]]
    principle_table = Table(principle_data, colWidths=[540])
    principle_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(principle_table)
    elements.append(Spacer(1, 8))

    # 2. Universal Industry Scope Matrix
    elements.append(Paragraph("2. Universal Cross-Industry Coverage Matrix", heading2_style))
    
    sector_data = [
        [Paragraph("<b>Industry Sector</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)), 
         Paragraph("<b>Buying Signals Detected</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)), 
         Paragraph("<b>Target Executive Persona & Value Proposition</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        
        [Paragraph("<b>Healthcare & Biotech</b>", body_style), Paragraph("FDA/ISO approvals, diagnostic center openings, clinical trial milestones, medical director hiring", body_style), Paragraph("Medical Equipment Vendors, HealthTech Providers, Diagnostic Suppliers", body_style)],
        [Paragraph("<b>Manufacturing & Industrial</b>", body_style), Paragraph("New plant construction, factory automation investments, ISO certifications, VP Operations hiring", body_style), Paragraph("Industrial Machinery, Supply Chain Software, Raw Material Distributors", body_style)],
        [Paragraph("<b>E-Commerce & Retail</b>", body_style), Paragraph("Series A/B funding, D2C retail expansion, CMO/Performance Marketing hiring, inventory tech updates", body_style), Paragraph("Ad Agencies, Logistics Providers, Packaging & Warehouse Tech", body_style)],
        [Paragraph("<b>Real Estate & Construction</b>", body_style), Paragraph("Groundbreaking on commercial tech parks, architectural hires, zoning approvals, LEED certification", body_style), Paragraph("Building Material Suppliers, Commercial Brokers, HVAC & Security Vendors", body_style)],
        [Paragraph("<b>Fintech & Banking</b>", body_style), Paragraph("Regulatory compliance approvals, SOC2 security launches, VP Risk/Legal hiring, capital raises", body_style), Paragraph("Compliance Software, Payment Gateways, Cybersecurity Consultancies", body_style)],
        [Paragraph("<b>SaaS & Technology</b>", body_style), Paragraph("Venture funding rounds, active engineering hiring, cloud stack migrations, product launches", body_style), Paragraph("DevOps Tools, Cloud Providers, B2B Growth Agencies", body_style)],
    ]

    sector_table = Table(sector_data, colWidths=[130, 210, 200])
    sector_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    elements.append(sector_table)
    elements.append(Spacer(1, 8))

    # 3. Technical Architecture Summary
    elements.append(Paragraph("3. Technical Architecture & Delivery Readiness", heading2_style))
    elements.append(Paragraph("• <b>Frontend Dashboard:</b> Next.js 14, TypeScript, Tailwind CSS with active sector preset selectors (🏥 Healthcare, 🏭 Manufacturing, 🛒 D2C, 🏢 Real Estate, 💻 SaaS).", bullet_style))
    elements.append(Paragraph("• <b>Backend API:</b> Python 3.11+, FastAPI listening on <code>0.0.0.0</code> ready for free deployment on Render.", bullet_style))
    elements.append(Paragraph("• <b>LLM Reasoning:</b> Groq API (<code>llama-3.3-70b-versatile</code>) performing structured JSON extraction and non-hallucinated outreach hook generation.", bullet_style))
    elements.append(Paragraph("• <b>Database Storage:</b> Neon PostgreSQL cloud relational storage with SQLAlchemy 2.0 and Alembic migrations.", bullet_style))
    elements.append(Paragraph("• <b>Villow Adapter:</b> Isolated <code>app/villow/adapter.py</code> bridge ready to plug into the official Villow Founding Publisher SDK upon release.", bullet_style))

    elements.append(Spacer(1, 8))

    # 4. Selection Criteria for Villow Program
    elements.append(Paragraph("4. Why This Project Should Be Selected for Villow", heading2_style))
    elements.append(Paragraph("1. <b>Turnkey Delivery Ready:</b> 100% working production codebase with 10/10 passing Pytest test suites, live backend API, and live Neon DB.", bullet_style))
    elements.append(Paragraph("2. <b>Universal Market Fit:</b> Serves all commercial sectors, expanding the total addressable market (TAM) for Villow users across all industries.", bullet_style))
    elements.append(Paragraph("3. <b>Clean Adapter Design:</b> Built with zero assumptions about unreleased Villow SDK methods, ensuring immediate plug-and-play SDK integration.", bullet_style))
    elements.append(Paragraph("4. <b>Free Cloud Deployment:</b> Pre-configured for zero-cost hosting on Render (Backend), Vercel (Frontend), and Neon (Database).", bullet_style))

    doc.build(elements)
    print("Universal PDF generated successfully:", pdf_filename)

if __name__ == "__main__":
    generate_pdf()
