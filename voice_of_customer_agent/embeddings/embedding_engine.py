from typing import Iterable

import numpy as np


class VOCEmbeddingEngine:
    def embed(self, text_vector: Iterable[float]) -> np.ndarray:
        return np.array(list(text_vector), dtype=float)

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denominator = np.linalg.norm(a) * np.linalg.norm(b)
        if denominator == 0:
            return 0.0

        similarity = float(np.dot(a, b) / denominator)
        return max(0.0, min(1.0, similarity))
