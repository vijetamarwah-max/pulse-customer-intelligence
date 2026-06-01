from typing import Dict


class SignalFusionEngine:
    def fuse(
        self,
        event_signals: Dict[str, float],
        voc_signals: Dict[str, float],
        crm_context: Dict,
    ) -> Dict[str, float]:
        purchase_intent = event_signals.get("purchase_intent", 0.0)
        exploration_intent = event_signals.get("exploration_intent", 0.0)
        event_churn_risk = event_signals.get("churn_risk", 0.0)

        frustration = voc_signals.get("frustration_signal", 0.0)
        urgency = voc_signals.get("urgency_signal", 0.0)
        trust = voc_signals.get("trust_signal", 0.0)
        voc_retention_risk = voc_signals.get("retention_risk", 0.0)
        engagement = voc_signals.get("engagement_signal", 0.0)
        escalation = voc_signals.get("escalation_risk", 0.0)

        total_orders = float(crm_context.get("total_orders", 0) or 0)
        average_order_value = float(crm_context.get("average_order_value", 0) or 0)
        last_purchase_days_ago = float(crm_context.get("last_purchase_days_ago", 30) or 30)

        brand_affinity = self._brand_affinity(
            total_orders=total_orders,
            average_order_value=average_order_value,
            loyalty_member=bool(crm_context.get("loyalty_member", False)),
        )

        return {
            "purchase_readiness": purchase_intent,
            "engagement_probability": max(engagement, exploration_intent * 0.6),
            "communication_fatigue": max(frustration, escalation * 0.6),
            "retention_risk": max(event_churn_risk, voc_retention_risk),
            "trust_level": trust,
            "discount_sensitivity": self._discount_sensitivity(crm_context),
            "brand_affinity": brand_affinity,
            "recency_strength": self._recency_strength(last_purchase_days_ago),
            "urgency_signal": urgency,
        }

    def _discount_sensitivity(self, crm_context: Dict) -> float:
        ltv_segment = crm_context.get("ltv_segment")
        customer_tier = crm_context.get("customer_tier")

        if ltv_segment == "price_sensitive":
            return 0.8
        if customer_tier in {"gold", "platinum"} or ltv_segment == "high_value":
            return 0.35
        return 0.4

    def _brand_affinity(
        self,
        total_orders: float,
        average_order_value: float,
        loyalty_member: bool,
    ) -> float:
        order_score = min(total_orders / 20, 1.0)
        value_score = min(average_order_value / 300, 1.0)
        loyalty_boost = 0.15 if loyalty_member else 0.0
        return min((order_score * 0.65) + (value_score * 0.25) + loyalty_boost, 1.0)

    def _recency_strength(self, last_purchase_days_ago: float) -> float:
        return max(0.0, min(1.0, 1 - (last_purchase_days_ago / 90)))
