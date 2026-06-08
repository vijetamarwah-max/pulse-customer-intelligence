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

For real state/action/outcome training data, use `training_data_pipeline`:

```bash
python -m training_data_pipeline.examples.run_training_example
python -m training_data_pipeline.examples.seed_pgvector_memory
```

## Decisioning Flow

The refined Pulse AI decisioning flow separates prediction from action choice:

```text
Behavioral State Engine
        |
Behavioral Memory + Similarity Retrieval
        |
Outcome Estimator
        |
Predicted Outcomes
        |
NBA Decision Engine
        |
Recommended Action
```

`behavioral_memory` estimates likely outcomes for possible actions. `nba_engine`
uses those predicted outcomes, business goals, and constraints to choose the
recommended action.

## Cost-Aware Processing

Pulse avoids running LLMs per user. LLMs classify enterprise event types into a
semantic taxonomy when mappings are created or refreshed. Runtime Event
Understanding uses deterministic lookup tables plus embeddings/rules across
users.

Processing defaults:

- Event Understanding: batch every 6-24 hours, configured as 12 hours.
- VoC Agent: runs only when a new call, chat, support ticket, or message arrives.
- Behavioral State Engine: hybrid mode. Critical events refresh state in real
  time; all other states are refreshed in scheduled batch jobs.

## Model Routing

Pulse centralizes model selection in `model_router`:

- Event taxonomy classification: `gpt-5.1`, medium reasoning.
- Event runtime fallback: `gpt-5-mini`, low reasoning, only for low-confidence cases.
- VoC reasoning: `gpt-5.1`, medium reasoning.
- NBA explanation: `gpt-5-mini`, no reasoning, because the decision is already computed.
- Audio transcription: `gpt-4o-transcribe`.

Environment variables in `.env` can override these defaults without changing
agent code.

Event Understanding prompts live in `event_understanding_agent/prompts.py`.
`EVENT_TAXONOMY_CLASSIFICATION_PROMPT` is used for taxonomy-build-time event
classification. `EVENT_RUNTIME_REASONING_PROMPT` is used only for ambiguous or
low-confidence runtime fallback cases after lookup, embeddings, and rules.

VoC reasoning uses `VOC_REASONING_SYSTEM_PROMPT` from
`voice_of_customer_agent/llm/prompts.py`. NBA explanations use
`NBA_EXPLANATION_SYSTEM_PROMPT` from `nba_engine/explanation/prompts.py`.

Run the examples with:

```bash
python -m behavioral_memory.examples.run_example
python -m nba_engine.examples.run_example
```

## Outcome Tracking

`intervention_outcome_tracker` measures causal business impact after Pulse
recommendations are executed. It joins decisions, execution records, observed
outcomes, attribution rules, holdout/control logic, and executive evidence.

Run it with:

```bash
python -m intervention_outcome_tracker.examples.run_example
```

## Frontend Prototype

`pulse_frontend` is a static Lifecycle PM cockpit for diagnosing over-sending,
suppression economics, journey collisions, and per-user next-best-action
evidence.

Open:

```text
pulse_frontend/index.html
```

## API Backend

`pulse_api` exposes REST endpoints for the Lovable frontend:

- `GET /api/health`
- `POST /api/login`
- `GET /api/profile`
- `GET /api/get-data`
- `POST /api/behavioral-state`

Run locally with:

```bash
uvicorn pulse_api.main:app --reload --host 0.0.0.0 --port 8000
```

CORS is enabled for the Lovable production URL and preview URL by default.
Deployment files are included:

- `Dockerfile`
- `render.yaml`
- `Procfile`
- `pulse_api/DEPLOYMENT.md`

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
