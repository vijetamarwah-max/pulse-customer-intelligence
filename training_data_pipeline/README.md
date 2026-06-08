# Training Data Pipeline

## Purpose

Build pgvector-backed behavioral memory from real user event streams,
communication history, CRM context, behavioral state, actions, and observed
outcomes.

This is the bridge from product data to model training and outcome retrieval.

## Local Transform Test

```bash
python -m training_data_pipeline.examples.run_training_example
```

## Seed pgvector Behavioral Memory

Requires `PULSE_DATABASE_URL` and a running Postgres database with pgvector:

```bash
python -m training_data_pipeline.examples.seed_pgvector_memory
```
