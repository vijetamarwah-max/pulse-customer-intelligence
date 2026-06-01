# Behavioral State Engine

## Purpose

Fuse:

- Event Understanding signals
- Voice of Customer signals
- CRM context

into a unified behavioral state vector.

This is the central customer cognition layer of Pulse. It converts fragmented
signals, enterprise context, and communication understanding into a stable
behavioral state representation.

## Architecture

```text
Event Understanding Agent
        +
Voice of Customer Agent
        +
CRM Variables
        |
Signal Fusion Layer
        |
Feature Construction Layer
        |
Behavioral Scoring Models
        |
State Normalization Layer
        |
Unified Customer State Vector
```

## Outputs

- purchase_readiness
- engagement_probability
- communication_fatigue
- retention_risk
- trust_level
- discount_sensitivity
- brand_affinity
- intervention_receptiveness

## Run

From the repository root:

```bash
python -m behavioral_state_engine.examples.run_example
```

From inside `behavioral_state_engine/`:

```bash
python examples/run_example.py
```

## Next Step

The next system should be the NBA Decision Engine, which consumes this state
vector and performs suppression, channel optimization, timing optimization, and
intervention selection.
