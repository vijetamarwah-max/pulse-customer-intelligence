from typing import Dict


class BehavioralScoringModels:
    """MVP scoring logic.

    Replace this deterministic scoring class with LightGBM or XGBoost once
    labeled outcome data is available.
    """

    def score(
        self,
        normalized_state: Dict[str, float],
        engineered_features: Dict[str, float],
    ) -> Dict[str, float]:
        state = dict(normalized_state)

        intervention_receptiveness = (
            engineered_features["purchase_x_trust"]
            + (state["brand_affinity"] * 0.2)
            + (state.get("urgency_signal", 0.0) * 0.15)
            - (state["communication_fatigue"] * 0.4)
            - (state["retention_risk"] * 0.15)
        )

        state["intervention_receptiveness"] = self._bounded(intervention_receptiveness)

        return {
            "purchase_readiness": state["purchase_readiness"],
            "engagement_probability": state["engagement_probability"],
            "communication_fatigue": state["communication_fatigue"],
            "retention_risk": state["retention_risk"],
            "trust_level": state["trust_level"],
            "discount_sensitivity": state["discount_sensitivity"],
            "brand_affinity": state["brand_affinity"],
            "intervention_receptiveness": state["intervention_receptiveness"],
        }

    def _bounded(self, value: float) -> float:
        return round(min(max(float(value), 0.0), 1.0), 3)
