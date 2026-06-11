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
        cart_intensity = event_signals.get("cart_intensity", 0.0)
        checkout_intensity = event_signals.get("checkout_intensity", 0.0)
        wishlist_intensity = event_signals.get("wishlist_intensity", 0.0)
        browse_intensity = event_signals.get("browse_intensity", 0.0)
        coupon_intensity = event_signals.get("coupon_intensity", 0.0)
        recent_conversion_signal = event_signals.get("recent_conversion_signal", 0.0)
        service_blocker_intensity = event_signals.get("service_blocker_intensity", 0.0)

        frustration = voc_signals.get("frustration_signal", 0.0)
        urgency = voc_signals.get("urgency_signal", 0.0)
        trust = voc_signals.get("trust_signal", 0.0)
        voc_retention_risk = voc_signals.get("retention_risk", 0.0)
        engagement = voc_signals.get("engagement_signal", 0.0)
        escalation = voc_signals.get("escalation_risk", 0.0)

        total_orders = float(crm_context.get("total_orders", 0) or 0)
        average_order_value = float(crm_context.get("average_order_value", 0) or 0)
        last_purchase_days_ago = float(crm_context.get("last_purchase_days_ago", 30) or 30)
        messages_7d = float(crm_context.get("messages_7d", 0) or 0)
        inactive_days = float(crm_context.get("inactive_days", 0) or 0)
        support_status = crm_context.get("support_status", "none")
        recent_complaint = bool(crm_context.get("recent_complaint", False))
        nps = crm_context.get("nps")

        trust = self._trust_with_enterprise_context(
            trust=trust,
            nps=nps,
            support_status=support_status,
            recent_complaint=recent_complaint,
        )
        fatigue = max(
            frustration,
            escalation * 0.6,
            min(messages_7d / 12, 1.0),
            0.65 if recent_complaint else 0.0,
        )
        complaint_retention_risk = self._complaint_retention_risk(
            support_status=support_status,
            recent_complaint=recent_complaint,
            nps=nps,
            voc_retention_risk=voc_retention_risk,
            event_churn_risk=event_churn_risk,
        )
        inactivity_retention_risk = self._inactivity_retention_risk(
            inactive_days=inactive_days,
            last_purchase_days_ago=last_purchase_days_ago,
        )
        retention_risk = max(
            event_churn_risk,
            voc_retention_risk,
            complaint_retention_risk,
            inactivity_retention_risk,
        )

        brand_affinity = self._brand_affinity(
            total_orders=total_orders,
            average_order_value=average_order_value,
            loyalty_member=bool(crm_context.get("loyalty_member", False)),
        )

        return {
            "purchase_readiness": purchase_intent,
            "engagement_probability": max(engagement, exploration_intent * 0.6),
            "communication_fatigue": fatigue,
            "retention_risk": retention_risk,
            "trust_level": trust,
            "discount_sensitivity": self._discount_sensitivity(crm_context),
            "brand_affinity": brand_affinity,
            "recency_strength": self._recency_strength(last_purchase_days_ago),
            "urgency_signal": urgency,
            "complaint_retention_risk": complaint_retention_risk,
            "inactivity_retention_risk": inactivity_retention_risk,
            "cart_intensity": cart_intensity,
            "checkout_intensity": checkout_intensity,
            "wishlist_intensity": wishlist_intensity,
            "browse_intensity": browse_intensity,
            "coupon_intensity": coupon_intensity,
            "recent_conversion_signal": recent_conversion_signal,
            "service_blocker_intensity": service_blocker_intensity,
        }

    def _discount_sensitivity(self, crm_context: Dict) -> float:
        ltv_segment = crm_context.get("ltv_segment")
        customer_tier = crm_context.get("customer_tier")

        if ltv_segment == "price_sensitive":
            return 0.8
        if customer_tier in {"gold", "platinum"} or ltv_segment == "high_value":
            return 0.35
        return 0.4

    def _trust_with_enterprise_context(
        self,
        trust: float,
        nps,
        support_status: str,
        recent_complaint: bool,
    ) -> float:
        adjusted = trust
        if nps is not None:
            adjusted = min(adjusted, max(0.0, min(1.0, (float(nps) + 100) / 200)))
        if support_status in {"open_ticket", "escalated_ticket", "recent_return"}:
            adjusted = min(adjusted, 0.35)
        if recent_complaint:
            adjusted = min(adjusted, 0.4)
        if support_status == "resolved":
            adjusted = max(adjusted, 0.45)

        return adjusted

    def _complaint_retention_risk(
        self,
        support_status: str,
        recent_complaint: bool,
        nps,
        voc_retention_risk: float,
        event_churn_risk: float,
    ) -> float:
        risk = 0.0
        if support_status == "escalated_ticket":
            risk = max(risk, 0.9)
        elif support_status == "open_ticket":
            risk = max(risk, 0.78)
        elif support_status in {"recent_return", "closed_negative"}:
            risk = max(risk, 0.7)
        if recent_complaint:
            risk = max(risk, 0.72)
        if nps is not None and float(nps) < 0:
            risk = max(risk, min(0.9, 0.5 + abs(float(nps)) / 100))
        if risk > 0:
            risk = max(risk, voc_retention_risk, event_churn_risk * 0.6)

        return risk

    def _inactivity_retention_risk(
        self,
        inactive_days: float,
        last_purchase_days_ago: float,
    ) -> float:
        if inactive_days > 30:
            return 0.9
        if inactive_days > 14:
            return 0.8
        if last_purchase_days_ago > 120:
            return 0.75
        if last_purchase_days_ago > 75:
            return 0.62
        return 0.0

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
