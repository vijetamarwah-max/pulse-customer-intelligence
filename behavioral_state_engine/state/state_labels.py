from typing import Dict


class StateLabeler:
    def label(self, state: Dict[str, float]) -> str:
        if state.get("complaint_retention_risk", 0.0) > 0.75:
            if state["communication_fatigue"] > 0.6 or state["trust_level"] < 0.45:
                return "complaint_led_retention_risk"
            return "trust_recovery_needed"

        if state.get("inactivity_retention_risk", 0.0) > 0.75:
            return "inactivity_led_retention_risk"

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
