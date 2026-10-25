"""
Prompt Strength Meter & Prompt Improvement Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.core.prompt_enhancer import prompt_enhancer

router = APIRouter(prefix="/api/prompt", tags=["prompt"])


class PromptEvaluateRequest(BaseModel):
    prompt: str


class PromptImproveRequest(BaseModel):
    prompt: str


@router.post("/evaluate")
def evaluate_prompt(req: PromptEvaluateRequest):
    """Calculates prompt strength score (0-100%) and provides legal clarity tips."""
    return prompt_enhancer.evaluate_strength(req.prompt)


@router.post("/improve")
def improve_prompt(req: PromptImproveRequest):
    """Enriches prompt with legal jurisdiction, governing statutes, and precision clauses."""
    return prompt_enhancer.improve_prompt(req.prompt)
