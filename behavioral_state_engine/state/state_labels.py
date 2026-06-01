from typing import Dict


class StateLabeler:
    def label(self, state: Dict[str, float]) -> str:
        if (
            state["purchase_readiness"] > 0.7
            and state["communication_fatigue"] > 0.6
        ):
            return "high_intent_high_fatigue"

        if state["retention_risk"] > 0.8:
            return "high_retention_risk"

        if state["purchase_readiness"] > 0.7 and state["trust_level"] > 0.6:
            return "high_intent_receptive"

        if state["communication_fatigue"] > 0.7 and state["trust_level"] < 0.4:
            return "low_trust_high_fatigue"

        if state["engagement_probability"] < 0.3 and state["purchase_readiness"] < 0.4:
            return "passive_or_dormant"

        return "balanced_state"
