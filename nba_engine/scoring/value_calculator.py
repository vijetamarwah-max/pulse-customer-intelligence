class ValueCalculator:
    def calculate(
        self,
        predicted_outcomes,
        goal_weights,
        allowed_actions,
        behavioral_state=None,
    ):
        behavioral_state = behavioral_state or {}
        values = {}

        for action in allowed_actions:
            metrics = predicted_outcomes.get(action)
            if not metrics:
                continue

            score = (
                metrics["revenue"] * goal_weights["revenue"]
                + metrics["engagement"] * goal_weights["engagement"]
                + metrics["retention"] * goal_weights["retention"]
            )

            values[action] = round(
                self._apply_state_adjustments(score, action, behavioral_state),
                3,
            )

        return values

    def _apply_state_adjustments(self, score, action, state):
        fatigue = state.get("communication_fatigue", 0.0)
        trust = state.get("trust_level", 0.0)
        retention = state.get("retention_risk", 0.0)
        complaint_retention = state.get("complaint_retention_risk", 0.0)
        inactivity_retention = state.get("inactivity_retention_risk", 0.0)
        purchase = state.get("purchase_readiness", 0.0)
        discount = state.get("discount_sensitivity", 0.0)
        receptiveness = state.get("intervention_receptiveness", 0.0)
        cart = state.get("cart_intensity", 0.0)
        checkout = state.get("checkout_intensity", 0.0)
        wishlist = state.get("wishlist_intensity", 0.0)
        browse = state.get("browse_intensity", 0.0)
        coupon = state.get("coupon_intensity", 0.0)
        recent_conversion = state.get("recent_conversion_signal", 0.0)
        service_blocker = state.get("service_blocker_intensity", 0.0)

        if action in {"send_product_recommendation", "send_discount_offer", "send_cart_reminder"}:
            if fatigue > 0.7:
                score -= 45
            if trust < 0.45:
                score -= 50
            if receptiveness < 0.25:
                score -= 30

        if action == "send_product_recommendation":
            if browse > 0.55 and cart < 0.25 and checkout < 0.2 and wishlist < 0.25:
                score -= 45
            if recent_conversion > 0.5 and fatigue > 0.45:
                score -= 35

        if action == "send_discount_offer":
            if coupon > 0.45 and purchase > 0.45 and trust >= 0.45:
                score += 90
            elif discount > 0.65 and purchase > 0.5 and trust >= 0.45:
                score += 35
            if discount < 0.5 and coupon < 0.45:
                score -= 25
            if recent_conversion > 0.5:
                score -= 30

        if action == "send_cart_reminder":
            if cart > 0.35 and checkout > 0.2 and fatigue < 0.65 and trust > 0.5:
                score += 70
            elif cart > 0.35 and fatigue < 0.55 and trust > 0.5:
                score += 35
            else:
                score -= 85
            if browse > 0.55 and cart < 0.25:
                score -= 45
            if wishlist > 0.4 and checkout < 0.2:
                score -= 35
            if inactivity_retention > 0.65:
                score -= 55
            if complaint_retention > 0.65:
                score -= 35
            if recent_conversion > 0.5:
                score -= 60
            if service_blocker > 0.5:
                score -= 40

        if action == "send_content":
            if browse > 0.45 and cart < 0.35 and fatigue < 0.75:
                score += 75
            if wishlist > 0.35 and checkout < 0.35 and fatigue < 0.75:
                score += 45
            if recent_conversion > 0.5 and fatigue < 0.8:
                score += 35
            if purchase < 0.55 and fatigue < 0.6:
                score += 25
            if trust < 0.45 and fatigue < 0.75:
                score += 15

        if action == "send_retention_message":
            if inactivity_retention > 0.65:
                score += 95
            elif retention > 0.65:
                score += 45
            if trust < 0.45 and complaint_retention > 0.65:
                score += 20

        if action == "service_recovery":
            if complaint_retention > 0.65:
                score += 90
            elif inactivity_retention > 0.65:
                score -= 45
            else:
                score -= 40
            if trust < 0.45:
                score += 70
            if fatigue > 0.65:
                score += 50 if complaint_retention > 0.45 or service_blocker > 0.5 else 5
            if retention > 0.65:
                score += 55
            if purchase > 0.55:
                score += 15
            if service_blocker > 0.5:
                score += 85
            if recent_conversion > 0.5 and complaint_retention < 0.45 and service_blocker < 0.5:
                score -= 85

        if action == "suppress":
            if fatigue > 0.7:
                score += 65
            if trust < 0.4:
                score += 45
            if receptiveness < 0.2:
                score += 35
            if recent_conversion > 0.5 and fatigue > 0.55:
                score += 45
            if browse > 0.5 and cart < 0.25 and state.get("engagement_probability", 0.0) < 0.45:
                score += 25
            if purchase > 0.75 and fatigue < 0.45 and trust > 0.55:
                score -= 40

        return score
