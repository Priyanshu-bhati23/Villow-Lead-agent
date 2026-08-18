# Lead Generation Agent for Villow Founding Publisher Program

An AI-powered Lead Generation, Signal Enrichment, and Qualification Agent MVP built for the **Villow Founding Publisher Program**.

Unlike basic LLM prompts that invent fake company names, this agent combines **real web discovery & data enrichment** with **Groq LLM reasoning** to identify real companies, extract verifiable buying signals (funding rounds, engineering hiring, stack changes), score leads transparently (0–100), explain why each lead is warm RIGHT NOW, and draft personalized outreach hooks.

---

## Architecture Flow

```
Frontend (Next.js / React)
       │ (HTTP REST)
       ▼
FastAPI Backend (Python 3.11+)
       │
       ├──► ICP Parser Agent (Groq LLM / Heuristic Fallback)
       ├──► Lead Discovery Engine (SerpAPI / Tavily / WebSearch / MockProvider)
       ├──► Data Enrichment & Signal Extraction (Funding, Hiring, Job Postings, Stack)
       ├──► Transparent Lead Scoring (0-100 Score Matrix: ICP Fit, Signals, Recency, Relevance, Confidence)
       ├──► Outreach & Reasoning Agent (Groq LLM: "Why Good Lead", "Why Now", Personalized Hook)
       └──► Villow Adapter Abstraction (VillowJobRequest / VillowJobResponse)
       │
       ▼
Neon PostgreSQL Database (SQLAlchemy + Alembic Migrations)
```

---

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, psycopg 3, httpx
- **LLM Layer**: Groq API (`llama-3.3-70b-versatile`)
- **Database**: Neon PostgreSQL (with SQLite fallback for local test mode)
- **Search & Signals**: Real Web Search API (Tavily/SerpAPI) + fallback `MockProvider`
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons

---

## Environment Variables Configuration

Create `.env` in `backend/` and `frontend/` (or at root):

### Backend (`backend/.env`)
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Neon PostgreSQL connection string
DATABASE_URL=postgresql+psycopg://user:password@ep-cool-db-123456.us-east-2.aws.neon.tech/neondb?sslmode=require

# External Search / Enrichment Provider API Settings (e.g. Tavily API)
SEARCH_API_KEY=your_search_api_key_here
SEARCH_API_URL=https://api.tavily.com/search
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Local Development Setup

### 1. Backend Setup & Run

```bash
cd backend

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Alembic Database Migrations (if DATABASE_URL is set)
alembic upgrade head

# Start FastAPI dev server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
FastAPI interactive docs will be available at: `http://localhost:8000/docs`

### 2. Frontend Setup & Run

```bash
cd frontend

# Install dependencies
npm install

# Start Next.js dev server
npm run dev
```
Dashboard will be available at: `http://localhost:3000`

---

## Running Unit Tests

Backend tests are executed using `pytest` without requiring paid API keys (uses SQLite in-memory and `MockProvider`):

```bash
cd backend
python -m pytest tests/
```

---

## API Endpoints Reference

### 1. Health Check
`GET /health`
```json
{
  "status": "ok",
  "environment": "development"
}
```

### 2. Provider & LLM Status
`GET /api/providers/status`
```json
{
  "active_provider": "RealWebSearchProvider (Tavily/SerpAPI/WebSearch)",
  "is_mock": false,
  "has_groq": true,
  "groq_model": "llama-3.3-70b-versatile",
  "has_database": true
}
```

### 3. Generate & Qualify Leads
`POST /api/leads/generate`

**Request Body:**
```json
{
  "icp": "Find SaaS companies in India with 50-500 employees that recently raised funding and are hiring engineers.",
  "industry": "SaaS",
  "geography": "India",
  "number_of_leads": 5
}
```

**Response:**
```json
{
  "request_id": "9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c",
  "icp": "Find SaaS companies in India...",
  "industry": "SaaS",
  "geography": "India",
  "number_of_leads": 5,
  "leads": [
    {
      "id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "company_name": "PerfStack AI",
      "website": "https://perfstack.io",
      "description": "B2B SaaS application performance monitoring platform...",
      "industry": "SaaS",
      "location": "Bengaluru, India",
      "signals": [
        {
          "signal_type": "funding",
          "signal_text": "PerfStack AI raised $12M Series A led by Peak XV Partners.",
          "source_url": "https://techcrunch.com/perfstack-series-a"
        }
      ],
      "sources": ["https://perfstack.io/about"],
      "score": 91,
      "score_breakdown": {
        "icp_fit": 28,
        "signal_strength": 24,
        "signal_recency": 19,
        "company_relevance": 13,
        "data_confidence": 9
      },
      "why_this_is_a_good_lead": "Strong ICP match operating in SaaS in Bengaluru, India.",
      "why_now": "Company recently raised $12M Series A and is actively hiring backend engineers.",
      "outreach_hook": "Saw that PerfStack AI recently raised its Series A and is expanding technical headcount..."
    }
  ]
}
```

### 4. Villow Job Adapter Placeholder
`POST /api/villow/job`

Translates incoming Villow Founding Publisher Program job contracts to the internal agent pipeline via `VillowAdapter`.

---

## Villow Integration Placeholder (`app/villow/`)

The application contains a clean abstraction layer (`app/villow/adapter.py`) implementing placeholder methods for:
- Receiving Villow job contracts (`receive_villow_job`)
- Converting Villow inputs into internal requests (`convert_to_internal_request`)
- Running execution workflows (`run_lead_generation_workflow`)
- Returning structured outputs (`convert_to_villow_response`)

> **Note**: Once official Villow SDK specification is released, update `app/villow/adapter.py` and `app/villow/schemas.py` directly.

---

## Deployment Setup

### 1. Render Deployment (Backend Service)

- Create a new **Web Service** on Render.
- Connect your GitHub repository.
- **Root Directory**: `backend`
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `GROQ_API_KEY`
  - `GROQ_MODEL`
  - `DATABASE_URL` (Neon PostgreSQL string)
  - `SEARCH_API_KEY`
  - `SEARCH_API_URL`

### 2. Vercel Deployment (Frontend Dashboard)

- Import your GitHub repository into Vercel.
- **Root Directory**: `frontend`
- **Framework Preset**: Next.js
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL` = `https://your-backend-service.onrender.com`

---

## Known Limitations & Future Improvements

1. **Search API Quotas**: Requires active Tavily / SerpAPI key for real-time live web scraping; defaults to `MockProvider` when API keys are omitted.
2. **Contact Email Discovery**: Future iterations can integrate Clearbit / Apollo / Hunter APIs for verified founder email lookup.
