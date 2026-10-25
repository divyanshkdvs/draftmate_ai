"""
Reference-Based Legal Style Adaptation Engine for DraftMate AI
Analyzes user-provided reference documents to extract drafting style, tone,
formatting conventions, numbering systems, and terminology patterns.
Applies these learned stylistic attributes to generated legal documents
without altering substantive legal meaning.
"""

import re
from typing import Dict, Any, List


class LegalStyleAdapter:
    """Extracts and adapts legal drafting styles from reference documents."""

    def analyze_style(self, reference_text: str, doc_name: str = "Reference Document") -> Dict[str, Any]:
        """Analyze text and extract stylistic parameters."""
        if not reference_text.strip():
            return self._default_style()

        lower = reference_text.lower()

        # 1. Tone Analysis
        archaic_keywords = ["witnesseth", "whereas", "hereinunder", "hereinafter", "aforementioned", "in witness whereof"]
        modern_keywords = ["the parties agree", "background", "definitions", "summary", "this agreement is between"]
        
        archaic_count = sum(1 for kw in archaic_keywords if kw in lower)
        modern_count = sum(1 for kw in modern_keywords if kw in lower)
        
        if archaic_count > modern_count:
            tone = "Traditional Formal Legalese (Formal, Recital-Heavy, Classical Phrasing)"
        elif modern_count > archaic_count:
            tone = "Modern Plain Legal (Clear, Active Voice, Modular Clauses)"
        else:
            tone = "Standard Institutional Commercial Legal"

        # 2. Numbering System
        if re.search(r"\bArticle\s+[IVXLCDM]+\b", reference_text):
            numbering = "Roman Numerals (Article I, Article II, Section 1.01)"
        elif re.search(r"^\d+\.\d+\.\d+", reference_text, re.MULTILINE):
            numbering = "Hierarchical Decimal (1.1.1, 1.1.2)"
        elif re.search(r"^\d+\.\d+", reference_text, re.MULTILINE):
            numbering = "Standard Decimal (1.1, 1.2, 1.3)"
        elif re.search(r"^\([a-z]\)", reference_text, re.MULTILINE):
            numbering = "Alphabetical Parenthetical ((a), (b), (c))"
        else:
            numbering = "Sequential Arabic (Clause 1, Clause 2)"

        # 3. Obligation Verbs
        shall_count = len(re.findall(r"\bshall\b", lower))
        will_count = len(re.findall(r"\bwill\b", lower))
        must_count = len(re.findall(r"\bmust\b", lower))
        agrees_to = len(re.findall(r"\bagrees to\b", lower))

        primary_obligation = "shall" if shall_count >= max(will_count, must_count, agrees_to) else "will / agrees to"

        # 4. Defined Terms Syntax
        quotes_count = len(re.findall(r'\"([A-Z][A-Za-z\s]+)\"', reference_text))
        paren_count = len(re.findall(r'\(([A-Z][A-Za-z\s]+)\)', reference_text))
        defined_terms_syntax = 'Double Quotes e.g. "Company"' if quotes_count >= paren_count else 'Parentheses e.g. (Company)'

        # 5. Latin Legal Maxims Usage
        latin_phrases = ["inter alia", "mutatis mutandis", "pari passu", "bona fide", "ipso facto", "pro rata", "force majeure"]
        detected_latin = [p for p in latin_phrases if p in lower]

        # 6. Governing Law Pattern
        gov_match = re.search(r"(?:governed by|construed in accordance with)\s+([A-Za-z\s,]+?)(?:\.|\;|\band)", reference_text, re.IGNORECASE)
        governing_pattern = gov_match.group(1).strip() if gov_match else "Laws of India / Relevant State"

        profile = {
            "source_reference": doc_name,
            "tone": tone,
            "numbering_system": numbering,
            "obligation_syntax": primary_obligation,
            "defined_terms_syntax": defined_terms_syntax,
            "latin_phrases_used": detected_latin,
            "governing_pattern": governing_pattern,
            "has_recitals": "whereas" in lower,
            "has_severability": "severability" in lower,
            "has_arbitration": "arbitration" in lower or "dispute resolution" in lower,
            "summary_directive": (
                f"Adopt a {tone} tone. Use {numbering} for clause numbering. "
                f"Express mandatory obligations using '{primary_obligation}'. "
                f"Format defined terms using {defined_terms_syntax}. "
                f"Include standard boilerplate structures matching the reference."
            )
        }

        return profile

    def _default_style(self) -> Dict[str, Any]:
        """Default professional legal drafting style."""
        return {
            "source_reference": "Default Professional Legal Standard",
            "tone": "Modern Commercial Legal (Clean, precise, enforceable)",
            "numbering_system": "Hierarchical Decimal (1.0, 1.1, 1.2)",
            "obligation_syntax": "shall",
            "defined_terms_syntax": 'Double Quotes e.g. "Purchaser"',
            "latin_phrases_used": ["force majeure", "mutatis mutandis"],
            "governing_pattern": "Standard Commercial Jurisdiction",
            "has_recitals": True,
            "has_severability": True,
            "has_arbitration": True,
            "summary_directive": "Use clean modern commercial legal language with standard decimal clause numbering and precise covenants."
        }


# Global Singleton Instance
legal_style_adapter = LegalStyleAdapter()
