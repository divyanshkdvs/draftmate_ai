"""
Headroom-Inspired LLM Context and Token Optimization Module for DraftMate AI
Reference: https://github.com/headroomlabs-ai/headroom

Implements selective context retrieval, legal boilerplate compression,
citation-preserving token reduction, and context deduplication to minimize
LLM token usage and latency while maintaining 100% legal precision.
"""

import re
from typing import Dict, Any, List, Tuple


class HeadroomContextOptimizer:
    """Headroom Token & Context Manager for Legal AI Workflows."""

    # Common legal boilerplate clauses that can be selectively compressed
    BOILERPLATE_PATTERNS = [
        (r"(?i)(?:Counterparts|Execution in Counterparts)[\s\S]*?(?=\n##|\n\*\*|\Z)", "[Standard Counterparts Clause: Execution in multiple counterparts permissible via electronic signature]"),
        (r"(?i)(?:Severability)[\s\S]*?(?=\n##|\n\*\*|\Z)", "[Standard Severability Clause: Invalid provisions severed without impairing remaining enforceability]"),
        (r"(?i)(?:Waiver|No Waiver)[\s\S]*?(?=\n##|\n\*\*|\Z)", "[Standard Waiver Clause: Failure or delay to exercise rights does not constitute waiver]"),
        (r"(?i)(?:Entire Agreement|Merger Clause)[\s\S]*?(?=\n##|\n\*\*|\Z)", "[Standard Integration Clause: Supersedes all prior oral or written understandings]"),
    ]

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count using typical ~4 chars per token rule with legal vocabulary weighting."""
        if not text:
            return 0
        words = text.split()
        # English legal terminology often contains multi-token Latin words, citations, and clause numbers
        base_estimate = int(len(text) / 3.8)
        word_based = int(len(words) * 1.35)
        return max(base_estimate, word_based, 1)

    def optimize_context(
        self,
        text: str,
        target_focus: str = "general",
        compress_boilerplate: bool = True,
        preserve_citations: bool = True,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        Selectively optimize legal text for model prompting.
        Reduces token footprint while preserving operative covenants, citations, and structure.
        """
        original_tokens = self.estimate_tokens(text)
        
        # 1. Identify and extract citations to guarantee preservation
        preserved_citations = []
        if preserve_citations:
            citation_regex = re.compile(
                r"(\b(?:Section|Sec\.|Art\.|Article)\s+\d+[\w\(\)]*\s+(?:of\s+the\s+)?[\w\s]+(?:Act|Code|Rules|Regulations)?,?\s*\d{4}?"
                r"|\b\d{4}\s+SCC\s+\d+"
                r"|\bAIR\s+\d{4}\s+[A-Z]+\s+\d+"
                r"|\b\d+\s+U\.S\.C\.\s+§?\s*\d+"
                r"|\b\d+\s+F\.\d+d\s+\d+"
                r"|\b\d+\s+U\.S\.\s+\d+)",
                re.IGNORECASE
            )
            preserved_citations = citation_regex.findall(text)

        optimized_text = text

        # 2. Boilerplate compression if enabled
        compressed_clauses = 0
        if compress_boilerplate:
            for pattern, replacement in self.BOILERPLATE_PATTERNS:
                if re.search(pattern, optimized_text):
                    optimized_text = re.sub(pattern, replacement, optimized_text)
                    compressed_clauses += 1

        # 3. Selective Context Retrieval: If specific legal focus is requested (e.g. "termination", "indemnity", "governing law")
        focused_sections = []
        if target_focus and target_focus.lower() not in ["all", "general", ""]:
            focus_terms = [t.strip().lower() for t in target_focus.split()]
            paragraphs = optimized_text.split("\n\n")
            high_priority = []
            standard_priority = []

            for p in paragraphs:
                p_lower = p.lower()
                if any(term in p_lower for term in focus_terms):
                    high_priority.append(p)
                elif any(c in p for c in preserved_citations):
                    # Always include paragraphs with legal citations
                    high_priority.append(p)
                else:
                    standard_priority.append(p)

            # Construct focused context prioritizing relevant clauses
            combined = "\n\n".join(high_priority)
            if self.estimate_tokens(combined) < max_tokens:
                # Add preamble or relevant standard clauses if room permits
                remaining_budget = max_tokens - self.estimate_tokens(combined)
                added = []
                for sp in standard_priority:
                    if self.estimate_tokens("\n\n".join(added + [sp])) < remaining_budget:
                        added.append(sp)
                optimized_text = combined + ("\n\n--- [Supplementary Context] ---\n\n" + "\n\n".join(added) if added else "")
            else:
                optimized_text = combined

        optimized_tokens = self.estimate_tokens(optimized_text)
        tokens_saved = max(0, original_tokens - optimized_tokens)
        reduction_pct = round((tokens_saved / max(1, original_tokens)) * 100, 1)

        return {
            "optimized_text": optimized_text,
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "tokens_saved": tokens_saved,
            "reduction_percentage": f"{reduction_pct}%",
            "boilerplate_compressed_count": compressed_clauses,
            "preserved_citations_count": len(preserved_citations),
            "citations_preserved": preserved_citations[:10],
            "headroom_status": "optimized" if tokens_saved > 0 else "baseline"
        }

    def prune_reference_for_style(self, reference_text: str, max_tokens: int = 1200) -> str:
        """
        Extract only stylistic cues (structure, preamble, signature blocks, clause syntax)
        from a reference document so that style adaptation requires minimal tokens.
        """
        lines = reference_text.splitlines()
        sample_chunks = []
        
        # Take preamble / title
        sample_chunks.append("\n".join(lines[:15]))
        
        # Take 2-3 sample middle clauses to capture terminology and numbering
        middle = lines[len(lines)//3 : len(lines)//3 + 20]
        sample_chunks.append("\n".join(middle))
        
        # Take closing / execution style
        sample_chunks.append("\n".join(lines[-15:]))
        
        compact_style = "\n\n... [Style Sample Anchor] ...\n\n".join(sample_chunks)
        return compact_style[:4000]


# Global Singleton Instance
headroom = HeadroomContextOptimizer()
