# Pulse AI Enterprise Training & Pilot Success One-Pager

## What Pulse AI Does

Pulse AI is a decisioning layer for lifecycle, CRM, growth, and retention teams using tools such as Braze, MoEngage, WebEngage, push, email, WhatsApp, SMS, or in-app messaging.

It answers:

> What is the best action to take for this customer right now, considering revenue, fatigue, trust, intent, and business rules?

Pulse does not replace the campaign platform. It decides whether to send, suppress, recover trust, choose a channel, pick a send window, and explain the recommendation.

## What Users See In The Action Centre

Each recommendation includes:

- action: send, suppress, service recovery, retention, content, cart reminder, discount, etc.
- channel and send window, adjusted for quiet hours and user constraints
- confidence score and auto-approval status
- expected value per communication
- explanation, top signals, and alternatives ruled out

Confidence workflow:

| Confidence | Meaning | Workflow |
|---|---|---|
| `> 80%` | High confidence | Eligible for auto-approval |
| `60-80%` | Moderate confidence | Observe or manually approve |
| `< 60%` | Low confidence | Reject or keep out of execution |

Example:

```text
User: Riya Sharma
State: high intent, low fatigue
Recommendation: Wishlist nudge + free shipping
Channel: Push
Send window: Today, 7:40 PM
Confidence: 92%
Expected value: Rs 312
Why: Strong product interest, low fatigue, high push responsiveness.
```

## What To Expect In The First Two Weeks

The first two weeks should prove decision quality, not full autonomous optimization.

Expected outputs:

- connected sample event, CRM, and communication data
- mapped taxonomy for major customer events
- behavioral state generation for a pilot cohort
- Action Centre recommendations with explanations
- suppression, service recovery, channel, timing, and content-type decisions
- first readout against a control group or historical baseline

Recommended pilot scope:

- 1 lifecycle journey or product area
- 5,000 to 50,000 users if data is available
- 2 to 4 channels
- 3 to 5 intervention types
- 1 primary goal: conversion, revenue, retention, or fatigue reduction

## North Star Business Metrics

These are the business outcomes Pulse should ultimately move after the pilot is cleared and a one-month measurement window is available:

| Metric | What To Measure | Expected Direction |
|---|---|---|
| Incremental conversion or revenue lift | Lift versus holdout or historical baseline | Positive lift |
| Reduced marketing spend | Lower sends, fewer low-value touches, better channel mix | Lower spend per conversion |

## MVP Quality Metrics

Use these in the first two weeks:

| Metric | Target |
|---|---:|
| Recommendation action alignment on golden suite | `> 85%` |
| Hard rule violation rate | `0%` |
| Suppression/service-recovery recall | `> 75%` |
| Auto-approve precision | `> 85%` once outcome labels exist |
| Notification reduction in eligible journeys | `10-20%` |

## Pilot Readout Questions

- Which users did Pulse suppress that static journeys would have messaged?
- Which high-intent users received a better channel or time recommendation?
- Which users needed service recovery before marketing?
- Which recommendations had high expected value but low confidence?
- Which custom rules were triggered most often?

Do not overclaim long-term LTV, unsubscribe reduction, or revenue lift in two weeks unless the pilot has a clean holdout group and enough post-send outcome data.

