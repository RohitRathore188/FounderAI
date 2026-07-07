import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.graph.builder import graph
from app.services.pdf_service import PDFService
from app.core.logging import logger

router = APIRouter()

# Data directory for storing generated PDFs
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)
PDF_DIR = os.path.join(DATA_DIR, "pdf")

class StartupAnalyzeRequest(BaseModel):
    idea: str = Field(description="Startup description or idea statement")
    industry: str = Field(description="Sector or industry niche")
    country: str = Field(description="Country of registration")
    state: str = Field(default="", description="State or province of registration")
    district: str = Field(default="", description="City or district within the state")
    budget: str = Field(description="Initial budget / startup capital")
    stage: str = Field(description="Current stage (e.g. Idea, MVP, Seed)")
    founder_name: str = Field(description="Primary founder's name")
    target_market: str = Field(description="Target customer segment")
    team_size: str = Field(default="1", description="Initial team size")

@router.post("/startup/analyze")
async def analyze_startup(request: StartupAnalyzeRequest):
    """
    Executes the multi-agent graph workflow to analyze the startup idea.
    Returns the complete structured state along with PDF download URL.
    """
    logger.info(f"API: Received analysis request for {request.idea} by {request.founder_name}")
    run_id = str(uuid.uuid4())

    # Assemble a full location context string for all agents to use
    location_parts = [p for p in [request.district, request.state, request.country] if p.strip()]
    location_context = ", ".join(filter(None, [request.district, request.state, request.country]))

    print("================== PIPELINE START ==================")
    print("Received Country:", request.country)
    print("Received Industry:", request.industry)
    print("Received Startup:", request.idea)
    print("====================================================")

    startup_data = request.model_dump()
    startup_data["location_context"] = location_context

    # Initialize LangGraph State matching FounderState (using the new financial key)
    initial_state = {
        "startup": startup_data,
        "discovery": None,
        "validation": None,
        "market": None,
        "competitors": None,
        "business_model": None,
        "financial": None,
        "legal": None,
        "funding": None,
        "roadmap": None,
        "risk": None,
        "metadata": {
            "run_id": run_id,
            "status": "processing"
        }
    }

    try:
        # Run the workflow
        logger.info(f"API: Running multi-agent LangGraph workflow for run_id: {run_id}")
        final_state = graph.invoke(initial_state)
        
        # Ensure pdf directory exists
        os.makedirs(PDF_DIR, exist_ok=True)
        pdf_path = os.path.join(PDF_DIR, f"{run_id}.pdf")
        
        # Generate the PDF report
        logger.info(f"API: Compiling PDF report at {pdf_path}")
        PDFService.generate_startup_report(final_state, pdf_path)
        
        # Update metadata in final response
        final_state["report"] = {
            "summary": "Report synthesis complete.",
            "data": {
                "pdf_url": f"/api/startup/pdf/{run_id}",
                "executive_summary": "Report synthesis complete."
            }
        }
        final_state["metadata"]["pdf_url"] = f"/api/startup/pdf/{run_id}"
        final_state["metadata"]["status"] = "success"
        
        # Backward compatibility mappings for frontend
        final_state["registration"] = final_state["legal"]
        final_state["financial_planning"] = final_state["financial"]
        
        return final_state

    except Exception as e:
        import traceback
        logger.exception(f"API: Error during startup orchestration: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": f"Orchestration workflow failed: {str(e)}", "stack": traceback.format_exc()}
        )

@router.get("/startup/pdf/{pdf_id}")
async def download_pdf(pdf_id: str):
    """
    Serves the compiled PDF startup report.
    """
    pdf_path = os.path.join(PDF_DIR, f"{pdf_id}.pdf")
    if not os.path.exists(pdf_path):
        logger.warning(f"API: Requested PDF not found at {pdf_path}")
        raise HTTPException(status_code=404, detail="Report PDF not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"founderai_{pdf_id[:8]}.pdf")

@router.get("/health")
async def health_check():
    """
    Checks API service health.
    """
    return {"status": "healthy", "service": "FounderAI API"}
