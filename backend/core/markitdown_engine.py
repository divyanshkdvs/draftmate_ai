"""
Microsoft MarkItDown Document Processing Engine for DraftMate AI
Converts legal PDFs, DOCX, XLSX, PPTX, and text files into structured Markdown
with legal metadata extraction (parties, clauses, citations, defined terms).
"""

import os
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

# Try importing Microsoft markitdown
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class LegalMarkItDownEngine:
    """Document Ingestion & Markdown conversion engine powered by Microsoft MarkItDown."""

    def __init__(self):
        if MARKITDOWN_AVAILABLE:
            try:
                self.md_converter = MarkItDown()
            except Exception:
                self.md_converter = None
        else:
            self.md_converter = None

    def convert_file(self, file_path: str) -> Dict[str, Any]:
        """Convert a document file to structured Markdown with legal metadata."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        raw_markdown = ""
        conversion_method = "plain_fallback"

        # Attempt conversion with Microsoft MarkItDown
        if self.md_converter:
            try:
                result = self.md_converter.convert(str(path))
                raw_markdown = result.text_content
                conversion_method = "microsoft_markitdown"
            except Exception as e:
                raw_markdown = self._fallback_conversion(path)
                conversion_method = f"fallback ({str(e)})"
        else:
            raw_markdown = self._fallback_conversion(path)
            conversion_method = "custom_legal_parser"

        structured_md = self._clean_and_structure_legal_md(raw_markdown)
        metadata = self._extract_legal_metadata(structured_md, path.name)

        return {
            "filename": path.name,
            "extension": path.suffix.lower(),
            "conversion_method": conversion_method,
            "markdown": structured_md,
            "metadata": metadata,
            "size_bytes": path.stat().st_size
        }

    def convert_text(self, text: str, title: str = "Legal Document") -> Dict[str, Any]:
        """Convert raw text or paste to structured markdown with metadata."""
        structured_md = self._clean_and_structure_legal_md(text)
        metadata = self._extract_legal_metadata(structured_md, title)
        return {
            "filename": f"{title}.md",
            "extension": ".md",
            "conversion_method": "direct_text_processor",
            "markdown": structured_md,
            "metadata": metadata,
            "size_bytes": len(text.encode("utf-8"))
        }

    def _fallback_conversion(self, path: Path) -> str:
        """Handle DOCX, TXT, and PDF files when MarkItDown is unavailable or encounters an error."""
        suffix = path.suffix.lower()
        if suffix in [".docx", ".doc"] and DOCX_AVAILABLE:
            try:
                doc = docx.Document(str(path))
                lines = []
                for p in doc.paragraphs:
                    text = p.text.strip()
                    if not text:
                        continue
                    if p.style.name.startswith("Heading 1"):
                        lines.append(f"# {text}")
                    elif p.style.name.startswith("Heading 2"):
                        lines.append(f"## {text}")
                    elif p.style.name.startswith("Heading 3"):
                        lines.append(f"### {text}")
                    else:
                        lines.append(text)
                return "\n\n".join(lines)
            except Exception:
                pass

        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return f"# Document: {path.name}\n\n[Content extraction failed or binary file format]"

    def _clean_and_structure_legal_md(self, text: str) -> str:
        """Clean whitespace and ensure legal clause numbering and headers are properly formatted."""
        lines = text.splitlines()
        formatted_lines = []
        
        # Regex patterns for legal clauses: "1.", "Section 1", "Clause 2", "Article III", "WHEREAS,"
        recital_re = re.compile(r"^(WHEREAS|NOW, THEREFORE|IN WITNESS WHEREOF|NOW THIS AGREEMENT WITNESSETH)\b", re.IGNORECASE)
        clause_re = re.compile(r"^(SECTION|ARTICLE|CLAUSE)\s+([0-9IVXLCDM]+)[\.\:]?\s*(.*)", re.IGNORECASE)
        num_clause_re = re.compile(r"^(\d+\.\d*)\s+(.*)")

        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append("")
                continue

            # Detect Recitals
            if recital_re.match(stripped):
                formatted_lines.append(f"\n### {stripped}\n")
            # Detect Articles/Sections
            elif clause_re.match(stripped):
                m = clause_re.match(stripped)
                formatted_lines.append(f"\n## {m.group(1).upper()} {m.group(2)}: {m.group(3)}\n")
            # Detect Numbered Clauses like 1.1 or 2.
            elif num_clause_re.match(stripped):
                m = num_clause_re.match(stripped)
                formatted_lines.append(f"\n**{m.group(1)}** {m.group(2)}")
            else:
                formatted_lines.append(stripped)

        clean_text = "\n".join(formatted_lines)
        # Collapse multiple blank lines
        clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
        return clean_text.strip()

    def _extract_legal_metadata(self, markdown_text: str, filename: str) -> Dict[str, Any]:
        """Extract legal document classification, parties, defined terms, and citations."""
        # Detect document classification
        doc_type = "Legal Agreement"
        lower = markdown_text.lower()
        if "non-disclosure" in lower or "confidentiality agreement" in lower or "nda" in lower:
            doc_type = "Non-Disclosure Agreement (NDA)"
        elif "employment agreement" in lower or "employment contract" in lower:
            doc_type = "Employment Agreement"
        elif "share purchase" in lower or "spa" in lower:
            doc_type = "Share Purchase Agreement (SPA)"
        elif "legal notice" in lower or "notice under section" in lower:
            doc_type = "Legal Notice"
        elif "petition" in lower or "writ petition" in lower or "plaint" in lower:
            doc_type = "Court Petition / Plaint"
        elif "board resolution" in lower or "resolutions of the board" in lower:
            doc_type = "Board Resolution"
        elif "due diligence" in lower:
            doc_type = "Due Diligence Report"

        # Detect potential parties
        parties = []
        party_matches = re.findall(r"between\s+([A-Za-z0-9\s,\.\(\)]+?)\s+and\s+([A-Za-z0-9\s,\.\(\)]+?)(?:,\s*hereinafter|\.\s*WHEREAS)", markdown_text, re.IGNORECASE)
        if party_matches:
            parties = [p.strip() for p in party_matches[0] if p.strip()]

        # Detect jurisdiction / governing law
        jurisdiction = "Not specified"
        gov_match = re.search(r"(?:governed by|construed in accordance with)\s+the\s+laws\s+of\s+([A-Za-z\s]+?)(?:[\.,;]|\band\b)", markdown_text, re.IGNORECASE)
        if gov_match:
            jurisdiction = gov_match.group(1).strip()

        # Count clauses
        clauses = re.findall(r"(?:##\s*(?:SECTION|ARTICLE|CLAUSE)|\*\*\d+\.|\bSection\s+\d+)", markdown_text, re.IGNORECASE)

        # Count citations
        citations = re.findall(r"(?:\[\d{4}\]\s*\d+\s*[A-Z]+|\d{4}\s+SCC\s+\d+|AIR\s+\d{4}|Section\s+\d+\s+of\s+the|\d+\s+U\.S\.C\.)", markdown_text, re.IGNORECASE)

        return {
            "document_type": doc_type,
            "filename": filename,
            "parties": parties,
            "jurisdiction": jurisdiction,
            "clause_count": len(clauses),
            "citation_count": len(citations),
            "word_count": len(markdown_text.split()),
            "character_count": len(markdown_text)
        }


# Global Singleton Instance
legal_markitdown = LegalMarkItDownEngine()
