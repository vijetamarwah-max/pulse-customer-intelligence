import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class BehavioralMemoryMatch:
    memory_id: str
    user_id: str
    action: str
    outcome: Dict
    state_vector: Dict
    similarity: float


class BehavioralMemoryPGVectorStore:
    """pgvector store for historical state/action/outcome memory."""

    def __init__(
        self,
        database_url: Optional[str] = None,
        table_name: str = "pulse_behavioral_memory",
        dimension: int = 5,
        connect_timeout_seconds: int = 5,
    ) -> None:
        self.database_url = database_url or os.getenv("PULSE_DATABASE_URL")
        self.table_name = table_name
        self.dimension = dimension
        self.connect_timeout_seconds = connect_timeout_seconds

        if not self.database_url:
            raise ValueError("PULSE_DATABASE_URL is required for behavioral memory.")

    def initialize(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        memory_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        action TEXT NOT NULL,
                        state_vector JSONB NOT NULL,
                        outcome JSONB NOT NULL,
                        metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                        embedding vector({self.dimension}) NOT NULL,
                        occurred_at TIMESTAMPTZ,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                    );
                    """
                )
                cur.execute(
                    f"""
                    CREATE INDEX IF NOT EXISTS {self.table_name}_embedding_idx
                    ON {self.table_name}
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                    """
                )
                conn.commit()

    def upsert_memory(
        self,
        memory_id: str,
        user_id: str,
        action: str,
        state_vector: Dict,
        outcome: Dict,
        embedding: Iterable[float],
        metadata: Optional[Dict] = None,
        occurred_at: Optional[str] = None,
    ) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {self.table_name}
                        (
                            memory_id,
                            user_id,
                            action,
                            state_vector,
                            outcome,
                            metadata,
                            embedding,
                            occurred_at
                        )
                    VALUES (%s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s::vector, %s)
                    ON CONFLICT (memory_id)
                    DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        action = EXCLUDED.action,
                        state_vector = EXCLUDED.state_vector,
                        outcome = EXCLUDED.outcome,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding,
                        occurred_at = EXCLUDED.occurred_at;
                    """,
                    (
                        memory_id,
                        user_id,
                        action,
                        json.dumps(state_vector),
                        json.dumps(outcome),
                        json.dumps(metadata or {}),
                        self._embedding_literal(embedding),
                        occurred_at,
                    ),
                )
                conn.commit()

    def search_similar(
        self,
        embedding: Iterable[float],
        limit: int = 20,
        action: Optional[str] = None,
    ) -> List[BehavioralMemoryMatch]:
        embedding_literal = self._embedding_literal(embedding)
        action_filter = "AND action = %s" if action else ""
        params = [embedding_literal, embedding_literal]
        if action:
            params.append(action)
        params.append(limit)

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                        memory_id,
                        user_id,
                        action,
                        state_vector,
                        outcome,
                        1 - (embedding <=> %s::vector) AS similarity
                    FROM {self.table_name}
                    WHERE 1 = 1
                    {action_filter}
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s;
                    """,
                    params,
                )

                return [
                    BehavioralMemoryMatch(
                        memory_id=row[0],
                        user_id=row[1],
                        action=row[2],
                        state_vector=row[3],
                        outcome=row[4],
                        similarity=float(row[5]),
                    )
                    for row in cur.fetchall()
                ]

    def _connect(self):
        import psycopg

        return psycopg.connect(
            self.database_url,
            connect_timeout=self.connect_timeout_seconds,
        )

    def _embedding_literal(self, embedding: Iterable[float]) -> str:
        values = [float(value) for value in embedding]
        if len(values) != self.dimension:
            raise ValueError(
                f"Expected embedding dimension {self.dimension}, got {len(values)}."
            )
        return "[" + ",".join(str(value) for value in values) + "]"
