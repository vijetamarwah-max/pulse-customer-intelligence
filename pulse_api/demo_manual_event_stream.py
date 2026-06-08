DEMO_MANUAL_EVENT_STREAM = {
    "workspace_id": "default",
    "source_name": "manual_5_user_event_stream_demo",
    "business_goal": "increase_revenue",
    "constraints": {
        "discounts_allowed": False,
        "send_allowed": True,
        "suppress_if_high_fatigue": False,
    },
    "users": [
        {
            "user_id": "U100",
            "events": {
                "raw_events": [
                    "app_open",
                    "product_view",
                    "product_view",
                    "search",
                    "add_to_cart",
                    "checkout_started",
                    "exit",
                ]
            },
            "comms_history": [
                {
                    "channel": "support_ticket",
                    "message": (
                        "I have followed up three times and nobody resolved my "
                        "refund issue. This is frustrating."
                    ),
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "total_orders": 18,
                "average_order_value": 220,
                "last_purchase_days_ago": 12,
            },
            "user_state": {
                "inactive_days": 1,
                "events_7d": 9,
            },
        },
        {
            "user_id": "U101",
            "events": {
                "raw_events": [
                    "app_open",
                    "category_view",
                    "search",
                    "product_view",
                    "wishlist_add",
                ]
            },
            "comms_history": [
                {
                    "channel": "chat",
                    "message": "Thanks, the recommendations are useful. I am still comparing options.",
                }
            ],
            "crm_context": {
                "customer_tier": "silver",
                "ltv_segment": "mid_value",
                "total_orders": 4,
                "average_order_value": 62,
                "last_purchase_days_ago": 31,
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 5,
            },
        },
        {
            "user_id": "U102",
            "events": {
                "raw_events": [
                    "push_sent",
                    "push_ignored",
                    "email_sent",
                    "email_ignored",
                    "whatsapp_sent",
                    "app_open",
                    "exit",
                ]
            },
            "comms_history": [
                {
                    "channel": "whatsapp",
                    "message": "Please stop sending so many messages. This is too much.",
                }
            ],
            "crm_context": {
                "customer_tier": "bronze",
                "ltv_segment": "low_value",
                "total_orders": 1,
                "average_order_value": 28,
                "last_purchase_days_ago": 75,
            },
            "user_state": {
                "inactive_days": 6,
                "events_7d": 1,
            },
        },
        {
            "user_id": "U103",
            "events": {
                "raw_events": [
                    "app_open",
                    "subscription_cancelled",
                    "support_opened",
                    "app_close",
                ]
            },
            "comms_history": [
                {
                    "channel": "email",
                    "message": (
                        "This is unacceptable. I expected better and I am thinking "
                        "of leaving."
                    ),
                }
            ],
            "crm_context": {
                "customer_tier": "platinum",
                "ltv_segment": "high_value",
                "total_orders": 27,
                "average_order_value": 310,
                "last_purchase_days_ago": 4,
            },
            "user_state": {
                "inactive_days": 15,
                "events_7d": 0,
                "recent_complaint": True,
            },
        },
        {
            "user_id": "U104",
            "events": {
                "raw_events": [
                    "app_open",
                    "product_view",
                    "purchase",
                    "app_open",
                    "product_view",
                ]
            },
            "comms_history": [
                {
                    "channel": "chat",
                    "message": "The last order was smooth. Send me updates for new arrivals.",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "total_orders": 22,
                "average_order_value": 180,
                "last_purchase_days_ago": 2,
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 11,
            },
        },
    ],
}
