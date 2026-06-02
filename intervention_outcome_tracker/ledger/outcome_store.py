class OutcomeStore:
    def __init__(self):
        self.outcomes = []

    def write(self, outcome):
        self.outcomes.append(outcome)

    def all(self):
        return self.outcomes
