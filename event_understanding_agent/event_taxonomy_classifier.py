import json
import os
from pathlib import Path
from typing import Dict, Iterable, List

from model_router.routing_policy import ModelRoutingPolicy

from .config import EVENT_TAXONOMY_MODEL_USE_CASE
from .prompts import EVENT_TAXONOMY_CLASSIFICATION_PROMPT


class EventTaxonomyClassifier:
    """LLM-backed taxonomy builder for raw enterprise event names."""

    def __init__(self, model=None) -> None:
        self._load_local_env()
        self.model_router = ModelRoutingPolicy()
        self.model_use_case = EVENT_TAXONOMY_MODEL_USE_CASE
        self.model = model or self.model_router.model_for(self.model_use_case)

    def classify(self, event_names: Iterable[str]) -> List[Dict]:
        api_key = self._usable_api_key()
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for LLM taxonomy classification."
            )

        from openai import OpenAI

        payload = {"raw_event_names": list(event_names)}
        response = OpenAI(api_key=api_key).responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": EVENT_TAXONOMY_CLASSIFICATION_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, indent=2),
                },
            ],
            **self._reasoning_kwargs(),
        )

        parsed = json.loads(response.output_text)
        return parsed.get("mappings", [])

    def _reasoning_kwargs(self) -> Dict:
        effort = self.model_router.reasoning_effort_for(self.model_use_case)
        if effort == "none":
            return {}
        return {"reasoning": {"effort": effort}}

    def _usable_api_key(self):
        value = os.getenv("OPENAI_API_KEY")
        if not value or "your_" in value:
            return None
        return value

    def _load_local_env(self) -> None:
        env_path = Path(__file__).resolve().parents[1] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            if value and "your_" not in value:
                os.environ.setdefault(key.strip(), value)
