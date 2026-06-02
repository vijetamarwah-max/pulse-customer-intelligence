class ActionSelector:
    def select(self, ranked_actions):
        if not ranked_actions:
            return "suppress"
        return next(iter(ranked_actions.keys()))
