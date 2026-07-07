import sys
import os

# Add the project root (backend) directory to the sys.path
# This ensures python resolves imports starting with 'app.' correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
print("========== CORS ORIGINS ==========")
print(settings.CORS_ORIGINS)
print("==================================")
from app.core.logging import setup_logging
from app.api.endpoints import router as api_router

# Initialize application logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FounderAI - Enterprise Multi-Agent Operating System for Startup Founders",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to FounderAI API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    # Start uvicorn server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
