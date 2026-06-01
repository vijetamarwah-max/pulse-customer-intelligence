from typing import Dict, Iterable, Optional

import numpy as np


class EmbeddingEngine:
    """Fast pattern recognition layer for behavior-template similarity."""

    def __init__(self, vector_store: Optional[object] = None) -> None:
        self.vector_store = vector_store
        self.vector_namespace = "event_behavior_templates"
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
        if self.vector_store:
            records = self.vector_store.search_similar(
                namespace=self.vector_namespace,
                embedding=user_embedding,
                limit=len(self.behavior_templates),
            )
            if records:
                return {
                    record.label: max(0.0, min(1.0, float(record.similarity or 0.0)))
                    for record in records
                }

        return {
            intent: self.cosine_similarity(user_embedding, template_vec)
            for intent, template_vec in self.behavior_templates.items()
        }
