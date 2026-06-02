class AttributionRules:
    def purchase_attributed(self, outcome):
        return bool(outcome.get("purchased", False))
