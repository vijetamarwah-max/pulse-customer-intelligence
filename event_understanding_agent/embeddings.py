from typing import Dict, Iterable

import numpy as np


class EmbeddingEngine:
    """Fast pattern recognition layer for behavior-template similarity."""

    def __init__(self) -> None:
        self.behavior_templates = {
            "purchase_intent": np.array([1.0, 0.8, 0.2]),
            "exploration_intent": np.array([0.7, 1.0, 0.3]),
            "churn_risk": np.array([0.1, 0.2, 1.0]),
        }

    def embed_sequence(self, event_vector: Iterable[float]) -> np.ndarray:
        return np.array(list(event_vector), dtype=float)

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denominator = np.linalg.norm(a) * np.linalg.norm(b)
        if denominator == 0:
            return 0.0

        similarity = float(np.dot(a, b) / denominator)
        return max(0.0, min(1.0, similarity))

    def score_intents(self, user_embedding: np.ndarray) -> Dict[str, float]:
        return {
            intent: self.cosine_similarity(user_embedding, template_vec)
            for intent, template_vec in self.behavior_templates.items()
        }
