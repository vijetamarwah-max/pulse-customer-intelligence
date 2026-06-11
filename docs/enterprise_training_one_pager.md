# Pulse AI Enterprise Training One-Pager

## Who This Is For

Pulse AI is for lifecycle, CRM, growth, and retention teams that already run campaigns in tools such as Braze, MoEngage, WebEngage, email, WhatsApp, SMS, push, or in-app channels.

The product helps answer one question:

> What is the best action to take for this customer right now, considering revenue, fatigue, trust, intent, and business rules?

## What Pulse Produces

Pulse turns event behavior, communication history, and CRM context into an Action Centre queue.

Each recommendation includes:

- recommended action: send, suppress, service recovery, retention, content, cart reminder, discount, etc.
- channel: push, email, WhatsApp, SMS, in-app, chat, phone, or no message
- send window: recommended local time, adjusted for quiet hours
- expected value per communication
- confidence score
- explanation and alternatives ruled out
- auto-approve eligibility

## How To Read The Action Centre

| Confidence | Meaning | Suggested Workflow |
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

## What Good Usage Looks Like

Start by reviewing recommendation patterns, not individual rows only.

Look for:

- which journeys are over-sending
- which users should be suppressed
- which high-value users need service recovery before marketing
- which recommendations have high expected value but low confidence
- which business rules are frequently overriding AI decisions

## Key Operating Principle

Pulse is not a campaign builder. It is a decisioning layer.

Your campaign platform still sends the message. Pulse decides whether to send, what intervention type to use, which channel to prefer, when to send, and when not to disturb the customer.

