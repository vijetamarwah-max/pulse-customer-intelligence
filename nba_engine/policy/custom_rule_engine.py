class CustomRuleEngine:
    """Evaluates tenant/user configurable NBA guardrail rules.

    Rule format:
    {
      "id": "support_dnd",
      "when": {"field": "support_ticket_open_days", "op": ">=", "value": 14},
      "actions": [
        {"type": "force_action", "value": "suppress"},
        {"type": "add_reason", "value": "support_ticket_policy"}
      ]
    }
    """

    def apply(self, constraints, behavioral_state=None):
        constraints = dict(constraints or {})
        behavioral_state = behavioral_state or {}
        context = {
            **constraints,
            **{f"state.{key}": value for key, value in behavioral_state.items()},
        }
        result = {
            "constraints": constraints,
            "forced_action": None,
            "reasons": [],
        }

        for rule in constraints.get("custom_rules", []):
            if self._matches(rule.get("when", {}), context):
                self._apply_actions(rule, result)

        return result

    def _matches(self, condition, context):
        if not condition:
            return True

        if "all" in condition:
            return all(self._matches(item, context) for item in condition["all"])

        if "any" in condition:
            return any(self._matches(item, context) for item in condition["any"])

        field = condition.get("field")
        op = condition.get("op", "==")
        expected = condition.get("value")
        actual = context.get(field)
        return self._compare(actual, op, expected)

    def _compare(self, actual, op, expected):
        if op == "==":
            return actual == expected
        if op == "!=":
            return actual != expected
        if op == "in":
            return actual in (expected or [])
        if op == "not_in":
            return actual not in (expected or [])
        if op in {">", ">=", "<", "<="}:
            try:
                left = float(actual)
                right = float(expected)
            except (TypeError, ValueError):
                return False
            if op == ">":
                return left > right
            if op == ">=":
                return left >= right
            if op == "<":
                return left < right
            return left <= right
        if op == "truthy":
            return bool(actual)
        if op == "falsy":
            return not bool(actual)
        return False

    def _apply_actions(self, rule, result):
        for action in rule.get("actions", []):
            action_type = action.get("type")
            value = action.get("value")
            constraints = result["constraints"]

            if action_type == "force_action":
                result["forced_action"] = value
            elif action_type == "add_reason":
                result["reasons"].append(value)
            elif action_type == "set":
                constraints[action["key"]] = value
            elif action_type == "block_channel":
                blocked = set(constraints.get("blocked_channels") or [])
                blocked.add(value)
                constraints["blocked_channels"] = sorted(blocked)
            elif action_type == "allow_channels":
                constraints["allowed_channels"] = list(value or [])
            elif action_type == "prefer_channel":
                constraints["preferred_channel"] = value
            elif action_type == "suppress_action":
                suppressed = set(constraints.get("suppressed_actions") or [])
                suppressed.add(value)
                constraints["suppressed_actions"] = sorted(suppressed)
