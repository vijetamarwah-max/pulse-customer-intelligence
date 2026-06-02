from typing import Dict, Iterable, List, Tuple

import numpy as np


class SimilarityEngine:
    def cosine_similarity(self, a: Iterable[float], b: Iterable[float]) -> float:
        vec_a = np.array(list(a), dtype=float)
        vec_b = np.array(list(b), dtype=float)
        denominator = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
        if denominator == 0:
            return 0.0

        similarity = float(np.dot(vec_a, vec_b) / denominator)
        return max(0.0, min(1.0, similarity))

    def retrieve_similar(
        self,
        current_embedding: Iterable[float],
        historical_records: List[Dict],
        embedder,
        top_k: int = 3,
    ) -> List[Tuple[float, Dict]]:
        scored = []

        for record in historical_records:
            historical_embedding = embedder.generate(record["state_vector"])
            similarity = self.cosine_similarity(current_embedding, historical_embedding)
            scored.append((similarity, record))

        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[:top_k]
