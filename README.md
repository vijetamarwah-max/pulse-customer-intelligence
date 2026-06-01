# Event Understanding Agent

Hybrid event inference engine combining:

- embedding similarity for fast behavior-pattern recognition
- LLM-style semantic reasoning for ambiguity and mixed signals
- deterministic rules for overrides, suppressions, and safety

## Structure

```text
event_understanding_agent/
├── agent.py
├── embeddings.py
├── rules.py
├── llm.py
├── schema.py
├── run_example.py
└── __init__.py
```

## Run

```bash
pip install -r requirements.txt
python -m event_understanding_agent.run_example
```

## Local Secrets

For OpenAI-backed audio transcription, create a local `.env` file from
`.env.example` and set `OPENAI_API_KEY`. The `.env` file is ignored by Git.

For pgvector-backed similarity search, set `PULSE_DATABASE_URL` in `.env`.

## Vector Store

Pulse uses pgvector as the production vector database. The current agents still
run with in-memory NumPy vectors by default, but they can use `PGVectorStore`
when a Postgres database with the pgvector extension is available.

Seed canonical Event and VoC templates with:

```bash
python -m pulse_vector_store.seed_pgvector
```

## Output Contract

The agent returns `EventUnderstandingOutput`, a strict Pydantic model with:

- `user_id`
- `purchase_intent`
- `exploration_intent`
- `churn_risk`
- `behavioral_tags`
- `confidence`
- `explanation`
- `signal_sources`

## Replacement Points

- Replace `EmbeddingEngine.embed_sequence` and `behavior_templates` with OpenAI, SBERT, or another embedding backend.
- Replace `LLMReasoning.infer` with a model call that accepts event streams, embedding scores, and communication signals.
- Extend `RuleEngine.apply` with enterprise policy, suppression, audit, and compliance rules.
