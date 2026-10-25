"""
Comprehensive End-to-End Test Suite for DraftMate AI
Validates all 5 Core Architectural Modules:
1. Document Processing & Ingestion (Microsoft MarkItDown)
2. Token Optimization & Context Retrieval (Headroom)
3. Dynamic Legal Skills Framework (Claude for Legal & Awesome Legal Skills)
4. Citation & Legal Authority Verification Engine (Supreme Court / Statutes)
5. Integrated Voice Agent & Consequential Safety Guard (OpenWhispr / VoxCPM)
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from backend.core.markitdown_engine import legal_markitdown
from backend.core.headroom import headroom
from backend.core.style_adapter import legal_style_adapter
from backend.core.prompt_enhancer import prompt_enhancer
from backend.skills.registry import legal_skills_registry
from backend.verification.citation_engine import citation_verifier
from backend.voice.voice_agent import voice_agent
from backend.voice.safety_guard import safety_guard
from backend.core.ai_engine import ai_orchestrator


def run_tests():
    print("=" * 70)
    print("🚀 RUNNING DRAFTMATE AI ARCHITECTURAL VALIDATION SUITE")
    print("=" * 70)

    passed = 0
    total = 0

    # Test 1: Microsoft MarkItDown Document Processing
    total += 1
    print("\n[TEST 1] Testing Document Processing & Ingestion...")
    sample_text = "# NON-DISCLOSURE AGREEMENT\n\nWHEREAS, Party A and Party B agree to evaluate confidential data."
    converted = legal_markitdown.convert_text(sample_text, title="Test NDA")
    assert "markdown" in converted
    assert converted["metadata"]["document_type"] == "Non-Disclosure Agreement (NDA)"
    print(f"  ✅ MarkItDown Engine: Successfully extracted {converted['metadata']['document_type']}")
    passed += 1

    # Test 2: Headroom Token & Context Optimization
    total += 1
    print("\n[TEST 2] Testing Headroom Token Optimization...")
    boilerplate_heavy_doc = (
        "# COMMERCIAL CONTRACT\n\n"
        "## CLAUSE 1: COVENANTS\nParty A shall deliver goods.\n\n"
        "## Counterparts\nThis Agreement may be executed in any number of counterparts.\n\n"
        "## Severability\nIf any provision is invalid, remaining provisions remain enforceable.\n\n"
        "Section 138 of the Negotiable Instruments Act, 1881 applies."
    )
    opt_result = headroom.optimize_context(boilerplate_heavy_doc, compress_boilerplate=True, preserve_citations=True)
    assert opt_result["tokens_saved"] > 0
    assert opt_result["preserved_citations_count"] >= 1
    print(f"  ✅ Headroom: Reduced tokens from {opt_result['original_tokens']} to {opt_result['optimized_tokens']} ({opt_result['reduction_percentage']} saved)")
    print(f"  ✅ Citations Preserved: {opt_result['preserved_citations_count']}")
    passed += 1

    # Test 3: Reference-Based Legal Style Adapter
    total += 1
    print("\n[TEST 3] Testing Reference-Based Style Adaptation...")
    archaic_doc = "WITNESSETH: WHEREAS the Parties hereinunder agree that Company shall..."
    style = legal_style_adapter.analyze_style(archaic_doc, "Old Firm Template")
    assert "Traditional Formal" in style["tone"]
    assert style["obligation_syntax"] == "shall"
    print(f"  ✅ Style Adapter: Successfully detected '{style['tone']}' with '{style['obligation_syntax']}' obligations")
    passed += 1

    # Test 4: Dynamic Legal Skills Framework
    total += 1
    print("\n[TEST 4] Testing Dynamic Legal Skills Registry...")
    skills = legal_skills_registry.list_skills()
    assert len(skills) >= 15
    nda_skill = legal_skills_registry.find_by_tag("@NDA")
    assert nda_skill is not None
    assert nda_skill.name == "NDA Drafting"
    print(f"  ✅ Skills Registry: Loaded {len(skills)} skills across 7 categories")
    print(f"  ✅ Tag Invocation: Resolved '@NDA' -> {nda_skill.name}")
    passed += 1

    # Test 5: Citation & Legal Authority Verification Engine
    total += 1
    print("\n[TEST 5] Testing Citation & Legal Authority Verification...")
    doc_with_citations = (
        "As held in Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1, privacy is a fundamental right. "
        "Also pursuant to Section 138 of the Negotiable Instruments Act, 1881, cheque dishonour entails penal consequences. "
        "Conversely, in Bogus Fabricated Corp v. Fictional State 999 SCC 000, unverified claims were made."
    )
    audit = citation_verifier.audit_document_citations(doc_with_citations)
    assert audit["verified_count"] >= 2
    assert audit["unverified_count"] >= 1
    print(f"  ✅ Citation Audit: {audit['verified_count']} Verified, {audit['partially_verified_count']} Partial, {audit['unverified_count']} Flagged")
    print(f"  ✅ Hallucination Guardrail: Triggered {audit['guardrail_status']}")
    passed += 1

    # Test 6: Prompt Strength Meter & Improvement
    total += 1
    print("\n[TEST 6] Testing Prompt Strength Meter & Legal Enhancer...")
    raw_prompt = "draft an nda"
    initial_score = prompt_enhancer.evaluate_strength(raw_prompt)
    enhanced = prompt_enhancer.improve_prompt(raw_prompt)
    assert enhanced["enhanced_score"] > initial_score["score"]
    print(f"  ✅ Prompt Meter: Initial {initial_score['score']}% -> Enhanced {enhanced['enhanced_score']}%")
    passed += 1

    # Test 7: Integrated Voice Agent & Consequential Safety Guard
    total += 1
    print("\n[TEST 7] Testing Voice Agent & Consequential Safety Guard...")
    safe_voice = voice_agent.parse_transcript("draft an nda")
    assert safe_voice["action"] == "activate_skill"
    assert safe_voice["skill_tag"] == "@NDA"
    print(f"  ✅ Voice Agent Command: 'draft an nda' -> Dispatched {safe_voice['skill_tag']}")

    dangerous_voice = voice_agent.parse_transcript("overwrite the draft")
    assert dangerous_voice["status"] == "confirmation_required"
    token = dangerous_voice["safety"]["token"]
    assert token is not None
    # Verify safety token consumption
    consumed = safety_guard.verify_and_consume(token)
    assert consumed is True
    print(f"  ✅ Consequential Safety Guard: Successfully gated destructive action with confirmation token")
    passed += 1

    # Test 8: Hiromi Higuruma Interactive Character Persona Engine
    total += 1
    print("\n[TEST 8] Testing Hiromi Higuruma Legal Defense Persona Engine...")
    from backend.core.higuruma_persona import higuruma_engine
    higuruma_response = higuruma_engine.generate_counsel(
        user_message="Cross-Examine this contract for loopholes",
        active_draft="# MUTUAL AGREEMENT\nParty A agrees to deliver goods."
    )
    assert higuruma_response["speaker"] == "Hiromi Higuruma"
    assert "Contract Act" in higuruma_response["response"] or "Judgeman" in higuruma_response["response"]
    assert higuruma_response["tactical_recommendation"] is not None
    print(f"  ✅ Higuruma Persona: Successfully generated tactical counsel from '{higuruma_response['speaker']}'")
    print(f"  ✅ Tactical Takeaway: {higuruma_response['tactical_recommendation'][:80]}...")
    passed += 1

    print("\n" + "=" * 70)
    print(f"🎉 ALL ARCHITECTURAL TESTS PASSED: {passed}/{total} (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
