"""
DraftMate AI: Legal Drafting Studio - FastAPI Application Entry Point
Kodekurrent Season 2 Hackathon
"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.api.routes_skills import router as skills_router
from backend.api.routes_documents import router as documents_router
from backend.api.routes_prompt import router as prompt_router
from backend.api.routes_citations import router as citations_router
from backend.api.routes_voice import router as voice_router
from backend.api.routes_chat import router as chat_router
from backend.api.routes_higuruma import router as higuruma_router

app = FastAPI(
    title="DraftMate AI: Legal Drafting Studio",
    description="AI-powered legal drafting platform integrating Microsoft MarkItDown, Headroom token optimization, dynamic legal skills framework, citation verification, and voice-controlled workflows.",
    version="2.0.0"
)

# Enable CORS for Next.js / frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(skills_router)
app.include_router(documents_router)
app.include_router(prompt_router)
app.include_router(citations_router)
app.include_router(voice_router)
app.include_router(chat_router)
app.include_router(higuruma_router)

# Paths for static frontend
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_frontend_root():
    """Serves the central Legal Drafting Studio interface."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "product": "DraftMate AI: Legal Drafting Studio",
        "status": "online",
        "docs_url": "/docs",
        "message": "FastAPI Legal Backend is running. Please access frontend at /"
    }


@app.get("/health")
def health_check():
    """System health check and module status."""
    return {
        "status": "operational",
        "system": "DraftMate AI Studio",
        "modules": {
            "markitdown": "Microsoft MarkItDown Ingestion Active",
            "headroom": "Token & Context Optimizer Active",
            "skills_framework": "Dynamic Legal Skills Registry Active",
            "citation_verifier": "Authority Database & Hallucination Guardrail Active",
            "voice_agent": "Voice Dictation & Consequential Safety Guard Active",
            "higuruma_companion": "Hiromi Higuruma Defense Persona Active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
