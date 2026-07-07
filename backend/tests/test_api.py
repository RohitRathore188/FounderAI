import os
import shutil
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "FounderAI API"}

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to FounderAI API" in response.json()["message"]

def test_api_analyze_and_download_pdf():
    payload = {
        "idea": "Premium tea subscription delivery service",
        "industry": "Food & Beverage",
        "country": "India",
        "budget": "INR 200,000",
        "stage": "MVP",
        "founder_name": "Rajesh",
        "target_market": "Urban office professionals"
    }

    # Execute analysis endpoint
    response = client.post("/api/startup/analyze", json=payload)
    assert response.status_code == 200
    
    state = response.json()
    assert state["metadata"]["status"] == "success"
    assert "pdf_url" in state["metadata"]
    
    pdf_url = state["metadata"]["pdf_url"]
    # Retrieve PDF via generated download URL
    pdf_response = client.get(pdf_url)
    assert pdf_response.status_code == 200
    assert pdf_response.headers["content-type"] == "application/pdf"
    
    # Clean up generated PDFs in data directory after test runs
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data"
    )
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
