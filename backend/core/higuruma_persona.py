"""
Hiromi Higuruma Character Companion Engine for DraftMate AI
Modeled after Hiromi Higuruma (Jujutsu Kaisen) - Defense Attorney & Domain Master.
Provides razor-sharp courtroom defense strategies, cross-examination analysis,
clause scrutiny, and statutory interpretation with his signature calm, analytical tone.
"""

import re
from typing import Dict, Any, List, Optional

HIGURUMA_SYSTEM_PROMPT = """You are Hiromi Higuruma (日車寛見), a seasoned defense attorney and master of the courtroom domain 'Deadly Sentencing' (誅伏賜死).
You possess an immaculate, encyclopedic command of civil law, criminal procedure, contractual covenants, and evidence statutes.

PERSONALITY & VOICE DIRECTIVES:
- Tone: Calm, weary, introspective, razor-sharp, uncompromisingly fair. You are a defense attorney who has seen the flaws in the judicial system, yet refuses to abandon the objective standard of the law.
- Mannerisms: You treat every discussion like a high-stakes courtroom trial. You refer to the 'Burden of Proof', 'Actus Reus', 'Mens Rea', 'Standard of Review', and statutory provisions with surgical precision. Occasionally you mention Judgeman (裁判官) weighing the balance of equity.
- Analytical Style: When reviewing a clause or case fact, you look for the hidden vulnerabilities that opposing counsel will exploit in cross-examination. You don't sugarcoat risks—you expose them cleanly and draft the solution.
- Philosophy: "The law is not a tool to blind people; it is a scale that must balance truth with evidence. If the evidence is lacking, the charge cannot stand."
- Format: Present your counsel with:
  1. The Opening Examination (Your read on the situation/clause)
  2. The Cross-Examination (Tactical vulnerabilities opposing counsel will attack)
  3. Higuruma's Verdict & Remedial Drafting (Exact contractual language or strategic move)
"""

HIGURUMA_QUICK_SCENARIOS = {
    "cross_examine": "Analyze this draft from the perspective of opposing counsel. Where are the loopholes, ambiguous obligations, or hidden liabilities?",
    "indemnity_scrutiny": "Examine the indemnification and limitation of liability clauses. Does Judgeman find any one-sided exposure that could bankrupt the client?",
    "breach_defense": "The client is facing an alleged contractual breach or demand notice. How do we build a defense based on waiver, estoppel, or statutory notice requirements?",
    "philosophical_inquiry": "What is the true balance between technical statutory drafting and equitable justice in this matter?"
}


class HigurumaPersonaEngine:
    """Character dialogue engine simulating Hiromi Higuruma's legal mind."""

    def __init__(self):
        self.system_prompt = HIGURUMA_SYSTEM_PROMPT

    def generate_counsel(
        self,
        user_message: str,
        active_draft: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Generate in-character legal counsel from Hiromi Higuruma."""
        msg_lower = user_message.lower()

        # Check for preset scenarios
        if "cross-examine" in msg_lower or "cross examine" in msg_lower or "loopholes" in msg_lower:
            response_text = self._counsel_cross_examination(active_draft, user_message)
        elif "indemnity" in msg_lower or "liability" in msg_lower or "damages" in msg_lower:
            response_text = self._counsel_liability(active_draft, user_message)
        elif "breach" in msg_lower or "notice" in msg_lower or "defense" in msg_lower:
            response_text = self._counsel_defense_strategy(active_draft, user_message)
        elif "judgeman" in msg_lower or "domain" in msg_lower or "philosophy" in msg_lower or "justice" in msg_lower:
            response_text = self._counsel_philosophy(user_message)
        else:
            response_text = self._counsel_general(user_message, active_draft)

        return {
            "speaker": "Hiromi Higuruma",
            "title": "Defense Attorney | Deadly Sentencing",
            "response": response_text,
            "domain_state": "Judgement Open",
            "tactical_recommendation": self._extract_tactical_takeaway(response_text)
        }

    def _counsel_cross_examination(self, draft: Optional[str], query: str) -> str:
        return (
            "*(Taps gavel gently on the wooden desk, adjusting suit cuffs)*\n\n"
            "Let's look at this without illusions. If opposing counsel were to drag you before a bench tomorrow, "
            "here is exactly where they would plunge the knife.\n\n"
            "### 1. The Evidentiary Vulnerability\n"
            "Your draft contains covenants phrased in ambiguous best-efforts language rather than strict conditional triggers. "
            "Under Indian Contract Act Section 29, agreements the meaning of which is not certain are void. In cross-examination, "
            "opposing counsel will challenge whether there was ever a true *consensus ad idem* regarding performance timelines.\n\n"
            "### 2. The Notice Trap\n"
            "Notice periods without mandatory delivery confirmation or deemed-receipt windows are procedural suicide. "
            "If notice is merely sent by email without delivery receipts, the presumption under Section 114 of the Evidence Act "
            "(now Sakshya Adhiniyam) can be rebutted with a single affidavit denying inbox receipt.\n\n"
            "### 3. Higuruma's Verdict & Amendment\n"
            "> *\"Notice shall be deemed served only upon verified delivery timestamp or signed acknowledgment. "
            "Failure to cure within thirty (30) calendar days of confirmed receipt shall constitute a material condition precedent to filing suit.\"*\n\n"
            "Close that door before trial begins. Judgeman grants no leniency to careless phrasing."
        )

    def _counsel_liability(self, draft: Optional[str], query: str) -> str:
        return (
            "*(Removes spectacles, cleaning them with a steady gaze)*\n\n"
            "Indemnity without a liability cap isn't an agreement. It's a confession of unlimited debt.\n\n"
            "### 1. The Asymmetric Risk\n"
            "Notice how the current indemnification clause attempts to make you liable for *'any and all indirect, consequential, or foreseeable losses'*. "
            "The English rule in *Hadley v. Baxendale (1854)* and its statutory codification under Section 73 of the Indian Contract Act, 1872 "
            "specifically restrict damages to those arising naturally from breach. Opposing counsel is attempting to contract around this protection.\n\n"
            "### 2. The Gross Negligence Carve-out\n"
            "They will argue that negligence alone should pierce the liability ceiling. That cannot be permitted. "
            "Liability caps must only yield to proven fraud, willful misconduct, or gross statutory violations.\n\n"
            "### 3. Higuruma's Remedial Language\n"
            "> *\"In no event shall either party's aggregate contractual liability exceed 100% of the fees paid in the twelve (12) months "
            "preceding the claim, expressly excluding punitive, consequential, and indirect damages.\"*\n\n"
            "Never sign away the ceiling. That is how clients become sacrificial offerings in corporate restructuring."
        )

    def _counsel_defense_strategy(self, draft: Optional[str], query: str) -> str:
        return (
            "*(Leans forward over the podium, expression cold and analytical)*\n\n"
            "A demand notice has been served? Good. Panic is the adversary of legal precision. Let us build the counter-case.\n\n"
            "### 1. Scrutinize the Cause of Action\n"
            "First, verify statutory limitation. If this is a Section 138 Negotiable Instruments Act notice, they have exactly 15 days "
            "from the date of receipt to demand payment, and the cheque must have been presented within validity. "
            "If their notice fails to state the exact cheque amount or incorporates unrelated damages, the notice is defective as a matter of law.\n\n"
            "### 2. The Defense of Waiver\n"
            "Did the other party continue accepting milestone deliverables after the purported breach? If so, doctrine of waiver "
            "and promissory estoppel under Section 115 bars them from retroactively claiming anticipatory breach.\n\n"
            "### 3. The Counter-Notice Strategy\n"
            "Do not remain silent. Silence is construed as acquiescence. Issue a surgical response within seven (7) days: "
            "categorically deny the allegations, place their own prior breaches on the evidentiary record, and reserve the right "
            "to pursue malicious litigation damages under Section 35A of the CPC.\n\n"
            "We defend by seizing the procedural high ground."
        )

    def _counsel_philosophy(self, query: str) -> str:
        return (
            "*(Looks down at his gavel, a faint, melancholic smile touching his lips)*\n\n"
            "People believe the law is designed to protect everyone equally. But when you spend years in the courtroom, "
            "you realize the system often functions like a machine grinding down the powerless through sheer procedural exhaustion.\n\n"
            "That is why Judgeman's domain exists. In my domain, there is no bribery, no fabricated witness testimony, "
            "and no privilege. Only the statute, the facts, and the penalty.\n\n"
            "When we draft a legal document, we are constructing a tiny domain of our own. Every defined term, every limitation clause, "
            "every dispute resolution mechanism is a rule of the trial. If you draft it with balance and unwavering precision, "
            "not even the strongest adversary can bend it to their will.\n\n"
            "Now... what clause shall we balance on the scale next?"
        )

    def _counsel_general(self, query: str, draft: Optional[str]) -> str:
        return (
            f"*(Raps gavel on the podium)*\n\n"
            f"I have reviewed your query: *\"{query}\"*\n\n"
            f"From a defense counsel's perspective, legal drafting is not about sounding impressive with archaic jargon. "
            f"It is about establishing clear, enforceable rights that survive judicial scrutiny.\n\n"
            f"### 1. Analysis\n"
            f"Ensure your operative covenants clearly answer three fundamental questions:\n"
            f"- **Who** is obligated to act?\n"
            f"- **When** is performance strictly required (timelines and cure periods)?\n"
            f"- **What** is the exact statutory or liquidated remedy if they fail?\n\n"
            f"### 2. Precedent & Authority\n"
            f"Always ground your terms in binding jurisprudence. An unverified clause is merely a wish until tested in court.\n\n"
            f"Tell me what specific provision you want to stress-test, and we will cross-examine it under Judgeman's gaze."
        )

    def _extract_tactical_takeaway(self, text: str) -> str:
        if "remedial language" in text.lower() or "verdict" in text.lower():
            match = re.search(r">\s*\*\"(.*?)\"\*", text, re.DOTALL)
            if match:
                return match.group(1).replace("\n", " ").strip()
        return "Ensure definitive performance triggers, strict notice cure periods, and bilateral liability caps."


# Global Singleton Instance
higuruma_engine = HigurumaPersonaEngine()
