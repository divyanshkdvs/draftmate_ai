"""
Hiromi Higuruma Interactive Character Companion API Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.core.higuruma_persona import higuruma_engine, HIGURUMA_QUICK_SCENARIOS

router = APIRouter(prefix="/api/higuruma", tags=["higuruma"])


class HigurumaChatRequest(BaseModel):
    message: str
    active_draft: Optional[str] = None
    chat_history: Optional[List[Dict[str, str]]] = None


@router.post("/chat")
def chat_with_higuruma(req: HigurumaChatRequest):
    """
    Direct character dialogue endpoint with Defense Attorney Hiromi Higuruma.
    Provides strategic legal advice, clause cross-examination, and defense tactics.
    """
    return higuruma_engine.generate_counsel(
        user_message=req.message,
        active_draft=req.active_draft,
        chat_history=req.chat_history
    )


@router.get("/scenarios")
def get_quick_scenarios():
    """Retrieve quick tactical inquiry scenarios for the character companion."""
    return HIGURUMA_QUICK_SCENARIOS
