import json
import os
from pathlib import Path
from typing import Any, Dict

from model_router.routing_policy import ModelRoutingPolicy

from .config import EVENT_RUNTIME_FALLBACK_MODEL_USE_CASE
from .prompts import EVENT_RUNTIME_REASONING_PROMPT


class LLMReasoning:
    """Semantic reasoning layer.

    This mock keeps the interface stable while leaving a clear replacement point
    for an OpenAI call or another model-backed implementation.
    """

    def __init__(self) -> None:
        self._load_local_env()
        self.model_router = ModelRoutingPolicy()
        self.model_use_case = EVENT_RUNTIME_FALLBACK_MODEL_USE_CASE
        self.model = self.model_router.model_for(self.model_use_case)

    def infer(
        self,
        event_stream: Dict[str, Any],
        embedding_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        if self._should_call_openai(event_stream, embedding_scores):
            return self._infer_with_openai(event_stream, embedding_scores)

        return self._infer_locally(event_stream, embedding_scores)

    def _infer_locally(
        self,
        event_stream: Dict[str, Any],
        embedding_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        purchase = embedding_scores["purchase_intent"] * 0.9
        explore = embedding_scores["exploration_intent"] * 0.8
        churn = embedding_scores["churn_risk"] * 0.7

        tags = []

        if purchase > 0.7:
            tags.append("high_consideration_user")

        if explore > 0.6 and event_stream.get("cart_actions", 0) == 0:
            tags.append("exploration_mode")

        if churn > 0.6:
            tags.append("at_risk")

        if event_stream.get("cart_actions", 0) > 0 and event_stream.get("checkout_actions", 0) == 0:
            tags.append("mid_funnel")

        confidence = min(0.95, max(0.0, (purchase + explore) / 2))

        return {
            "purchase_intent": purchase,
            "exploration_intent": explore,
            "churn_risk": churn,
            "behavioral_tags": tags,
            "confidence": confidence,
            "explanation": "Derived from mixed behavioral signals over a 30-day window.",
            "model_route": {
                "use_case": self.model_use_case,
                "model": self.model_router.model_for(self.model_use_case),
                "reasoning_effort": self.model_router.reasoning_effort_for(
                    self.model_use_case
                ),
            },
        }

    def _infer_with_openai(
        self,
        event_stream: Dict[str, Any],
        embedding_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        from openai import OpenAI

        payload = {
            "events": event_stream,
            "embedding_scores": embedding_scores,
            "model_route": {
                "use_case": self.model_use_case,
                "model": self.model,
                "reasoning_effort": self.model_router.reasoning_effort_for(
                    self.model_use_case
                ),
            },
        }

        response = OpenAI(api_key=self._usable_api_key()).responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": EVENT_RUNTIME_REASONING_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, indent=2),
                },
            ],
            **self._reasoning_kwargs(),
        )

        result = json.loads(response.output_text)
        result["model_route"] = payload["model_route"]
        return self._coerce_result(result)

    def _coerce_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "purchase_intent": self._bounded(result.get("purchase_intent", 0.0)),
            "exploration_intent": self._bounded(result.get("exploration_intent", 0.0)),
            "churn_risk": self._bounded(result.get("churn_risk", 0.0)),
            "behavioral_tags": list(result.get("behavioral_tags", [])),
            "confidence": self._bounded(result.get("confidence", 0.0)),
            "explanation": str(result.get("explanation", "")),
            "model_route": result["model_route"],
        }

    def _should_call_openai(
        self,
        event_stream: Dict[str, Any],
        embedding_scores: Dict[str, float],
    ) -> bool:
        if event_stream.get("force_llm_reasoning", False):
            return bool(self._usable_api_key())

        if not self._usable_api_key():
            return False

        if event_stream.get("unknown_events", 0) > 0:
            return True

        top_score = max(embedding_scores.values()) if embedding_scores else 0.0
        sorted_scores = sorted(embedding_scores.values(), reverse=True)
        margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else 1.0

        return top_score < 0.55 or margin < 0.08

    def _reasoning_kwargs(self) -> Dict[str, Any]:
        effort = self.model_router.reasoning_effort_for(self.model_use_case)
        if effort == "none":
            return {}
        return {"reasoning": {"effort": effort}}

    def _usable_api_key(self):
        value = os.getenv("OPENAI_API_KEY")
        if not value or "your_" in value:
            return None
        return value

    def _bounded(self, value: Any) -> float:
        return max(0.0, min(1.0, float(value)))

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
