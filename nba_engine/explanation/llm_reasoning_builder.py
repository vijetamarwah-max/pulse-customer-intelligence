import json
import os
from pathlib import Path

from model_router.routing_policy import ModelRoutingPolicy

from .prompts import NBA_EXPLANATION_SYSTEM_PROMPT


class LLMReasoningBuilder:
    """OpenAI-backed NBA decision explanation builder."""

    def __init__(self, model=None):
        self._load_local_env()
        self.model_router = ModelRoutingPolicy()
        self.model = model or self.model_router.model_for("nba_explanation")

    def build(
        self,
        selected_action,
        behavioral_state,
        ranked_actions,
        counterfactuals,
        goal,
    ):
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Set it in your environment or local .env "
                "before running NBA LLM reasoning."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The openai package is not installed. Run: python -m pip install -r requirements.txt"
            ) from exc

        client = OpenAI()
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": NBA_EXPLANATION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "selected_action": selected_action,
                            "business_goal": goal,
                            "behavioral_state": behavioral_state,
                            "ranked_actions": ranked_actions,
                            "counterfactuals": counterfactuals,
                        },
                        indent=2,
                    ),
                },
            ],
        )

        return response.output_text.strip()

    def _load_local_env(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
