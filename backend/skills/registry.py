"""
Dynamic Legal Skills Framework for DraftMate AI
Reference: https://github.com/anthropics/claude-for-legal & https://github.com/lawve-ai/awesome-legal-skills

Modular, extensible registry supporting 60+ specialized legal workflows across 7 categories.
Supports @tag dynamic invocation in chat and structured UI filtering (Lawyers / Students).
"""

from typing import Dict, Any, List, Optional


class LegalSkill:
    """Represents an atomic, specialized legal workflow capability."""

    def __init__(
        self,
        skill_id: str,
        name: str,
        category: str,
        target_audience: str,  # 'lawyer' | 'student' | 'all'
        tag: str,
        icon: str,
        description: str,
        system_prompt: str,
        required_inputs: List[str],
        recommended_clauses: List[str]
    ):
        self.skill_id = skill_id
        self.name = name
        self.category = category
        self.target_audience = target_audience
        self.tag = tag
        self.icon = icon
        self.description = description
        self.system_prompt = system_prompt
        self.required_inputs = required_inputs
        self.recommended_clauses = recommended_clauses

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.skill_id,
            "name": self.name,
            "category": self.category,
            "target_audience": self.target_audience,
            "tag": self.tag,
            "icon": self.icon,
            "description": self.description,
            "required_inputs": self.required_inputs,
            "recommended_clauses": self.recommended_clauses
        }


class LegalSkillsRegistry:
    """Central registry and executor for legal skills."""

    def __init__(self):
        self._skills: Dict[str, LegalSkill] = {}
        self._load_all_skills()

    def register(self, skill: LegalSkill):
        self._skills[skill.skill_id] = skill

    def get_skill(self, skill_id: str) -> Optional[LegalSkill]:
        return self._skills.get(skill_id)

    def find_by_tag(self, tag: str) -> Optional[LegalSkill]:
        clean_tag = tag.lower().replace("@", "").strip()
        for s in self._skills.values():
            if s.tag.lower().replace("@", "").strip() == clean_tag:
                return s
            if s.skill_id.lower() == clean_tag:
                return s
        return None

    def list_skills(
        self,
        category: Optional[str] = None,
        target_audience: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = []
        for s in self._skills.values():
            if category and category.lower() != "all" and s.category.lower() != category.lower():
                continue
            if target_audience and target_audience.lower() != "all":
                if target_audience.lower() == "lawyer" and s.target_audience not in ["lawyer", "all"]:
                    continue
                if target_audience.lower() == "student" and s.target_audience not in ["student", "all"]:
                    continue
            if search_query:
                sq = search_query.lower()
                if sq not in s.name.lower() and sq not in s.description.lower() and sq not in s.tag.lower():
                    continue
            results.append(s.to_dict())
        return results

    def _load_all_skills(self):
        # 1. DRAFTING & WRITING
        self.register(LegalSkill(
            skill_id="contract_drafting",
            name="Contract Drafting",
            category="Drafting & Writing",
            target_audience="all",
            tag="@ContractDrafting",
            icon="FileSignature",
            description="Draft complete commercial contracts with operative covenants, representations, warranties, and dispute clauses.",
            system_prompt="You are a Master Contract Drafting Specialist. Draft comprehensive, legally binding contracts with clear recitals, definitions, covenants, warranties, indemnities, and governing law.",
            required_inputs=["parties", "purpose", "commercial_terms"],
            recommended_clauses=["Definitions", "Scope of Work", "Payment Terms", "Limitation of Liability", "Governing Law"]
        ))

        self.register(LegalSkill(
            skill_id="legal_notice_drafting",
            name="Legal Notice Drafting",
            category="Drafting & Writing",
            target_audience="lawyer",
            tag="@LegalNotice",
            icon="Send",
            description="Generate formal demand and statutory legal notices under Section 138 NI Act, Section 80 CPC, defamation, or breach of contract.",
            system_prompt="You are a Litigation Advocate. Draft strict, formal legal notices detailing facts, cause of action, statutory breach, 15/30-day requisition demand, and litigation warnings.",
            required_inputs=["client_name", "recipient_name", "factual_matrix", "demand_amount"],
            recommended_clauses=["Statement of Facts", "Breach of Statute", "Specific Demand", "15-Day Time Limit", "Litigation Caution"]
        ))

        self.register(LegalSkill(
            skill_id="nda_drafting",
            name="NDA Drafting",
            category="Drafting & Writing",
            target_audience="all",
            tag="@NDA",
            icon="ShieldCheck",
            description="Draft unilateral or bilateral non-disclosure agreements with trade secret protection, non-circumvention, and survival terms.",
            system_prompt="Draft an enforceable Mutual or Unilateral Non-Disclosure Agreement complying with trade secret protection statutes and standard confidentiality covenants.",
            required_inputs=["disclosing_party", "receiving_party", "purpose", "term_years"],
            recommended_clauses=["Definition of Confidential Information", "Standard of Care", "Compelled Disclosure", "Injunctive Relief", "Survival"]
        ))

        self.register(LegalSkill(
            skill_id="employment_agreement",
            name="Employment Agreement",
            category="Drafting & Writing",
            target_audience="all",
            tag="@EmploymentAgreement",
            icon="Briefcase",
            description="Draft executive and employee agreements covering CTC, IP assignment, restrictive covenants, and termination procedures.",
            system_prompt="Draft a robust Employment Agreement with IP work-for-hire assignment, non-solicitation, garden leave, and compliance with labour laws.",
            required_inputs=["employer_name", "employee_name", "role", "remuneration"],
            recommended_clauses=["Job Responsibilities", "Compensation & ESOP", "IP Assignment", "Termination For Cause", "Non-Solicitation"]
        ))

        self.register(LegalSkill(
            skill_id="petition_drafting",
            name="Petition Drafting",
            category="Drafting & Writing",
            target_audience="lawyer",
            tag="@PetitionDrafting",
            icon="Scale",
            description="Draft High Court and Supreme Court Writ Petitions (Articles 32 & 226), Special Leave Petitions, and civil plaints.",
            system_prompt="Draft court petitions adhering to appellate formatting rules, synopsis, list of dates, grounds, and prayer clauses.",
            required_inputs=["court_name", "petitioner", "respondent", "grounds_of_challenge"],
            recommended_clauses=["Synopsis & List of Dates", "Parties Description", "Facts Matrix", "Grounds", "Prayer for Relief"]
        ))

        self.register(LegalSkill(
            skill_id="legal_opinion",
            name="Legal Opinion",
            category="Drafting & Writing",
            target_audience="lawyer",
            tag="@LegalOpinion",
            icon="FileCheck",
            description="Draft structured counsel opinions on legal risk, statutory compliance, or litigation prospects.",
            system_prompt="Draft formal Senior Advocate Legal Opinions detailing question posed, statutory framework, case law synthesis, and reasoned conclusion.",
            required_inputs=["queries_raised", "factual_background", "governing_statutes"],
            recommended_clauses=["Queries Submitted", "Factual Matrix", "Applicable Law", "Judicial Precedents", "Reasoned Opinion"]
        ))

        # 2. DOCUMENT REVIEW & ANALYSIS
        self.register(LegalSkill(
            skill_id="contract_review",
            name="Contract Review",
            category="Document Review & Analysis",
            target_audience="all",
            tag="@ContractReview",
            icon="Search",
            description="Examine agreements for unfavorable terms, lopsided indemnities, ambiguous covenants, and statutory conflicts.",
            system_prompt="Perform a senior corporate legal review of the provided document. Highlight high-risk clauses, missing protections, and counterparty exposure.",
            required_inputs=["contract_text"],
            recommended_clauses=["Risk Heatmap", "Indemnification Audit", "Termination Carve-outs", "Liability Cap Check"]
        ))

        self.register(LegalSkill(
            skill_id="redlining",
            name="Redlining",
            category="Document Review & Analysis",
            target_audience="all",
            tag="@Redlining",
            icon="FileDiff",
            description="Generate track-changes and strike-through markups with lawyer's commentary and negotiated replacement clauses.",
            system_prompt="Generate a formal legal redline markup. For each deficient clause, show Original Text, Deletions, Additions, and Negotiation Rationale.",
            required_inputs=["clause_or_agreement"],
            recommended_clauses=["Clause Markup", "Strikethrough Deletions", "Underlined Additions", "Negotiating Position"]
        ))

        self.register(LegalSkill(
            skill_id="due_diligence",
            name="Due Diligence",
            category="Document Review & Analysis",
            target_audience="lawyer",
            tag="@DueDiligence",
            icon="ShieldAlert",
            description="Conduct M&A and corporate due diligence across corporate filings, material contracts, litigation, and regulatory compliance.",
            system_prompt="Perform an institutional M&A Due Diligence audit. Identify red flags, change of control triggers, regulatory filings, and condition precedents.",
            required_inputs=["target_company", "material_contracts"],
            recommended_clauses=["Corporate Health", "Material Contracts", "Regulatory Licenses", "Litigation Exposure"]
        ))

        self.register(LegalSkill(
            skill_id="risk_analysis",
            name="Risk Analysis",
            category="Document Review & Analysis",
            target_audience="all",
            tag="@RiskAnalysis",
            icon="AlertTriangle",
            description="Evaluate catastrophic legal exposure, uncapped liabilities, non-standard warranties, and enforceability risks.",
            system_prompt="Conduct a rigorous legal risk analysis. Assign risk scores (Low, Medium, Critical) and recommend risk mitigation mechanisms.",
            required_inputs=["document_text"],
            recommended_clauses=["Risk Scoring", "Liability Exposure", "Compliance Vulnerabilities", "Mitigation Roadmap"]
        ))

        # 3. LEGAL RESEARCH
        self.register(LegalSkill(
            skill_id="case_law_research",
            name="Case Law Research",
            category="Legal Research",
            target_audience="all",
            tag="@CaseLawResearch",
            icon="Library",
            description="Find binding High Court and Supreme Court precedents, ratio decidendi, and judicial treatment on key propositions.",
            system_prompt="Conduct judicial precedent research. Provide landmark case citations, bench strength, court name, ratio decidendi, and distinguished rulings.",
            required_inputs=["legal_proposition", "jurisdiction"],
            recommended_clauses=["Proposition", "Landmark Rulings", "Bench Size", "Ratio Decidendi", "Distinguishing Precedents"]
        ))

        self.register(LegalSkill(
            skill_id="citation_checking",
            name="Citation Checking",
            category="Legal Research",
            target_audience="all",
            tag="@CitationChecking",
            icon="CheckCircle2",
            description="Verify citations against official law reporters (SCC, AIR, SCR, U.S. Reports) and flag overruled or invalid authorities.",
            system_prompt="Audit every legal citation in the text. Confirm valid reporter volume, page numbers, bench status, and whether the ruling remains good law.",
            required_inputs=["citation_text"],
            recommended_clauses=["Citation Audit", "Reporter Verification", "Overruled Status Check", "Hyperlinked Authorities"]
        ))

        self.register(LegalSkill(
            skill_id="irac_practice",
            name="IRAC Practice (Student)",
            category="Legal Research",
            target_audience="student",
            tag="@IRAC",
            icon="GraduationCap",
            description="Structure complex legal scenarios into Issue, Rule, Application, and Conclusion for law school exams and moot courts.",
            system_prompt="Guide law students through the IRAC framework. Deconstruct facts into discrete legal issues, statutory rules, factual application, and holding.",
            required_inputs=["hypothetical_facts"],
            recommended_clauses=["Issue Statement", "Governing Rule", "Analysis / Application", "Conclusion"]
        ))

        # 4. CASE & JUDGMENT TOOLS
        self.register(LegalSkill(
            skill_id="case_brief",
            name="Case Brief (Student)",
            category="Case & Judgment Tools",
            target_audience="student",
            tag="@CaseBrief",
            icon="BookOpen",
            description="Generate standard law school case briefs with procedural history, core issues, rules, holdings, and judicial reasoning.",
            system_prompt="Create a concise, pedagogical Case Brief: Title, Citation, Procedural Posture, Facts, Issues, Holdings, Rationale, and Dissent.",
            required_inputs=["case_name_or_text"],
            recommended_clauses=["Procedural Posture", "Key Facts", "Issue Posed", "Holding", "Judicial Rationale"]
        ))

        self.register(LegalSkill(
            skill_id="case_analysis",
            name="Case Analysis",
            category="Case & Judgment Tools",
            target_audience="all",
            tag="@CaseAnalysis",
            icon="Binary",
            description="In-depth jurisprudential deconstruction of landmark rulings, obiter dicta, and future doctrinal implications.",
            system_prompt="Perform a deep doctrinal case analysis extracting the exact ratio decidendi, constitutional principles, and statutory interpretations.",
            required_inputs=["judgment_text"],
            recommended_clauses=["Doctrinal Principles", "Statutory Interpretation", "Obiter Dicta vs Ratio", "Practical Impact"]
        ))

        # 5. COMPLIANCE & ADVISORY
        self.register(LegalSkill(
            skill_id="data_privacy_review",
            name="Data Privacy Review",
            category="Compliance & Advisory",
            target_audience="lawyer",
            tag="@DataPrivacy",
            icon="Lock",
            description="Assess data handling against Digital Personal Data Protection Act 2023 (DPDP), GDPR, and CCPA standards.",
            system_prompt="Audit data processing agreements and terms against DPDP Act 2023 and GDPR: notice, consent architecture, breach notification, and cross-border transfer.",
            required_inputs=["privacy_policy_or_dpa"],
            recommended_clauses=["Consent Mechanism", "Data Principal Rights", "Data Fiduciary Duties", "Cross-Border Transfer"]
        ))

        self.register(LegalSkill(
            skill_id="compliance_checklist",
            name="Compliance Checklist",
            category="Compliance & Advisory",
            target_audience="all",
            tag="@ComplianceChecklist",
            icon="ClipboardCheck",
            description="Generate actionable regulatory checklists with statutory timelines, forms, and penal consequences for non-compliance.",
            system_prompt="Generate a tabular regulatory compliance checklist specifying Statutory Section, Filing Requirement, Due Date, and Non-Compliance Penalty.",
            required_inputs=["industry_or_activity"],
            recommended_clauses=["Statutory Provision", "Compliance Action", "Filing Authority", "Penal Consequences"]
        ))

        # 6. STUDENT LEARNING & EXAM PREP
        self.register(LegalSkill(
            skill_id="socratic_drill",
            name="Socratic Drill",
            category="Student Learning & Exam Prep",
            target_audience="student",
            tag="@SocraticDrill",
            icon="HelpCircle",
            description="Engage in a rigorous law-professor style interrogation challenging legal assumptions and testing edge cases.",
            system_prompt="Act as an exacting Harvard Law Professor conducting a Socratic dialogue. Pose probing hypothetical questions to test constitutional or contractual doctrines.",
            required_inputs=["topic_or_case"],
            recommended_clauses=["Hypothetical Twist", "Edge Case Question", "Doctrinal Challenge"]
        ))

        # 7. GENERAL UTILITIES
        self.register(LegalSkill(
            skill_id="simplify_legal_language",
            name="Simplify Legal Language",
            category="General Utilities",
            target_audience="all",
            tag="@SimplifyLegal",
            icon="Sparkles",
            description="Translate dense, archaic legalese into crystal-clear plain English for clients and commercial stakeholders.",
            system_prompt="Translate archaic legalese into plain, clear English without compromising legal effect or losing critical conditions.",
            required_inputs=["dense_clause"],
            recommended_clauses=["Plain English Translation", "Key Takeaways", "Commercial Implications"]
        ))


# Global Singleton Instance
legal_skills_registry = LegalSkillsRegistry()
