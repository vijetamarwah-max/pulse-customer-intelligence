class WinRateMetrics:
    def calculate(self, wins, total):
        if total == 0:
            return 0.0

        return round(wins / total, 3)
