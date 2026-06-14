from datetime import datetime, timedelta


BASE_TIME = datetime(2026, 6, 12, 10, 0, 0)


def _event_stream(raw_events, start_offset_hours, channel, device, product, category):
    return [
        {
            "event_id": f"evt_{start_offset_hours}_{index + 1:02d}",
            "event_name": event_name,
            "timestamp": (
                BASE_TIME
                - timedelta(hours=start_offset_hours)
                + timedelta(minutes=index * 11)
            ).isoformat()
            + "Z",
            "source": "segment",
            "channel": channel,
            "device": device,
            "properties": {
                "product_name": product,
                "category": category,
                "session_id": f"sess_{start_offset_hours}",
                "currency": "INR",
                "value": 1499 + (index * 125),
            },
        }
        for index, event_name in enumerate(raw_events)
    ]


def _events(raw_events, start_offset_hours, channel, device, product, category):
    return {
        "raw_events": raw_events,
        "event_stream": _event_stream(
            raw_events=raw_events,
            start_offset_hours=start_offset_hours,
            channel=channel,
            device=device,
            product=product,
            category=category,
        ),
    }


DEMO_MANUAL_EVENT_STREAM = {
    "workspace_id": "default",
    "source_name": "manual_5_user_event_stream_demo",
    "business_goal": "increase_revenue",
    "constraints": {
        "discounts_allowed": False,
        "send_allowed": True,
        "suppress_if_high_fatigue": False,
        "quiet_hours": {
            "start": "21:00",
            "end": "09:00",
        },
    },
    "users": [
        {
            "user_id": "U100",
            "scenario": "high_intent_open_refund_issue",
            "events": _events(
                [
                    "Product List Viewed",
                    "Product Viewed",
                    "Product Viewed",
                    "Products Searched",
                    "Product Added",
                    "Cart Viewed",
                    "Checkout Started",
                    "Payment Info Entered",
                    "Checkout Step Viewed",
                    "app_close",
                ],
                3,
                "mobile_app",
                "ios",
                "Noise Cancelling Headphones",
                "Electronics",
            ),
            "comms_history": [
                {
                    "channel": "support_ticket",
                    "direction": "inbound",
                    "message": (
                        "I have followed up three times and nobody resolved my "
                        "refund issue. This is frustrating."
                    ),
                    "sent_at": "2026-06-12T08:45:00Z",
                    "sentiment_hint": "negative",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "checkout_blocked",
                "total_orders": 18,
                "average_order_value": 220,
                "last_purchase_days_ago": 12,
                "preferred_channel": "email",
                "timezone": "Asia/Kolkata",
                "support_status": "open_ticket",
                "nps": -35,
            },
            "user_state": {
                "inactive_days": 1,
                "events_7d": 10,
                "messages_7d": 5,
                "recent_complaint": True,
                "support_ticket_open_days": 5,
            },
        },
        {
            "user_id": "U101",
            "scenario": "wishlist_consideration_comparing_options",
            "events": _events(
                [
                    "Product List Viewed",
                    "Product List Filtered",
                    "Products Searched",
                    "Product Viewed",
                    "Product Added to Wishlist",
                    "Product Viewed",
                    "Product Added to Wishlist",
                    "app_close",
                ],
                8,
                "web",
                "desktop",
                "Running Shoes",
                "Footwear",
            ),
            "comms_history": [
                {
                    "channel": "chat",
                    "direction": "inbound",
                    "message": "Thanks, the recommendations are useful. I am still comparing options.",
                    "sent_at": "2026-06-11T18:10:00Z",
                    "sentiment_hint": "positive",
                }
            ],
            "crm_context": {
                "customer_tier": "silver",
                "ltv_segment": "mid_value",
                "lifecycle_stage": "consideration",
                "total_orders": 4,
                "average_order_value": 62,
                "last_purchase_days_ago": 31,
                "preferred_channel": "push",
                "timezone": "Asia/Kolkata",
                "support_status": "none",
                "nps": 42,
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 8,
                "messages_7d": 1,
            },
        },
        {
            "user_id": "U102",
            "scenario": "over_messaged_low_value_unresponsive",
            "events": _events(
                [
                    "push_sent",
                    "push_ignored",
                    "email_sent",
                    "email_ignored",
                    "whatsapp_sent",
                    "whatsapp_ignored",
                    "Product List Viewed",
                    "Product Viewed",
                    "app_close",
                ],
                14,
                "mobile_app",
                "android",
                "Budget Backpack",
                "Accessories",
            ),
            "comms_history": [
                {
                    "channel": "whatsapp",
                    "direction": "inbound",
                    "message": (
                        "Please stop sending so many messages. This is frustrating "
                        "and too much."
                    ),
                    "sent_at": "2026-06-10T20:30:00Z",
                    "sentiment_hint": "negative",
                }
            ],
            "crm_context": {
                "customer_tier": "bronze",
                "ltv_segment": "low_value",
                "lifecycle_stage": "fatigued",
                "total_orders": 1,
                "average_order_value": 28,
                "last_purchase_days_ago": 75,
                "preferred_channel": "none",
                "timezone": "Asia/Kolkata",
                "support_status": "none",
                "nps": 5,
            },
            "user_state": {
                "inactive_days": 6,
                "events_7d": 3,
                "messages_7d": 11,
                "ignored_comms_days": 14,
            },
        },
        {
            "user_id": "U103",
            "scenario": "high_value_churn_risk_service_recovery",
            "events": _events(
                [
                    "app_open",
                    "Product Viewed",
                    "Order Cancelled",
                    "support_complaint",
                    "subscription_cancelled",
                    "support_opened",
                    "app_close",
                ],
                26,
                "mobile_app",
                "ios",
                "Annual Membership",
                "Subscription",
            ),
            "comms_history": [
                {
                    "channel": "email",
                    "direction": "inbound",
                    "message": (
                        "This is unacceptable. I expected better and I am thinking "
                        "of leaving."
                    ),
                    "sent_at": "2026-06-09T09:20:00Z",
                    "sentiment_hint": "negative",
                }
            ],
            "crm_context": {
                "customer_tier": "platinum",
                "ltv_segment": "high_value",
                "lifecycle_stage": "trust_recovery",
                "total_orders": 27,
                "average_order_value": 310,
                "last_purchase_days_ago": 4,
                "preferred_channel": "phone",
                "timezone": "Asia/Kolkata",
                "support_status": "escalated_ticket",
                "nps": -62,
            },
            "user_state": {
                "inactive_days": 15,
                "events_7d": 0,
                "messages_7d": 6,
                "recent_complaint": True,
                "support_ticket_open_days": 16,
            },
        },
        {
            "user_id": "U104",
            "scenario": "recent_purchase_loyal_new_arrivals",
            "events": _events(
                [
                    "Product Viewed",
                    "Product Added",
                    "Cart Viewed",
                    "Checkout Started",
                    "Payment Info Entered",
                    "Order Completed",
                    "Product Reviewed",
                    "Product List Viewed",
                    "Product Viewed",
                ],
                35,
                "mobile_app",
                "ios",
                "Premium Coffee Maker",
                "Home",
            ),
            "comms_history": [
                {
                    "channel": "chat",
                    "direction": "inbound",
                    "message": "The last order was smooth. Send me updates for new arrivals.",
                    "sent_at": "2026-06-12T06:15:00Z",
                    "sentiment_hint": "positive",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "loyal",
                "total_orders": 22,
                "average_order_value": 180,
                "last_purchase_days_ago": 2,
                "preferred_channel": "in_app",
                "timezone": "Asia/Kolkata",
                "support_status": "none",
                "nps": 68,
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 11,
                "messages_7d": 1,
            },
        },
    ],
    "historical_outcomes": [
        {
            "state_vector": {
                "purchase_readiness": 0.88,
                "communication_fatigue": 0.12,
                "trust_level": 0.86,
                "retention_risk": 0.18,
                "engagement_probability": 0.74,
            },
            "action": "send_product_recommendation",
            "converted": True,
            "revenue": 260,
            "engagement": 0.82,
            "retention": 0.58,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.84,
                "communication_fatigue": 0.16,
                "trust_level": 0.82,
                "retention_risk": 0.20,
                "engagement_probability": 0.70,
            },
            "action": "send_cart_reminder",
            "converted": True,
            "revenue": 235,
            "engagement": 0.76,
            "retention": 0.56,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.82,
                "communication_fatigue": 0.14,
                "trust_level": 0.84,
                "retention_risk": 0.18,
                "engagement_probability": 0.72,
            },
            "action": "send_content",
            "converted": True,
            "revenue": 138,
            "engagement": 0.86,
            "retention": 0.62,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.86,
                "communication_fatigue": 0.18,
                "trust_level": 0.80,
                "retention_risk": 0.22,
                "engagement_probability": 0.68,
            },
            "action": "send_discount_offer",
            "converted": True,
            "revenue": 210,
            "engagement": 0.78,
            "retention": 0.55,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.80,
                "communication_fatigue": 0.10,
                "trust_level": 0.88,
                "retention_risk": 0.16,
                "engagement_probability": 0.76,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 15,
            "engagement": 0.10,
            "retention": 0.70,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.30,
                "communication_fatigue": 0.90,
                "trust_level": 0.24,
                "retention_risk": 0.66,
                "engagement_probability": 0.18,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 92,
            "engagement": 0.08,
            "retention": 0.86,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.34,
                "communication_fatigue": 0.86,
                "trust_level": 0.28,
                "retention_risk": 0.62,
                "engagement_probability": 0.20,
            },
            "action": "service_recovery",
            "converted": False,
            "revenue": 74,
            "engagement": 0.44,
            "retention": 0.82,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.28,
                "communication_fatigue": 0.88,
                "trust_level": 0.26,
                "retention_risk": 0.70,
                "engagement_probability": 0.16,
            },
            "action": "send_retention_message",
            "converted": False,
            "revenue": 42,
            "engagement": 0.28,
            "retention": 0.74,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.32,
                "communication_fatigue": 0.84,
                "trust_level": 0.30,
                "retention_risk": 0.64,
                "engagement_probability": 0.22,
            },
            "action": "send_product_recommendation",
            "converted": False,
            "revenue": 10,
            "engagement": 0.12,
            "retention": 0.35,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.26,
                "communication_fatigue": 0.92,
                "trust_level": 0.22,
                "retention_risk": 0.68,
                "engagement_probability": 0.14,
            },
            "action": "send_discount_offer",
            "converted": False,
            "revenue": 8,
            "engagement": 0.10,
            "retention": 0.30,
        },
    ],
}
