from event_understanding_agent.embeddings import EmbeddingEngine
from pulse_vector_store.pgvector_store import PGVectorStore
from voice_of_customer_agent.embeddings.similarity import SimilarityMatcher


EVENT_NAMESPACE = "event_behavior_templates"
VOC_NAMESPACE = "voc_canonical_patterns"


def seed_event_templates(store: PGVectorStore) -> None:
    engine = EmbeddingEngine()
    for label, vector in engine.behavior_templates.items():
        store.upsert_embedding(
            namespace=EVENT_NAMESPACE,
            item_id=label,
            label=label,
            text=label.replace("_", " "),
            embedding=vector,
        )


def seed_voc_templates(store: PGVectorStore) -> None:
    matcher = SimilarityMatcher()
    for label, vector in matcher.reference_vectors.items():
        patterns = matcher.canonical_patterns.get(label, [])
        store.upsert_embedding(
            namespace=VOC_NAMESPACE,
            item_id=label,
            label=label,
            text=" | ".join(patterns) or label.replace("_", " "),
            embedding=vector,
        )


def main() -> None:
    store = PGVectorStore()
    store.initialize()
    seed_event_templates(store)
    seed_voc_templates(store)
    print("Seeded pgvector canonical templates.")


if __name__ == "__main__":
    main()
