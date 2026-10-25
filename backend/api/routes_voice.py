"""
Integrated Voice Agent & Consequential Action Safety Endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.voice.voice_agent import voice_agent
from backend.voice.safety_guard import safety_guard

router = APIRouter(prefix="/api/voice", tags=["voice"])


class VoiceParseRequest(BaseModel):
    transcript: str


class SafetyConfirmRequest(BaseModel):
    token: str


@router.post("/parse")
def parse_voice_command(req: VoiceParseRequest):
    """
    Parses spoken legal instructions, matches specialized skills,
    and flags consequential actions for user confirmation.
    """
    return voice_agent.parse_transcript(req.transcript)


@router.post("/safety/confirm")
def confirm_consequential_action(req: SafetyConfirmRequest):
    """
    Validates confirmation token for destructive/consequential actions
    (e.g., overwriting a draft or deleting a matter document).
    """
    success = safety_guard.verify_and_consume(req.token)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired confirmation token. Please re-issue voice instruction."
        )
    return {
        "status": "confirmed",
        "message": "Consequential action successfully authorized and executed."
    }
