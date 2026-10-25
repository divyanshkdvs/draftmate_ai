"""
Integrated Voice Agent for DraftMate AI
References: OpenWhispr (https://github.com/OpenWhispr/openwhispr) & VoxCPM (https://voxcpm.net)

Parses voice transcripts, dispatches legal workflows, enforces safety confirmations
for destructive commands, and synthesizes speech responses.
"""

import re
from typing import Dict, Any, Optional
from .safety_guard import safety_guard

# Voice command intent mapping
VOICE_INTENTS = [
    {
        "patterns": [r"draft\s+(?:an?\s+)?nda", r"create\s+(?:an?\s+)?non[- ]disclosure"],
        "action": "activate_skill",
        "skill_id": "nda_drafting",
        "skill_tag": "@NDA",
        "feedback": "Activating NDA Drafting Skill. Please confirm parties and duration."
    },
    {
        "patterns": [r"review\s+(?:this\s+)?contract", r"check\s+(?:this\s+)?agreement", r"analyze\s+(?:this\s+)?contract"],
        "action": "activate_skill",
        "skill_id": "contract_review",
        "skill_tag": "@ContractReview",
        "feedback": "Starting Contract Review. Scanning for risk factors and unfair covenants."
    },
    {
        "patterns": [r"redline\s+(?:this\s+)?(?:clause|contract|draft)", r"generate\s+redline"],
        "action": "activate_skill",
        "skill_id": "redlining",
        "skill_tag": "@Redlining",
        "feedback": "Initiating Redline markup mode. Preparing strike-through revisions."
    },
    {
        "patterns": [r"legal\s+notice", r"draft\s+(?:a\s+)?notice", r"section\s+138"],
        "action": "activate_skill",
        "skill_id": "legal_notice_drafting",
        "skill_tag": "@LegalNotice",
        "feedback": "Activating Legal Notice Drafting module under statutory recovery provisions."
    },
    {
        "patterns": [r"verify\s+citations?", r"check\s+authorit(?:y|ies)", r"audit\s+citations?"],
        "action": "verify_citations",
        "feedback": "Verifying legal citations and statutory authorities against legal database."
    },
    {
        "patterns": [r"export\s+document", r"download\s+(?:as\s+)?(?:markdown|pdf|docx)"],
        "action": "export_document",
        "feedback": "Preparing document export in selected format."
    },
    # Consequential Actions requiring safety confirmation
    {
        "patterns": [r"overwrite\s+(?:the\s+)?(?:draft|document|file)", r"replace\s+(?:the\s+)?draft"],
        "action": "consequential_request",
        "intent_type": "overwrite_draft",
        "feedback": "Hold on: Overwriting your current draft will replace active changes. Please confirm."
    },
    {
        "patterns": [r"delete\s+(?:the\s+)?(?:document|file|matter)", r"remove\s+(?:the\s+)?file"],
        "action": "consequential_request",
        "intent_type": "delete_document",
        "feedback": "Warning: Deleting this document is permanent. Explicit confirmation required."
    },
    {
        "patterns": [r"clear\s+(?:the\s+)?(?:workspace|conversation|chat|everything)"],
        "action": "consequential_request",
        "intent_type": "clear_workspace",
        "feedback": "Warning: Clearing the workspace will reset your active session. Explicit confirmation required."
    }
]


class VoiceAgent:
    """Interprets voice dictation and executes voice commands."""

    def parse_transcript(self, transcript: str) -> Dict[str, Any]:
        """Parse spoken instruction into actionable legal workflows with safety checks."""
        clean_text = transcript.strip().lower()

        # Check matched intent
        for rule in VOICE_INTENTS:
            for pattern in rule["patterns"]:
                if re.search(pattern, clean_text, re.IGNORECASE):
                    # Check if action is consequential
                    if rule["action"] == "consequential_request":
                        safety_check = safety_guard.inspect_intent(
                            intent=rule["intent_type"],
                            details={"spoken_phrase": transcript}
                        )
                        return {
                            "status": "confirmation_required",
                            "action": rule["action"],
                            "intent_type": rule["intent_type"],
                            "feedback": rule["feedback"],
                            "safety": safety_check,
                            "recognized_text": transcript
                        }

                    return {
                        "status": "ready",
                        "action": rule["action"],
                        "skill_id": rule.get("skill_id"),
                        "skill_tag": rule.get("skill_tag"),
                        "feedback": rule["feedback"],
                        "recognized_text": transcript
                    }

        # If no specialized command pattern, treat as natural language drafting dictation
        return {
            "status": "dictation",
            "action": "insert_text",
            "feedback": "Transcribed voice input added to prompt workspace.",
            "recognized_text": transcript
        }


# Global Singleton Instance
voice_agent = VoiceAgent()
