# Synthetic E-Commerce Test Data

This package contains synthetic e-commerce users for testing Pulse without
enterprise customer data.

The corpus uses Segment-style e-commerce event names, including:

- `Product List Viewed`
- `Product List Filtered`
- `Product Clicked`
- `Product Viewed`
- `Products Searched`
- `Product Added`
- `Cart Viewed`
- `Checkout Started`
- `Payment Info Entered`
- `Order Completed`
- `Order Refunded`
- `Order Cancelled`
- `Product Added to Wishlist`
- `Coupon Entered`
- `Coupon Applied`

## What It Covers

The quick corpus includes 12 deliberately different users:

- high intent cart abandon with high trust
- high intent plus high fatigue and low trust
- browse-only new user
- dormant high-value returning customer
- recent purchase loyal promoter
- discount-sensitive coupon seeker
- refund complaint with retention risk
- wishlist consideration user
- over-messaged low-value user
- urgent checkout or payment failure
- category explorer with email engagement
- high-value low-trust user after a bad delivery

Each user combines:

- event stream
- communication history
- CRM profile
- user state

The payload also includes `evaluation_expectations`. These are review labels
for humans and automated quality checks; they are not used by inference.

## API Usage

Fetch the synthetic payload:

```text
GET /api/test-data/ecommerce-scenarios
```

Run the corpus through Pulse:

```text
POST /api/test-data/run-ecommerce-scenarios
```

Read Action Centre outputs:

```text
GET /api/action-centre?workspace_id=ecommerce_synthetic_eval
```

## Local Smoke Test

```bash
python -m pulse_api.ecommerce_synthetic_smoke_test
```

Review quality across:

- customer behavioral state
- NBA action
- suppression intelligence
- counterfactuals
- LLM reasoning
- processing trace

## Comprehensive Review Corpus

For product review, use the larger corpus:

```text
GET /api/test-data/ecommerce-comprehensive-scenarios
```

It contains 30 labelled users with:

- long, unique event streams
- raw event names and timestamped event objects
- new, loyal, dormant, high-value, low-value, price-sensitive, support-open,
  service-recovery, and campaign-collision CRM states
- voice/chat/email/WhatsApp style communication logs
- synthetic metadata such as direction, timestamp, opened, clicked,
  response time, campaign id, and sentiment hints
- expected review labels for state/action quality evaluation

Run the corpus summary test:

```bash
python -m pulse_api.ecommerce_comprehensive_smoke_test
```
