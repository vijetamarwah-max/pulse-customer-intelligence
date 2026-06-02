class BusinessGoalEngine:
    GOAL_WEIGHTS = {
        "increase_revenue": {
            "revenue": 1.0,
            "engagement": 0.2,
            "retention": 0.3,
        },
        "increase_retention": {
            "revenue": 0.2,
            "engagement": 0.3,
            "retention": 1.0,
        },
        "increase_engagement": {
            "revenue": 0.2,
            "engagement": 1.0,
            "retention": 0.3,
        },
    }

    def get_weights(self, goal):
        if goal not in self.GOAL_WEIGHTS:
            raise ValueError(f"Unsupported business goal: {goal}")
        return self.GOAL_WEIGHTS[goal]
