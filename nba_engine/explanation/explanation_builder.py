class ExplanationBuilder:
    def build(self, selected_action, state, goal):
        reasons = []

        if state.get("communication_fatigue", 0.0) > 0.7:
            reasons.append("high_communication_fatigue")

        if state.get("purchase_readiness", 0.0) > 0.7:
            reasons.append("high_purchase_readiness")

        if state.get("retention_risk", 0.0) > 0.7:
            reasons.append("elevated_retention_risk")

        reasons.append(f"business_goal_{goal}")
        reasons.append(f"selected_action_{selected_action}")

        return reasons
