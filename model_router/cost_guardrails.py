class CostGuardrails:
    """Model usage policy for enterprise-scale cost control."""

    LLM_PER_USER_RUNTIME_ALLOWED = False

    BATCH_FIRST_USE_CASES = {
        "event_understanding",
        "event_taxonomy_classification",
        "behavioral_state_refresh",
    }

    EVENT_LLM_ALLOWED_FOR = {
        "new_taxonomy_mapping",
        "taxonomy_refresh",
        "low_confidence_fallback",
    }

    def allow_event_llm(self, reason: str) -> bool:
        return reason in self.EVENT_LLM_ALLOWED_FOR
