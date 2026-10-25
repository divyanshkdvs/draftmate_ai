"""
Citation & Legal Authority Verification Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.verification.citation_engine import citation_verifier
from backend.verification.authority_db import VERIFIED_PRECEDENTS, VERIFIED_STATUTES

router = APIRouter(prefix="/api/citations", tags=["citations"])


class VerifyCitationsRequest(BaseModel):
    text: str


@router.post("/verify")
def verify_citations(req: VerifyCitationsRequest):
    """
    Audits citations and statutory provisions against official legal repositories.
    Categorizes references into Verified, Partially Verified, and Unverified / Flagged states.
    """
    return citation_verifier.audit_document_citations(req.text)


@router.get("/database-stats")
def get_database_stats():
    """Returns metadata on verified authorities, landmark precedents, and statutes."""
    return {
        "precedents_count": len(VERIFIED_PRECEDENTS),
        "statutes_count": len(VERIFIED_STATUTES),
        "jurisdictions_supported": ["Supreme Court of India", "High Courts", "United States Supreme Court", "UK Common Law"],
        "governing_codes": [
            "Indian Contract Act 1872",
            "Companies Act 2013",
            "Negotiable Instruments Act 1881",
            "Arbitration & Conciliation Act 1996",
            "Digital Personal Data Protection Act 2023",
            "Bharatiya Nyaya Sanhita 2023 (BNS)",
            "Constitution of India",
            "18 U.S.C. § 1836 (Defend Trade Secrets Act)"
        ]
    }
