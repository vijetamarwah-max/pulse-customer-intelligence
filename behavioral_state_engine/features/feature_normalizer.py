from typing import Dict


class FeatureNormalizer:
    def normalize(self, state: Dict[str, float]) -> Dict[str, float]:
        normalized = {}

        for key, value in state.items():
            normalized[key] = self._bounded(value)

        return normalized

    def _bounded(self, value: float) -> float:
        return round(min(max(float(value), 0.0), 1.0), 3)
