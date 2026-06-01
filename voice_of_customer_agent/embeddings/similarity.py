from typing import Dict, Optional

import numpy as np

from .canonical_patterns import CANONICAL_PATTERNS


class SimilarityMatcher:
    def __init__(self, vector_store: Optional[object] = None) -> None:
        self.vector_store = vector_store
        self.vector_namespace = "voc_canonical_patterns"
        self.canonical_patterns = CANONICAL_PATTERNS
        self.reference_vectors = {
            "frustration_signal": np.array([1.0, 0.2, 0.1]),
            "trust_erosion_signal": np.array([0.8, 0.5, 0.2]),
            "urgency_signal": np.array([0.3, 1.0, 0.2]),
            "retention_risk": np.array([0.2, 0.5, 1.0]),
        }

    def score(self, user_embedding, embedding_engine) -> Dict[str, float]:
        if self.vector_store:
            records = self.vector_store.search_similar(
                namespace=self.vector_namespace,
                embedding=user_embedding,
                limit=len(self.reference_vectors),
            )
            if records:
                return {
                    record.label: max(0.0, min(1.0, float(record.similarity or 0.0)))
                    for record in records
                }

        return {
            label: embedding_engine.cosine_similarity(user_embedding, vector)
            for label, vector in self.reference_vectors.items()
        }
