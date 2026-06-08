from typing import Any, Dict, List

from .embedding_generator import EmbeddingGenerator
from .memory_store import BehavioralMemoryStore
from .outcome_estimator import OutcomeEstimator
from .schema import OutcomeEstimate
from .similarity_engine import SimilarityEngine


class BehavioralMemoryOutcomeEstimator:
    def __init__(self, top_k: int = 3, vector_store=None) -> None:
        self.top_k = top_k
        self.vector_store = vector_store
        self.memory = BehavioralMemoryStore()
        self.embedder = EmbeddingGenerator()
        self.similarity = SimilarityEngine()
        self.estimator = OutcomeEstimator()

    def run(
        self,
        user_id: str,
        state_vector: Dict[str, float],
        historical_records: List[Dict[str, Any]],
    ) -> OutcomeEstimate:
        embedding = self.embedder.generate(state_vector)
        if self.vector_store:
            neighbors = self._retrieve_from_pgvector(embedding)
        else:
            neighbors = self.similarity.retrieve_similar(
                current_embedding=embedding,
                historical_records=historical_records,
                embedder=self.embedder,
                top_k=self.top_k,
            )

        predicted_outcomes = self.estimator.estimate(neighbors)
        confidence = self._confidence(predicted_outcomes)

        return OutcomeEstimate(
            user_id=user_id,
            predicted_outcomes=predicted_outcomes,
            confidence=confidence,
        )

    def _retrieve_from_pgvector(self, embedding):
        matches = self.vector_store.search_similar(embedding=embedding, limit=self.top_k)
        return [
            (
                match.similarity,
                {
                    "state_vector": match.state_vector,
                    "action": match.action,
                    **match.outcome,
                },
            )
            for match in matches
        ]

    def _confidence(self, predicted_outcomes: Dict[str, Dict[str, float]]) -> float:
        if not predicted_outcomes:
            return 0.0

        sample_sizes = [outcome["sample_size"] for outcome in predicted_outcomes.values()]
        similarities = [
            outcome["average_similarity"] for outcome in predicted_outcomes.values()
        ]

        sample_confidence = min(sum(sample_sizes) / max(self.top_k, 1), 1.0)
        similarity_confidence = sum(similarities) / len(similarities)

        return round((sample_confidence * 0.4) + (similarity_confidence * 0.6), 3)
