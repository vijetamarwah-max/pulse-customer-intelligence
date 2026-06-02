class DecisionLedger:
    def __init__(self):
        self.records = []

    def write(self, record):
        self.records.append(record)

    def all(self):
        return self.records
