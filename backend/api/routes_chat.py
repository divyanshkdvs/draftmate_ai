"""
Chat, Legal Drafting Studio, and Redline Comparison Endpoints
"""

import difflib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.core.ai_engine import ai_orchestrator, SUPPORTED_MODELS
from backend.core.headroom import headroom
from backend.core.style_adapter import legal_style_adapter
from backend.skills.registry import legal_skills_registry
from backend.verification.citation_engine import citation_verifier

router = APIRouter(prefix="/api/chat", tags=["chat"])


class DraftRequest(BaseModel):
    prompt: str
    model_id: Optional[str] = "claude-3-5-sonnet"
    skill_id: Optional[str] = None
    skill_tag: Optional[str] = None
    context_docs: Optional[List[Dict[str, Any]]] = None
    reference_style_text: Optional[str] = None
    temperature: Optional[float] = 0.2
    optimize_tokens: Optional[bool] = True


class RedlineRequest(BaseModel):
    original_text: str
    revised_text: str


@router.get("/models")
def get_supported_models():
    """List available LLMs with capabilities and latency tiers."""
    return SUPPORTED_MODELS


@router.post("/draft")
async def generate_draft(req: DraftRequest):
    """
    Generate professional legal draft or analysis with:
    1. Dynamic skill system prompt
    2. Headroom token optimization on reference context
    3. Style adaptation from sample reference file
    4. Multi-model routing
    5. Automatic citation verification scan on output
    """
    skill = None
    if req.skill_id:
        skill = legal_skills_registry.get_skill(req.skill_id)
    elif req.skill_tag:
        skill = legal_skills_registry.find_by_tag(req.skill_tag)

    # Style adaptation profile
    style_profile = None
    if req.reference_style_text:
        style_profile = legal_style_adapter.analyze_style(req.reference_style_text, "User Reference Document")

    # Headroom Token Optimization
    headroom_metrics = None
    processed_docs = req.context_docs or []
    if req.optimize_tokens and processed_docs:
        optimized_docs = []
        total_original_tokens = 0
        total_optimized_tokens = 0

        for doc in processed_docs:
            content = doc.get("markdown", "")
            opt = headroom.optimize_context(content, target_focus="general", compress_boilerplate=True, preserve_citations=True)
            total_original_tokens += opt["original_tokens"]
            total_optimized_tokens += opt["optimized_tokens"]
            optimized_docs.append({
                "filename": doc.get("filename", "Doc"),
                "markdown": opt["optimized_text"]
            })

        processed_docs = optimized_docs
        tokens_saved = total_original_tokens - total_optimized_tokens
        headroom_metrics = {
            "original_tokens": total_original_tokens,
            "optimized_tokens": total_optimized_tokens,
            "tokens_saved": tokens_saved,
            "reduction_percentage": f"{round((tokens_saved / max(1, total_original_tokens)) * 100, 1)}%" if total_original_tokens else "0%"
        }

    # Generate response via AI Orchestrator
    ai_result = await ai_orchestrator.generate_response(
        prompt=req.prompt,
        system_prompt=skill.system_prompt if skill else None,
        model_id=req.model_id or "claude-3-5-sonnet",
        temperature=req.temperature or 0.2,
        context_docs=processed_docs,
        style_profile=style_profile,
        skill_metadata=skill.to_dict() if skill else None
    )

    # Run instant citation audit on generated output
    citation_audit = citation_verifier.audit_document_citations(ai_result["text"])

    return {
        "draft": ai_result["text"],
        "model": ai_result["model_used"],
        "badge": ai_result.get("badge", "Advanced"),
        "provider": ai_result.get("provider", "AI"),
        "skill_used": skill.to_dict() if skill else None,
        "style_profile": style_profile,
        "headroom_metrics": headroom_metrics,
        "citation_audit": citation_audit
    }


@router.post("/redline")
def compute_redline(req: RedlineRequest):
    """
    Compare original legal clause/document against revised version.
    Generates word-level and line-level diff markup (additions, deletions).
    """
    orig_lines = req.original_text.splitlines(keepends=True)
    rev_lines = req.revised_text.splitlines(keepends=True)

    differ = difflib.Differ()
    diff = list(differ.compare(orig_lines, rev_lines))

    structured_diff = []
    added_count = 0
    deleted_count = 0

    for line in diff:
        marker = line[:2]
        content = line[2:]
        if marker == "+ ":
            structured_diff.append({"type": "addition", "text": content})
            added_count += 1
        elif marker == "- ":
            structured_diff.append({"type": "deletion", "text": content})
            deleted_count += 1
        elif marker == "  ":
            structured_diff.append({"type": "unchanged", "text": content})

    html_diff = difflib.HtmlDiff().make_table(orig_lines, rev_lines, "Original Draft", "Revised DraftMate Draft")

    return {
        "structured_diff": structured_diff,
        "html_diff": html_diff,
        "additions_count": added_count,
        "deletions_count": deleted_count,
        "summary": f"{added_count} line additions, {deleted_count} line deletions."
    }
