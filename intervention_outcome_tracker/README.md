# Intervention Outcome Tracker

## Purpose

Measure what happened because of a Pulse decision.

This is not a generic analytics layer. It is the causal measurement system that
connects recommendations, execution, observed outcomes, incrementality, and
decision evidence.

## Flow

```text
Behavioral State
        |
Pulse Recommendation
        |
Actual Execution
        |
Observed Outcome
        |
Business Impact
        |
Decision Evidence
```

## Run

```bash
python -m intervention_outcome_tracker.examples.run_example
```
