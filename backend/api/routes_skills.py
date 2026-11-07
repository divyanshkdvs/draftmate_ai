"""
Legal Skills API Endpoints for DraftMate AI
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from backend.skills.registry import legal_skills_registry

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
def list_skills(
    category: Optional[str] = Query(None, description="Filter by category e.g. 'Drafting & Writing'"),
    audience: Optional[str] = Query(None, description="Filter by audience 'lawyer', 'student', or 'all'"),
    search: Optional[str] = Query(None, description="Search term for name/description")
):
    """Retrieve indexed legal skills filtered by category, audience, or search."""
    return legal_skills_registry.list_skills(
        category=category,
        target_audience=audience,
        search_query=search
    )


@router.get("/categories")
def get_categories():
    """Retrieve distinct legal skill categories."""
    skills = legal_skills_registry.list_skills()
    cats = sorted(list(set(s["category"] for s in skills)))
    return cats


@router.get("/find-by-tag/{tag}")
def find_by_tag(tag: str):
    """Find skill matching a chat mention tag like @ContractReview or @NDA."""
    skill = legal_skills_registry.find_by_tag(tag)
    if not skill:
        raise HTTPException(status_code=404, detail=f"No legal skill found for tag: {tag}")
    return skill.to_dict()


@router.get("/{skill_id}")
def get_skill(skill_id: str):
    """Retrieve full skill metadata by ID."""
    skill = legal_skills_registry.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.to_dict()
