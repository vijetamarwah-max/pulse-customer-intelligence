class ConfidenceEngine:
    def compute(self, behavioral_state_confidence, outcome_estimation_confidence):
        return round(
            (behavioral_state_confidence * 0.5)
            + (outcome_estimation_confidence * 0.5),
            3,
        )
