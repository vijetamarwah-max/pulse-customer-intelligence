from .custom_rule_engine import CustomRuleEngine


class ConstraintsEngine:
    def __init__(self):
        self.custom_rules = CustomRuleEngine()
        self.last_evaluated_constraints = {}
        self.last_rule_reasons = []

    def apply(self, actions, constraints, behavioral_state=None):
        behavioral_state = behavioral_state or {}
        constraints = constraints or {}
        rule_result = self.custom_rules.apply(constraints, behavioral_state)
        constraints = rule_result["constraints"]
        self.last_evaluated_constraints = constraints
        self.last_rule_reasons = rule_result["reasons"]

        if rule_result["forced_action"]:
            return [rule_result["forced_action"]]

        filtered = []
        suppressed_actions = set(constraints.get("suppressed_actions") or [])

        for action in actions:
            if action in suppressed_actions:
                continue

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

            if (
                (action.startswith("send_") or action == "service_recovery")
                and constraints.get("send_allowed", True) is False
            ):
                continue

            filtered.append(action)

        return filtered

    def evaluated_constraints(self):
        return {
            **self.last_evaluated_constraints,
            "custom_rule_reasons": self.last_rule_reasons,
        }
