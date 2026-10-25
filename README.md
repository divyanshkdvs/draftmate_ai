# ⚖️ DraftMate AI &bull; Legal Intelligence Studio
> **Kodekurrent Season 2 Hackathon — Rajiv Gandhi Institute of Petroleum Technology (RGIPT)**  
> *Category:* Software | *Theme:* Artificial Intelligence (AI) | LegalTech | Natural Language Processing | AI Agents | Voice AI  
> *Design Paradigm:* **Harvey.ai Luxury Legal Aesthetic** (Warm Near-Black `#0F0E0D`, Restrained Ambers `#C5A880`, Editorial Display Serif & Diatype-style Grotesk)

---

## 🏛️ Executive Summary

**DraftMate AI** is a sovereign legal drafting and verification studio designed for corporate law firms, advocates, and judicial researchers. 

The studio adopts the visual design language of **Harvey.ai**:
- **Palette:** Warm, deep ink canvas (`#0F0E0D`), elevated charcoal surfaces (`#161514`), muted gray-brown secondary text (`#8E8A82`), and warm brass/amber accents (`#C5A880`).
- **Typography:** High-contrast editorial display serif (**Cormorant Garamond**) paired with neutral, highly legible contemporary grotesque sans-serif (**Plus Jakarta Sans** / **Inter**) and **JetBrains Mono** for statutory codes.
- **Unified Action Dock:** Prompt input, file attachments (Microsoft MarkItDown), spoken voice dictation, and the generate/draft button are cleanly aligned in a single sleek horizontal dock bar.
- **Hiromi Higuruma Defense Chamber:** An animated mechanical scale emblem, live docket ticker, and interactive cross-examination companion drawer.

### 🌟 Key Pillars:
1. **Minimalist Courtroom Workspace:** Stripped of AI clutter. Houses only the 5 essential hackathon workflows:
   - ⚖️ **Contract Drafting** (`@ContractDrafting`)
   - 📜 **Legal Notice** (`@LegalNotice`)
   - 🏛️ **Court Petition** (`@PetitionDrafting`)
   - 🔍 **Contract Review & Redline** (`@ContractReview`)
   - 📚 **Case Law & Statutory Research** (`@CaseLawResearch`)
2. **Special Feature: "Consult Higuruma" (Interactive Character Companion):**
   - Direct, in-character legal consultation with defense attorney **Hiromi Higuruma** (master of the domain *Deadly Sentencing* 誅伏賜死).
   - Scrutinizes contracts from opposing counsel's viewpoint, cross-examines indemnities and notice traps under the *Indian Contract Act* and *Evidence Act*, and outputs one-click remedial drafting clauses.
3. **Microsoft MarkItDown Ingestion:** Clean conversion of PDFs, DOCX, and templates into structured legal Markdown with automatic metadata extraction.
4. **Headroom Context & Token Optimization:** Boilerplate pruning and operative covenant extraction, saving 30%–50% in LLM tokens while strictly preserving citations.
5. **Citation & Authority Verification Desk:** Categorizes citations into **VERIFIED**, **PARTIALLY VERIFIED**, and **UNVERIFIED / FLAGGED** states with hyperlinked official gazette/Supreme Court records and Judgeman anti-hallucination alerts.
6. **Voice Agent & Consequential Safety Guard:** Dictation and spoken workflows with confirmation tokens required before executing destructive actions (e.g. overwriting drafts).

---

## 📸 Reference Architecture & Layout Alignment

The implementation faithfully matches the Kodekurrent Season 2 reference layout:

| Ref # | Feature Component | Implementation Details |
| :--- | :--- | :--- |
| **1** | **ChatGPT-Style Workspace** | Minimal, familiar interface to chat, upload documents, and invoke legal skills. |
| **2** | **Model Selection** | Multi-model switcher: Claude 3.5 Sonnet (Advanced), GPT-4o (Balanced), Claude 3 Haiku (Quick), DeepSeek R1 (Reasoning), DraftMate Legal Core (Local/Private). |
| **3** | **Integrated Voice Agent** | Microphone button in header opening voice modal with animated waveform, speech dictation, and voice commands. |
| **4** | **Document Management** | Attachment pills inside prompt box (`+ Add from Device`, `Add from DraftMate Documents`), plus right-side slide-over panel with matters, templates, and MarkItDown preview. |
| **5** | **Tools & Options** | Web search toggle, legal skills library drawer trigger, and direct voice input shortcut. |
| **6** | **Send Prompt** | Circular blue arrow button initiating legal drafting, token optimization, and citation audit. |
| **7** | **Legal Skills Quick Chips** | Quick action chips (`Contract Review`, `Redlining`, `Legal Research`, `Agreement Drafting`, `Case Analysis`, `Legal Notice`, `Summarize`, `Due Diligence`, `More...`). |
| **8** | **Prompt Meter & Enhancement** | Dynamic percentage score (e.g., `72%`), feedback tip, and `+ Improve Prompt` button that enriches prompts with jurisdiction, governing statutes, and liability caps. |
| **8b** | **Complete Legal Skills Library** | Modal grid with filter tabs (`All Skills`, `For Lawyers`, `For Law Students`) organizing 60+ skills across 7 categories. |

---

## 📁 Project Directory Structure

```
draftmate-ai/
├── run.py                          # One-click application launcher
├── test_suite.py                   # Automated architectural validation suite
├── requirements.txt                # Python backend dependencies
├── package.json                    # Root package configuration
├── README.md                       # Comprehensive system documentation
│
├── backend/                        # FastAPI High-Performance Backend
│   ├── main.py                     # App factory, CORS, static file mounts, routes
│   ├── core/
│   │   ├── markitdown_engine.py    # Microsoft MarkItDown ingestion & legal metadata
│   │   ├── headroom.py             # Headroom token & context optimization
│   │   ├── style_adapter.py        # Reference-based legal style & tone adapter
│   │   ├── prompt_enhancer.py      # Prompt strength meter (0-100%) & legal enhancer
│   │   └── ai_engine.py            # Multi-model LLM orchestrator & local fallback
│   ├── skills/
│   │   └── registry.py             # Dynamic Legal Skills Framework (Awesome Legal Skills / Claude for Legal)
│   ├── verification/
│   │   ├── citation_engine.py      # Citation extractor & verification against authority DB
│   │   └── authority_db.py         # Indexed landmark precedents (SCC, AIR, US) & statutes (Contract Act, BNS, DPDP)
│   ├── voice/
│   │   ├── voice_agent.py          # Voice command interpreter & task dispatcher
│   │   └── safety_guard.py         # Consequential action safety token verification
│   ├── documents/
│   │   ├── samples/                # Preloaded matters: Employment Agreement, NDA, Board Resolution, SPA, etc.
│   │   └── storage/                # Uploaded files storage
│   └── api/
│       ├── routes_chat.py          # Chat, drafting execution, and redline diff endpoints
│       ├── routes_skills.py        # Skills listing, search, and tag lookups
│       ├── routes_documents.py     # Document upload, MarkItDown parsing, samples
│       ├── routes_prompt.py        # Prompt evaluation and enhancement
│       ├── routes_citations.py     # Citation audit and authority stats
│       └── routes_voice.py         # Voice parsing and safety confirmation
│
└── frontend/                       # Interactive Frontend (React SPA & Next.js Components)
    ├── index.html                  # Responsive Tailwind CSS layout matching reference mockup
    ├── static/
    │   └── app.js                  # Frontend client engine (reactive state, audio visualizer, diff renderer)
    ├── package.json                # Next.js / React component deliverables
    └── src/
        └── components/
            ├── Sidebar.tsx          # Navigation sidebar component
            ├── Header.tsx           # Top navigation with model selector & voice trigger
            ├── PromptMeter.tsx      # Prompt strength gauge & improve action
            ├── DocumentPanel.tsx    # DraftMate documents slide-over drawer
            ├── CitationInspector.tsx# Verification badges, links, and guardrail alerts
            └── VoiceAgentModal.tsx  # Voice recording modal with waveform
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.15)
- Standard modern web browser (Chrome, Edge, Firefox, Safari)

### 2. Installation
Clone the repository or navigate to the directory:
```bash
cd draftmate-ai
pip install -r requirements.txt
```

### 3. Run Automated Architectural Tests
Execute the end-to-end validation test suite:
```bash
python test_suite.py
```
*Output: Validates MarkItDown document conversion, Headroom token savings, Style adaptation, Skills tag lookup, Citation verification, Prompt strength scoring, and Voice safety tokens.*

### 4. Launch Legal Drafting Studio
Start the studio server:
```bash
python run.py
```

Open your browser at:
- **Studio Interface:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔄 End-to-End User Journey

1. **Select or Activate a Legal Skill**:
   - Type `@` in the chat input or click one of the quick chips (e.g. `Contract Review`, `Redlining`, `@NDA`, `@LegalNotice`).
   - Or click **View All Skills** to explore the 60+ categorized skills library.
2. **Prompt Strength Scoring & One-Click Improvement**:
   - Type your draft instruction (e.g. `draft an agreement between Apex and Quantum`).
   - Observe the **Prompt Strength Meter** dynamically update in real time.
   - Click **+ Improve Prompt**: DraftMate automatically inserts governing jurisdiction, dispute resolution under the *Arbitration and Conciliation Act, 1996*, indemnification caps, and compliance with the *Digital Personal Data Protection Act, 2023*.
3. **Attach Reference Documents for Style Adaptation**:
   - Open **DraftMate Documents** panel and select `Employment Agreement.pdf` or `NDA.pdf`, or click `+ Add from Device` to upload a custom PDF/DOCX.
   - Check **Learn & Adapt Drafting Style**. Microsoft MarkItDown parses the file into clean Markdown and extracts stylistic cues (tone, clause numbering, and defined terms).
4. **Synthesize Legal Draft with Token Optimization**:
   - Select your preferred model (e.g. *Claude 3.5 Sonnet* or *GPT-4o*).
   - Click **Send Prompt**: Headroom optimizes context by pruning boilerplate and preserving operative covenants and citations.
   - The document is synthesized and displayed in the **Drafting Studio**.
5. **Inspect Verified Citations & Guardrails**:
   - Click the **Citations Audit** tab.
   - Review **VERIFIED** citations (with links to Supreme Court of India judgments or India Code acts), **PARTIALLY VERIFIED** entries, and **UNVERIFIED / FLAGGED** citations with anti-hallucination alerts.
6. **Review Redline Markup**:
   - Click the **Redline Diff** tab to visualize strike-through deletions and highlighted additions between versions.
7. **Voice Control & Safety Confirmation**:
   - Click **Voice Agent** to dictate instructions.
   - Spoken commands like `"draft an NDA"` or `"verify citations"` execute instantly.
   - Consequential commands like `"overwrite draft"` or `"delete document"` trigger the **Safety Confirmation Modal** requiring explicit verification before changes take effect.
8. **Export**:
   - Export your finished document as **Markdown (.md)**, **Word (.doc/.docx)**, or **Print / Save as PDF**.

---

## 📚 Technical References

1. **Claude for Legal — Legal Workflow Plugins**:  
   Modular legal task designs and specialized prompting conventions.  
   Reference: `https://github.com/anthropics/claude-for-legal`
2. **Awesome Legal Skills — Legal Agent Skills Library**:  
   Comprehensive categorization of reusable legal skills across lawyers and students.  
   Reference: `https://github.com/lawve-ai/awesome-legal-skills`
3. **Microsoft MarkItDown**:  
   Document-to-Markdown conversion for PDFs, DOCX, XLSX, and presentation files.  
   Reference: `https://github.com/microsoft/markitdown`
4. **Headroom — LLM Context and Token Optimisation**:  
   Selective context retrieval, boilerplate pruning, and token optimization.  
   Reference: `https://github.com/headroomlabs-ai/headroom`
5. **VoxCPM2 & OpenWhispr**:  
   Voice interaction, speech recognition, and consequential command gating.  
   References: `https://voxcpm.net` & `https://github.com/OpenWhispr/openwhispr`
6. **DraftMate AI**:  
   Official product reference: `https://www.draftmate.in`

---

*Crafted for the Kodekurrent Season 2 Hackathon at Rajiv Gandhi Institute of Petroleum Technology (RGIPT).*
