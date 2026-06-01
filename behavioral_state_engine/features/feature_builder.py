from typing import Dict


class FeatureBuilder:
    def build(self, fused_state: Dict[str, float]) -> Dict[str, float]:
        return {
            "purchase_x_trust": (
                fused_state["purchase_readiness"] * fused_state["trust_level"]
            ),
            "fatigue_x_engagement": (
                fused_state["communication_fatigue"]
                * fused_state["engagement_probability"]
            ),
            "retention_x_affinity": (
                fused_state["retention_risk"] * fused_state["brand_affinity"]
            ),
            "urgency_x_retention": (
                fused_state.get("urgency_signal", 0.0) * fused_state["retention_risk"]
            ),
            "recency_x_purchase": (
                fused_state.get("recency_strength", 0.0)
                * fused_state["purchase_readiness"]
            ),
        }
