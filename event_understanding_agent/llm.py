from typing import Any, Dict


class LLMReasoning:
    """Semantic reasoning layer.

    This mock keeps the interface stable while leaving a clear replacement point
    for an OpenAI call or another model-backed implementation.
    """

    def infer(
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
        }
