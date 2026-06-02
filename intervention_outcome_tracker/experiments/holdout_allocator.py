import random


class HoldoutAllocator:
    def assign(self, holdout_pct=10):
        return "CONTROL" if random.randint(1, 100) <= holdout_pct else "PULSE"
