# FounderAI API Documentation Guide

Welcome to the FounderAI API. This guide outlines the endpoints, data schemas, and integration details for the multi-agent co-founder system.

## Endpoints

### 1. Health Check
* **Path**: `GET /api/health`
* **Response**:
  ```json
  {
    "status": "healthy",
    "service": "FounderAI API"
  }
  ```

### 2. Startup Analysis
* **Path**: `POST /api/startup/analyze`
* **Request Headers**: `Content-Type: application/json`
* **Request Payload**:
  ```json
  {
    "idea": "A SaaS platform automating medical billing compliance for small clinics.",
    "industry": "Healthcare Tech / SaaS",
    "country": "United States",
    "budget": "$15,000",
    "stage": "Idea",
    "founder_name": "Dr. Jane Smith",
    "target_market": "Private Medical Clinics and Billing Agents"
  }
  ```
* **Response Payload**: Returns the full compiled `FounderState` containing:
  - `startup`: Input startup details.
  - `discovery`: USP, core problem/solution, opportunities, and risks.
  - `market`: TAM/SAM/SOM estimates, buyer personas, and industry trends.
  - `competitors`: Direct/indirect competitors list, SWOT matrix, and positioning.
  - `business_model`: Cost structure items and revenue streams.
  - `registration`: State registration requirements, portals, and licenses.
  - `funding`: Bootstrapping blueprints, grants list, and investment readiness score.
  - `report`: Synthesized executive summaries and a 30/60/90 roadmap.
  - `metadata`: `run_id`, `status`, and `pdf_url`.

### 3. PDF serving
* **Path**: `GET /api/startup/pdf/{pdf_id}`
* **Response**: Binary stream of the generated ReportLab PDF document.

---

## Technical Stack & Configuration
* **Core Language**: Python 3.12
* **Framework**: FastAPI
* **Orchestration**: LangGraph
* **LLM Model**: Google Gemini 2.5 Flash (`gemini-2.5-flash`)
* **Vector Store**: ChromaDB (Stubbed)
* **Configuration**: Managed via `.env` and `app/core/config.py`.
