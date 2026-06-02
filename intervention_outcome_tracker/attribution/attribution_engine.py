from .attribution_rules import AttributionRules


class AttributionEngine:
    def __init__(self):
        self.rules = AttributionRules()

    def attribute(self, outcome):
        return self.rules.purchase_attributed(outcome)
