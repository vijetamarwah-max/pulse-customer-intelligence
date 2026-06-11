# Pulse AI API

FastAPI backend for the Pulse AI frontend.

## CORS

Allowed origins are configured in `pulse_api/config.py` and can be overridden
with:

```text
PULSE_CORS_ORIGINS=https://pulse-customer-intelligence.lovable.app,https://pulse-behavior-ai.lovable.app,https://your-production-domain.com
```

Default allowed origins include:

- `https://pulse-behavior-ai.lovable.app`
- `https://pulse-customer-intelligence.lovable.app`
- `https://id-preview--8ca02ac1-f8a8-4c13-ba27-d65509f12369.lovable.app`
- local development origins

## Run

```bash
uvicorn pulse_api.main:app --reload --host 0.0.0.0 --port 8000
```

Production entrypoint:

```bash
uvicorn pulse_api.asgi:app --host 0.0.0.0 --port 8000
```

## Smoke Test

```bash
python -m pulse_api.smoke_test
python -m pulse_api.enterprise_smoke_test
```

## Frontend Endpoints

- `GET /api/profile`
- `GET /api/get-data`
- `POST /api/login`
- `POST /api/behavioral-state`
- `POST /api/enterprise-data`
- `GET /api/action-centre`
- `GET /api/demo/manual-event-stream`
- `POST /api/demo/run-manual-event-stream`
- `GET /api/test-data/ecommerce-scenarios`
- `POST /api/test-data/run-ecommerce-scenarios`
- `GET /api/test-data/ecommerce-comprehensive-scenarios`
- `POST /api/test-data/run-ecommerce-comprehensive-scenarios`

## Enterprise Data Flow

Lovable should use this flow when a user connects or uploads enterprise data:

1. Send events, comms history, CRM context, goals, and constraints to:

```text
POST /api/enterprise-data
```

2. Load live Action Centre recommendations from:

```text
GET /api/action-centre
```

3. Continue loading the dashboard from:

```text
GET /api/get-data
```

After enterprise data is ingested, `/api/get-data` returns `data_mode:
enterprise_connected`. Before ingestion, it returns `data_mode: demo`.

Example ingestion payload:

```json
{
  "workspace_id": "default",
  "source_name": "braze_segment_upload",
  "business_goal": "increase_revenue",
  "constraints": {
    "discounts_allowed": false,
    "send_allowed": true,
    "suppress_if_high_fatigue": false
  },
  "users": [
    {
      "user_id": "U100",
      "events": {
        "raw_events": [
          "product_view",
          "search",
          "add_to_cart",
          "checkout_started"
        ]
      },
      "comms_history": [
        {
          "channel": "support_ticket",
          "message": "I have followed up three times and nobody resolved my issue. This is frustrating."
        }
      ],
      "crm_context": {
        "customer_tier": "gold",
        "ltv_segment": "high_value",
        "total_orders": 18,
        "average_order_value": 220
      },
      "user_state": {
        "inactive_days": 1,
        "events_7d": 8
      }
    }
  ]
}
```

See `DEPLOYMENT.md` for Render deployment steps.

## Manual 5-User Demo Flow

Use this when the user wants to simulate connecting enterprise event stream data
without a real connector.

1. Load the editable demo payload:

```text
GET /api/demo/manual-event-stream
```

2. Let the user review or edit the five users:

- raw event stream
- communication history
- CRM context
- user state

3. Either submit the edited payload to:

```text
POST /api/enterprise-data
```

Or run the default 5-user demo immediately:

```text
POST /api/demo/run-manual-event-stream
```

4. Show the processing journey from:

```text
GET /api/action-centre
```

The response includes `processing_trace`, where each user has these steps:

- Manual Event Stream
- Event Understanding Agent
- Voice of Customer Agent
- CRM Context
- Behavioral State Engine
- Outcome Estimator
- NBA Decision Engine

Render this trace next to each recommendation to show how Pulse moves from
manual events to Action Centre decisions.

## Synthetic E-Commerce Evaluation Corpus

Use this when testing Pulse quality without real enterprise data.

Fetch 12 synthetic users with Segment-style e-commerce events, communication
history, CRM profiles, and user state:

```text
GET /api/test-data/ecommerce-scenarios
```

Run the full corpus through Pulse:

```text
POST /api/test-data/run-ecommerce-scenarios
```

Inspect recommendations:

```text
GET /api/action-centre?workspace_id=ecommerce_synthetic_eval
```

Local test:

```bash
python -m pulse_api.ecommerce_synthetic_smoke_test
python -m pulse_api.ecommerce_comprehensive_smoke_test
```

For deeper product review, use:

```text
GET /api/test-data/ecommerce-comprehensive-scenarios
```

This returns 30 labelled e-commerce users. Each user has a long unique Segment-style event stream, rich CRM state, user state, and synthetic voice/chat/email/WhatsApp logs with timestamps and metadata.

## Configurable NBA Rules

Tenant and user constraints can be passed in the request payload. The examples
below are configuration, not hardcoded product behavior.

```json
{
  "constraints": {
    "quiet_hours": {"start": "21:00", "end": "09:00"},
    "allowed_channels": ["push", "email"],
    "blocked_channels": ["whatsapp"],
    "custom_rules": [
      {
        "id": "support_ticket_dnd",
        "when": {
          "all": [
            {"field": "support_status", "op": "in", "value": ["open_ticket", "escalated_ticket"]},
            {"field": "support_ticket_open_days", "op": ">=", "value": 14}
          ]
        },
        "actions": [
          {"type": "force_action", "value": "suppress"},
          {"type": "add_reason", "value": "custom_rule_support_ticket_open_14_days"}
        ]
      }
    ]
  }
}
```

Supported condition operators:

- `==`
- `!=`
- `>`
- `>=`
- `<`
- `<=`
- `in`
- `not_in`
- `truthy`
- `falsy`

Supported rule actions:

- `force_action`
- `add_reason`
- `set`
- `block_channel`
- `allow_channels`
- `prefer_channel`
- `suppress_action`

Rules can evaluate request-level/user-level fields such as
`support_status`, `support_ticket_open_days`, `messages_7d`, and
`recent_complaint`, plus state fields using the `state.` prefix, for example
`state.communication_fatigue`.
