"""
Safety Confirmation Engine for Consequential Voice Actions in DraftMate AI
Guards against accidental deletion, file overwrite, or unauthorized execution
via spoken commands.
"""

import uuid
import time
from typing import Dict, Any, Optional

# Actions flagged as consequential
CONSEQUENTIAL_ACTIONS = {
    "overwrite_draft": {
        "title": "Overwrite Active Legal Draft",
        "severity": "HIGH",
        "description": "This action will completely replace your current draft with a newly synthesized version. Previous unsaved revisions may be lost.",
        "requires_typed_confirmation": False
    },
    "delete_document": {
        "title": "Delete Matter Document",
        "severity": "CRITICAL",
        "description": "This will permanently remove the legal document from your DraftMate workspace storage.",
        "requires_typed_confirmation": True
    },
    "clear_workspace": {
        "title": "Reset Workspace & Conversation",
        "severity": "CRITICAL",
        "description": "All active drafting context, redlines, and chat history will be cleared.",
        "requires_typed_confirmation": False
    },
    "execute_disclaimer_waiver": {
        "title": "Final Legal Execution Sign-off",
        "severity": "MEDIUM",
        "description": "Acknowledges that AI drafting output has been reviewed by a qualified advocate prior to production.",
        "requires_typed_confirmation": False
    }
}


class ConsequentialSafetyGuard:
    """Manages confirmation tokens and safety checks for voice and automation actions."""

    def __init__(self):
        self._pending_tokens: Dict[str, Dict[str, Any]] = {}

    def inspect_intent(self, intent: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Check if an action is consequential and requires explicit user authorization."""
        intent_key = intent.lower().strip()
        if intent_key in CONSEQUENTIAL_ACTIONS:
            meta = CONSEQUENTIAL_ACTIONS[intent_key]
            token = str(uuid.uuid4())
            expires_at = time.time() + 180  # 3 minutes expiry

            payload = {
                "token": token,
                "intent": intent_key,
                "title": meta["title"],
                "severity": meta["severity"],
                "description": meta["description"],
                "details": details or {},
                "created_at": time.time(),
                "expires_at": expires_at,
                "is_consequential": True
            }
            self._pending_tokens[token] = payload
            return payload

        return {
            "is_consequential": False,
            "intent": intent_key,
            "can_execute_immediately": True
        }

    def verify_and_consume(self, token: str) -> bool:
        """Validate and consume a pending confirmation token."""
        if not token or token not in self._pending_tokens:
            return False

        item = self._pending_tokens[token]
        if time.time() > item["expires_at"]:
            del self._pending_tokens[token]
            return False

        # Token consumed
        del self._pending_tokens[token]
        return True


# Global Singleton Instance
safety_guard = ConsequentialSafetyGuard()
