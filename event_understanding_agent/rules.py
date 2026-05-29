from typing import Any, Dict


class RuleEngine:
    """Deterministic guardrail layer for overrides, suppressions, and consistency."""

    def apply(
        self,
        user_state: Dict[str, Any],
        llm_output: Dict[str, Any],
        embedding_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        output = {
            **llm_output,
            "behavioral_tags": list(llm_output.get("behavioral_tags", [])),
            "rule_adjustment": False,
        }

        if user_state.get("inactive_days", 0) > 14:
            output["churn_risk"] = max(output["churn_risk"], 0.9)
            output["rule_adjustment"] = True
            output["behavioral_tags"].append("hard_churn_override")

        if user_state.get("recent_complaint", False):
            output["purchase_intent"] *= 0.5
            output["rule_adjustment"] = True
            output["behavioral_tags"].append("support_sensitive")

        if embedding_scores["purchase_intent"] > 0.8 and output["confidence"] < 0.5:
            output["confidence"] = 0.6
            output["rule_adjustment"] = True
            output["behavioral_tags"].append("uncertain_signal")

        if user_state.get("events_7d", 0) == 0:
            output["churn_risk"] = max(output["churn_risk"], 0.7)
            output["rule_adjustment"] = True
            output["behavioral_tags"].append("recent_inactivity")

        if embedding_scores["purchase_intent"] < 0.3 and user_state.get("cart_actions_30d", 0) == 0:
            output["purchase_intent"] = 0.0
            output["rule_adjustment"] = True
            output["behavioral_tags"].append("purchase_intent_suppressed")

        output["confidence"] = max(0.0, min(1.0, output["confidence"]))
        output["purchase_intent"] = max(0.0, min(1.0, output["purchase_intent"]))
        output["exploration_intent"] = max(0.0, min(1.0, output["exploration_intent"]))
        output["churn_risk"] = max(0.0, min(1.0, output["churn_risk"]))
        output["behavioral_tags"] = sorted(set(output["behavioral_tags"]))

        return output
