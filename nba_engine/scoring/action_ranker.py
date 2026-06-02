class ActionRanker:
    def rank(self, action_scores):
        return dict(
            sorted(
                action_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )
