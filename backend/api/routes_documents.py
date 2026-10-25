"""
Document Processing & Token Optimization Endpoints
Powered by Microsoft MarkItDown and Headroom
"""

import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.core.markitdown_engine import legal_markitdown
from backend.core.headroom import headroom
from backend.core.style_adapter import legal_style_adapter

router = APIRouter(prefix="/api/documents", tags=["documents"])

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "documents" / "samples"
STORAGE_DIR = BASE_DIR / "documents" / "storage"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)


class OptimizeContextRequest(BaseModel):
    text: str
    focus: Optional[str] = "general"
    compress_boilerplate: Optional[bool] = True
    preserve_citations: Optional[bool] = True
    max_tokens: Optional[int] = 4000


class ExtractStyleRequest(BaseModel):
    text: str
    doc_name: Optional[str] = "Reference File"


@router.get("/samples")
def get_sample_documents():
    """Retrieve preloaded legal matters and templates matching the reference mockups."""
    files = [
        {"name": "Employment Agreement.pdf", "sample_file": "Employment_Agreement.md", "type": "Employment", "category": "Active Matters", "size": "142 KB", "date": "Oct 2026"},
        {"name": "NDA.pdf", "sample_file": "NDA.md", "type": "Non-Disclosure", "category": "Templates", "size": "88 KB", "date": "Oct 2026"},
        {"name": "Board Resolution.docx", "sample_file": "Board_Resolution.md", "type": "Corporate Governance", "category": "Active Matters", "size": "45 KB", "date": "Oct 2026"},
        {"name": "Share Purchase Agreement.pdf", "sample_file": "Share_Purchase_Agreement.md", "type": "M&A", "category": "Shared with Me", "size": "320 KB", "date": "Sep 2026"},
        {"name": "Due Diligence Report.pdf", "sample_file": "Due_Diligence_Report.md", "type": "Compliance", "category": "Recent Files", "size": "512 KB", "date": "Oct 2026"},
        {"name": "Legal Notice.docx", "sample_file": "Legal_Notice.md", "type": "Litigation", "category": "Recent Files", "size": "64 KB", "date": "Oct 2026"},
    ]
    return files


@router.get("/samples/{filename}")
def read_sample_document(filename: str):
    """Read a preloaded sample document and parse into structured markdown with MarkItDown."""
    target_path = SAMPLES_DIR / filename
    if not target_path.exists():
        # Try appending .md
        target_path = SAMPLES_DIR / f"{filename}.md"
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Sample document not found")

    content = target_path.read_text(encoding="utf-8")
    result = legal_markitdown.convert_text(content, title=filename)
    return result


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload legal document (PDF, DOCX, TXT), convert using Microsoft MarkItDown, and extract metadata."""
    allowed_extensions = [".pdf", ".docx", ".doc", ".txt", ".md", ".rtf"]
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {', '.join(allowed_extensions)}")

    save_path = STORAGE_DIR / file.filename
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert using Microsoft MarkItDown
        converted = legal_markitdown.convert_file(str(save_path))
        return converted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")


@router.post("/optimize-context")
def optimize_context(req: OptimizeContextRequest):
    """Run Headroom Token & Context Optimization on legal text."""
    return headroom.optimize_context(
        text=req.text,
        target_focus=req.focus or "general",
        compress_boilerplate=req.compress_boilerplate if req.compress_boilerplate is not None else True,
        preserve_citations=req.preserve_citations if req.preserve_citations is not None else True,
        max_tokens=req.max_tokens or 4000
    )


@router.post("/extract-style")
def extract_style(req: ExtractStyleRequest):
    """Extract drafting style profile from a user-supplied reference document."""
    return legal_style_adapter.analyze_style(req.text, req.doc_name or "Reference Document")
