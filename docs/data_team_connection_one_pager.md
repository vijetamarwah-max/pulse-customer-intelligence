# Pulse AI Data Connection One-Pager

## Objective

Connect three enterprise-owned data streams to Pulse so it can generate behavioral states and next-best-action recommendations:

- user event stream
- CRM/customer profile context
- communication and support history

## 1. Event Stream

Send customer behavioral events with timestamps and user IDs. Use your existing event names; Pulse maps them to canonical meanings.

Example:

```json
{
  "user_id": "U123",
  "events": {
    "raw_events": [
      "Product Viewed",
      "Product Added",
      "Cart Viewed",
      "Checkout Started",
      "Product Added to Wishlist"
    ]
  },
  "user_state": {
    "events_7d": 18,
    "inactive_days": 0,
    "messages_7d": 3
  }
}
```

Minimum fields: `user_id`, `event_name`, `event_timestamp`, `source`. Product, category, order, and session metadata are useful but optional.

## 2. CRM Context

CRM context must contain deterministic enterprise facts, not AI predictions.

Example:

```json
{
  "crm_context": {
    "customer_tier": "gold",
    "ltv_segment": "high_value",
    "total_orders": 18,
    "average_order_value": 220,
    "preferred_channel": "email",
    "timezone": "Asia/Kolkata",
    "support_status": "open_ticket",
    "nps": -35
  }
}
```

Do include profile attributes, purchase history, support status, consent flags, geography, language, tier, and timezone.

Do not include inferred intent, predicted churn, AI-generated state labels, or future-looking model outputs.

## 3. Communication History

Send prior outbound and inbound communication records.

Example:

```json
{
  "comms_history": [
    {
      "channel": "push",
      "direction": "outbound",
      "message": "Complete your cart today",
      "opened": false,
      "clicked": false
    },
    {
      "channel": "support_ticket",
      "direction": "inbound",
      "message": "My refund is unresolved and I am frustrated"
    }
  ]
}
```

Minimum fields: `user_id`, `channel`, `direction`, `message` or campaign metadata, and timestamp. Include open, click, conversion, dismiss, and unsubscribe where available.

## API Shape

For pilot/demo ingestion, send batches to:

```text
POST /api/enterprise-data
GET /api/action-centre?workspace_id=<workspace_id>
```

The backend returns Action Centre-ready recommendations, behavioral state vectors, confidence scores, explanations, expected value, and delivery plans.
