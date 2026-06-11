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
        if os.getenv("PULSE_DISABLE_RUNTIME_LLM", "").lower() == "true":
            return self._fallback_reasoning(
                selected_action,
                behavioral_state,
                ranked_actions,
                goal,
            )

        if not os.getenv("OPENAI_API_KEY"):
            return self._fallback_reasoning(
                selected_action,
                behavioral_state,
                ranked_actions,
                goal,
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            return self._fallback_reasoning(
                selected_action,
                behavioral_state,
                ranked_actions,
                goal,
            )

        client = OpenAI()
        try:
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
        except Exception:
            return self._fallback_reasoning(
                selected_action,
                behavioral_state,
                ranked_actions,
                goal,
            )

        return response.output_text.strip()

    def _fallback_reasoning(
        self,
        selected_action,
        behavioral_state,
        ranked_actions,
        goal,
    ):
        fatigue = behavioral_state.get("communication_fatigue", 0)
        trust = behavioral_state.get("trust_level", 0)
        best_value = ranked_actions.get(selected_action, 0)

        return (
            f"Recommended {selected_action} for goal '{goal}' because it has the "
            f"highest estimated value ({best_value}) among allowed actions. "
            f"The state shows communication fatigue={fatigue} and trust_level={trust}, "
            "so the decision balances incremental value with intervention risk."
        )

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
