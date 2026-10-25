"""
Legal Skills API Endpoints for DraftMate AI
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from backend.skills.registry import legal_skills_registry

router = APIRouter(prefix="/api/skills", tags=["skills"])


# FIX 1: Handles both /api/skills and /api/skills/ without 307 redirects
@router.get("", include_in_schema=True)
@router.get("/", include_in_schema=False)
def list_skills(
    category: Optional[str] = Query(None, description="Filter by category e.g. 'Drafting & Writing'"),
    audience: Optional[str] = Query(None, description="Filter by audience 'lawyer', 'student', or 'all'"),
    search: Optional[str] = Query(None, description="Search term for name/description")
) -> List[Dict[str, Any]]:
    """Retrieve indexed legal skills filtered by category, audience, or search."""
    return legal_skills_registry.list_skills(
        category=category,
        target_audience=audience,
        search_query=search
    )


# FIX 2: Safe set comprehension guarding against missing keys or None values
@router.get("/categories")
def get_categories() -> List[str]:
    """Retrieve distinct legal skill categories."""
    skills = legal_skills_registry.list_skills()
    cats = sorted(list({s.get("category") for s in skills if s.get("category")}))
    return cats


# FIX 3: {tag:path} allows handling '@' and encoded characters cleanly with ID fallback
@router.get("/find-by-tag/{tag:path}")
def find_by_tag(tag: str) -> Dict[str, Any]:
    """Find skill matching a chat mention tag like @ContractReview or @NDA."""
    cleaned = tag.strip()
    skill = legal_skills_registry.find_by_tag(cleaned)
    if not skill:
        # Fallback to direct ID lookup
        skill = legal_skills_registry.get_skill(cleaned)
    if not skill:
        raise HTTPException(status_code=404, detail=f"No legal skill found for tag: '{tag}'")
    
    data = skill.to_dict()
    data["system_prompt"] = skill.system_prompt
    return data


# FIX 4: Multi-tier resilient resolver for get_skill
@router.get("/{skill_id}")
def get_skill(skill_id: str) -> Dict[str, Any]:
    """
    Retrieve full skill metadata by ID, tag, or name.
    Supports exact skill_id (e.g. 'contract_drafting'),
    tag (e.g. '@NDA', 'NDA'), and kebab-case (e.g. 'contract-drafting').
    """
    # 1. Exact ID lookup
    skill = legal_skills_registry.get_skill(skill_id)
    
    # 2. Normalized ID lookup (lowercase, hyphens to underscores, strip '@')
    if not skill:
        norm_id = skill_id.lower().replace("-", "_").replace("@", "").strip()
        skill = legal_skills_registry.get_skill(norm_id)
        
    # 3. Tag lookup (e.g. '@NDA', 'NDA', 'ContractReview')
    if not skill:
        skill = legal_skills_registry.find_by_tag(skill_id)
        
    # 4. Human-readable Name lookup (e.g. 'Contract Drafting')
    if not skill:
        for s in legal_skills_registry._skills.values():
            if s.name.lower() == skill_id.lower().strip():
                skill = s
                break
                
    if not skill:
        raise HTTPException(
            status_code=404, 
            detail=f"Skill '{skill_id}' not found. Check available skills at /api/skills"
        )
        
    # Include full system prompt metadata in response
    data = skill.to_dict()
    data["system_prompt"] = skill.system_prompt
    return data
