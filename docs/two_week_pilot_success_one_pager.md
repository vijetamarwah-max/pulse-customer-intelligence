# Pulse AI Two-Week Pilot Success One-Pager

## What To Expect In Two Weeks

The goal of the first two weeks is not full autonomous campaign optimization. The goal is to prove that Pulse can identify better customer-level decisions than static journeys.

By the end of two weeks, you should expect:

- connected sample data from events, CRM, and communication history
- mapped event taxonomy for major customer actions
- customer behavioral state generation
- Action Centre recommendations for a pilot cohort
- suppression, service recovery, channel, timing, and content-type decisions
- explanations for every recommendation
- a first measurement readout against a control or historical baseline

## Recommended Pilot Scope

Start narrow:

- 1 product area or lifecycle journey
- 5,000 to 50,000 users if data is available
- 2 to 4 channels
- 3 to 5 intervention types
- 1 primary business goal, such as conversion, retention, or revenue

Example pilot:

```text
Journey: Cart abandonment and browsing recovery
Channels: Push, email, WhatsApp
Goal: Increase conversion without increasing fatigue
Guardrails: No WhatsApp after 9 PM; suppress open support tickets; max 2 sends per day
```

## How To Measure Success

Core MVP metrics:

| Metric | Target |
|---|---:|
| Recommendation action alignment on golden suite | `> 85%` |
| Hard rule violation rate | `0%` |
| Suppression/service-recovery recall | `> 75%` |
| Auto-approve precision | `> 85%` once outcome labels exist |
| Notification reduction | `10-20%` in eligible journeys |
| CTR or conversion uplift | directional positive in pilot |

## Pilot Readout Questions

At the end of week two, answer:

- Which users did Pulse suppress that static journeys would have messaged?
- Which high-intent users received a better channel or time recommendation?
- Which users needed service recovery before marketing?
- Which recommendations had high expected value but low confidence?
- Which custom business rules were triggered most often?

## What Not To Overclaim Yet

In two weeks, do not overclaim long-term revenue lift, LTV impact, or unsubscribe reduction unless the pilot has a proper holdout group and enough post-send outcome data.

The strongest early proof is decision quality: fewer bad sends, better prioritization, and clearer reasoning for lifecycle teams.

