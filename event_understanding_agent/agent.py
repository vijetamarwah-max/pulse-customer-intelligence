from typing import Any, Dict, Optional

from .embeddings import EmbeddingEngine
from .llm import LLMReasoning
from .rules import RuleEngine
from .schema import EventUnderstandingOutput


class EventUnderstandingAgent:
    def __init__(
        self,
        embedder: Optional[EmbeddingEngine] = None,
        llm: Optional[LLMReasoning] = None,
        rules: Optional[RuleEngine] = None,
    ) -> None:
        self.embedder = embedder or EmbeddingEngine()
        self.llm = llm or LLMReasoning()
        self.rules = rules or RuleEngine()

    def build_user_embedding(self, events: Dict[str, Any]):
        vector = [
            events.get("view_count", 0) * 0.3,
            events.get("cart_actions", 0) * 0.8,
            events.get("session_depth", 0) * 0.5,
        ]

        return self.embedder.embed_sequence(vector)

    def run(
        self,
        user_id: str,
        events: Dict[str, Any],
        user_state: Dict[str, Any],
    ) -> EventUnderstandingOutput:
        user_embedding = self.build_user_embedding(events)
        embedding_scores = self.embedder.score_intents(user_embedding)
        llm_output = self.llm.infer(events, embedding_scores)
        final_output = self.rules.apply(user_state, llm_output, embedding_scores)

        signal_sources = {
            **embedding_scores,
            "llm_confidence": llm_output["confidence"],
            "rule_adjustment": float(final_output["rule_adjustment"]),
        }

        return EventUnderstandingOutput(
            user_id=user_id,
            purchase_intent=final_output["purchase_intent"],
            exploration_intent=final_output["exploration_intent"],
            churn_risk=final_output["churn_risk"],
            behavioral_tags=final_output["behavioral_tags"],
            confidence=final_output["confidence"],
            explanation=final_output.get("explanation"),
            signal_sources=signal_sources,
        )
