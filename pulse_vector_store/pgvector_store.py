import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class PGVectorRecord:
    namespace: str
    item_id: str
    label: str
    text: str
    embedding: List[float]
    similarity: Optional[float] = None
    metadata: Optional[Dict] = None


class PGVectorStore:
    """pgvector-backed store for canonical behavior and communication patterns."""

    def __init__(
        self,
        database_url: Optional[str] = None,
        table_name: str = "pulse_embeddings",
        dimension: int = 3,
    ) -> None:
        self.database_url = database_url or os.getenv("PULSE_DATABASE_URL")
        self.table_name = table_name
        self.dimension = dimension

        if not self.database_url:
            raise ValueError("PULSE_DATABASE_URL is required for PGVectorStore.")

    def initialize(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        namespace TEXT NOT NULL,
                        item_id TEXT NOT NULL,
                        label TEXT NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                        embedding vector({self.dimension}) NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                        PRIMARY KEY (namespace, item_id)
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

    def upsert_embedding(
        self,
        namespace: str,
        item_id: str,
        label: str,
        text: str,
        embedding: Iterable[float],
        metadata: Optional[Dict] = None,
    ) -> None:
        embedding_literal = self._embedding_literal(embedding)

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {self.table_name}
                        (namespace, item_id, label, text, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (namespace, item_id)
                    DO UPDATE SET
                        label = EXCLUDED.label,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                    """,
                    (
                        namespace,
                        item_id,
                        label,
                        text,
                        json.dumps(metadata or {}),
                        embedding_literal,
                    ),
                )

    def search_similar(
        self,
        namespace: str,
        embedding: Iterable[float],
        limit: int = 5,
    ) -> List[PGVectorRecord]:
        embedding_literal = self._embedding_literal(embedding)

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                        namespace,
                        item_id,
                        label,
                        text,
                        metadata,
                        embedding::text,
                        1 - (embedding <=> %s::vector) AS similarity
                    FROM {self.table_name}
                    WHERE namespace = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s;
                    """,
                    (embedding_literal, namespace, embedding_literal, limit),
                )

                return [
                    PGVectorRecord(
                        namespace=row[0],
                        item_id=row[1],
                        label=row[2],
                        text=row[3],
                        metadata=row[4],
                        embedding=self._parse_embedding(row[5]),
                        similarity=float(row[6]),
                    )
                    for row in cur.fetchall()
                ]

    def _connect(self):
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError(
                "psycopg is not installed. Run: python -m pip install -r requirements.txt"
            ) from exc

        return psycopg.connect(self.database_url)

    def _embedding_literal(self, embedding: Iterable[float]) -> str:
        values = [float(value) for value in embedding]
        if len(values) != self.dimension:
            raise ValueError(
                f"Expected embedding dimension {self.dimension}, got {len(values)}."
            )
        return "[" + ",".join(str(value) for value in values) + "]"

    def _parse_embedding(self, embedding_text: str) -> List[float]:
        return [float(value) for value in embedding_text.strip("[]").split(",")]
