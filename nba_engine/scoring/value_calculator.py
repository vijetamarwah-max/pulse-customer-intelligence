class ValueCalculator:
    def calculate(self, predicted_outcomes, goal_weights, allowed_actions):
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

            values[action] = round(score, 3)

        return values
