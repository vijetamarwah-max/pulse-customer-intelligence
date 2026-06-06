import os

from .model_config import MODEL_CONFIG


class ModelRoutingPolicy:
    """Central model router for Pulse AI.

    Model choices live here so agents can swap model families without changing
    their business logic.
    """

    ENV_OVERRIDES = {
        "event_taxonomy_classification": "EVENT_TAXONOMY_MODEL",
        "event_runtime_fallback": "EVENT_RUNTIME_FALLBACK_MODEL",
        "voc_reasoning": "VOC_REASONING_MODEL",
        "nba_explanation": "NBA_LLM_MODEL",
        "audio_transcription": "OPENAI_TRANSCRIPTION_MODEL",
    }

    def model_for(self, use_case: str) -> str:
        self._ensure_use_case(use_case)
        override_key = self.ENV_OVERRIDES.get(use_case)
        if override_key and os.getenv(override_key):
            return os.getenv(override_key)

        return MODEL_CONFIG[use_case]["model"]

    def reasoning_effort_for(self, use_case: str) -> str:
        self._ensure_use_case(use_case)
        return MODEL_CONFIG[use_case]["reasoning_effort"]

    def describe(self):
        return {
            use_case: {
                "model": self.model_for(use_case),
                "reasoning_effort": self.reasoning_effort_for(use_case),
                "usage": config["usage"],
            }
            for use_case, config in MODEL_CONFIG.items()
        }

    def _ensure_use_case(self, use_case: str) -> None:
        if use_case not in MODEL_CONFIG:
            raise ValueError(f"Unknown model routing use case: {use_case}")
