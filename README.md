# FounderAI - AI Startup Co-Founder OS

FounderAI is a production-ready, multi-agent AI operating system that assists aspiring founders in turning their ideas into launch-ready startups. 

Instead of answering isolated queries, it uses a **LangGraph Orchestrator** to coordinate specialized agents (Discovery, Market, Competitor, Business Model, Registration, Funding, and Report Synthesis) to compile a complete, cohesive venture launch package.

---

## Workspace Layout

```
Founder AI/
├── backend/             # FastAPI & LangGraph multi-agent backend
│   ├── app/             # Application source packages
│   ├── data/            # Local data persistence and generated PDFs
│   ├── docs/            # Developer API guides and documentation
│   ├── tests/           # Comprehensive pytest suite
│   ├── main.py          # FastAPI application server entrypoint
│   └── requirements.txt # Python dependency file
│
└── frontend/            # React & Vite single-page dashboard
    ├── src/             # Component tree & design system
    ├── index.html       # Core HTML layout
    └── package.json     # Node modules and build configurations
```

---

## Quick Start Guide

### 1. Start the FastAPI Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Activate the Python virtual environment:
   ```bash
   # Windows PowerShell
   .venv/Scripts/activate
   ```
3. (Optional) Set your Gemini API key in `.env`:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```
4. Start the server using Uvicorn:
   ```bash
   py -m uvicorn main:app --reload --port 8000
   ```
5. Open the Swagger UI docs to inspect endpoints: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the React Frontend

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Launch the Vite development server:
   ```bash
   npm run dev
   ```
3. Open your browser and explore the UI at: [http://localhost:5173](http://localhost:5173)

---

## Multi-Agent Architecture

```
User Idea Input 
      ↓
FastAPI Endpoint (/api/startup/analyze)
      ↓
LangGraph Orchestrator 
  ├── Discovery Agent (USP, problem, solution, risks, opportunities)
  ├── Market Agent (TAM/SAM/SOM sizing, CAGR, buyer personas)
  ├── Competitor Agent (SWOT analysis, direct/indirect scans)
  ├── Business Model Agent (9-box Canvas, cost structures, revenue streams)
  ├── Registration Agent (Entity recommendations, regional portals, licenses)
  ├── Funding Agent (Bootstrapping, VC stages, grant matches, readiness score)
  └── Report Generator Agent (Synthesis, 30/60/90 roadmap, ReportLab PDF compile)
      ↓
Structured JSON + Downloadable PDF File served
```

---

## Verification & Testing

To run the automated test suite, navigate to the `backend/` directory and run:
```bash
$env:PYTHONPATH="."; .venv/Scripts/python -m pytest tests/
```
All tests verify endpoint status, graph traversal, and agent schema structures.
