# Behavioral Memory and Outcome Estimator

## Purpose

Store historical state/action/outcome records, retrieve similar historical
states, and estimate predicted outcomes for each observed action.

This subsystem predicts what may happen if an action is taken. It does not
choose the action. Action selection belongs to the NBA Decision Engine.

## Run

```bash
python -m behavioral_memory.examples.run_example
```
