import hashlib

from behavioral_memory.embedding_generator import EmbeddingGenerator
from .schema import UserTrainingRecord


class TrainingRecordBuilder:
    def __init__(self) -> None:
        self.embedder = EmbeddingGenerator()

    def build(self, raw_record):
        record = UserTrainingRecord(**raw_record)
        embedding = self.embedder.generate(record.behavioral_state)
        memory_id = self._memory_id(record)

        return {
            "memory_id": memory_id,
            "user_id": record.user_id,
            "action": record.action,
            "state_vector": record.behavioral_state,
            "outcome": record.outcome,
            "embedding": embedding,
            "metadata": {
                "event_count": len(record.event_stream),
                "communication_count": len(record.communication_history),
                "crm_context": record.crm_context,
            },
            "occurred_at": record.occurred_at,
        }

    def _memory_id(self, record):
        raw = f"{record.user_id}|{record.action}|{record.occurred_at}|{record.outcome}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
