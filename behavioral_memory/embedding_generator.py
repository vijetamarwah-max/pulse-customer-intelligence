from typing import Dict, List


class EmbeddingGenerator:
    """MVP embedding generator.

    For now, the behavioral state vector itself is the embedding. This can later
    be replaced with learned embeddings or pgvector-backed state embeddings.
    """

    FEATURE_ORDER = [
        "purchase_readiness",
        "communication_fatigue",
        "trust_level",
        "retention_risk",
        "engagement_probability",
    ]

    def generate(self, state_vector: Dict[str, float]) -> List[float]:
        return [float(state_vector.get(feature, 0.0)) for feature in self.FEATURE_ORDER]
