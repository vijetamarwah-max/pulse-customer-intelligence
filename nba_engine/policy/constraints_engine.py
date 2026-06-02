class ConstraintsEngine:
    def apply(self, actions, constraints, behavioral_state=None):
        behavioral_state = behavioral_state or {}
        filtered = []

        for action in actions:
            if action == "send_discount_offer" and not constraints.get(
                "discounts_allowed",
                False,
            ):
                continue

            if (
                action != "suppress"
                and constraints.get("suppress_if_high_fatigue", True)
                and behavioral_state.get("communication_fatigue", 0.0) > 0.85
            ):
                continue

            if action.startswith("send_") and constraints.get("send_allowed", True) is False:
                continue

            filtered.append(action)

        return filtered
