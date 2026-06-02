# NBA Decision Engine

## Purpose

Choose the next best action from:

- behavioral state
- predicted outcomes
- business goal
- constraints

The NBA engine does not estimate outcomes. It only ranks and selects actions
using predictions produced by the Outcome Estimator.

The output includes deterministic reasoning, counterfactual action values, and
an OpenAI-backed `llm_reasoning` natural-language rationale. Set
`OPENAI_API_KEY` in your environment or local `.env` before running examples.
Optionally set `NBA_LLM_MODEL`; it defaults to `gpt-5.1`.

## Run

```bash
python -m nba_engine.examples.run_example
```
