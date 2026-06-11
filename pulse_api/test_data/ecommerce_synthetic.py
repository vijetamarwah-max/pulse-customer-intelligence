ECOMMERCE_SYNTHETIC_TEST_PAYLOAD = {
    "workspace_id": "ecommerce_synthetic_eval",
    "source_name": "synthetic_segment_ecommerce_event_stream",
    "business_goal": "increase_revenue",
    "constraints": {
        "discounts_allowed": True,
        "send_allowed": True,
        "suppress_if_high_fatigue": False,
        "quiet_hours": {
            "start": "21:00",
            "end": "09:00",
        },
    },
    "evaluation_expectations": {
        "high_intent_cart_abandon_high_trust": {
            "expected_state": "high_intent_receptive",
            "expected_action_family": "cart_reminder_or_product_recommendation",
            "quality_question": "Does Pulse nudge conversion without suppressing a receptive buyer?",
        },
        "high_intent_high_fatigue_low_trust": {
            "expected_state": "high_intent_high_fatigue_or_low_trust_high_fatigue",
            "expected_action_family": "suppress_or_service_recovery",
            "quality_question": "Does Pulse avoid a generic discount when trust is low and fatigue is high?",
        },
        "browse_only_new_user_no_comms": {
            "expected_state": "exploration_or_balanced",
            "expected_action_family": "send_content_or_light_recommendation",
            "quality_question": "Does Pulse avoid treating browsing as late-funnel intent?",
        },
        "dormant_high_value_returning_customer": {
            "expected_state": "high_retention_risk",
            "expected_action_family": "send_retention_message",
            "quality_question": "Does Pulse prioritize reactivation over generic product recommendation?",
        },
        "recent_purchase_loyal_promoter": {
            "expected_state": "loyal_or_balanced",
            "expected_action_family": "send_content_or_product_recommendation",
            "quality_question": "Does Pulse avoid over-messaging immediately after purchase?",
        },
        "discount_sensitive_coupon_seeker": {
            "expected_state": "high_intent_price_sensitive",
            "expected_action_family": "send_discount_offer",
            "quality_question": "Does Pulse use discounting only when price sensitivity is explicit?",
        },
        "refund_complaint_retention_risk": {
            "expected_state": "low_trust_high_fatigue_or_high_retention_risk",
            "expected_action_family": "service_recovery_or_suppress",
            "quality_question": "Does Pulse suppress promotional messaging after a complaint?",
        },
        "wishlist_consideration_mid_funnel": {
            "expected_state": "mid_funnel_consideration",
            "expected_action_family": "send_content_or_product_recommendation",
            "quality_question": "Does Pulse identify consideration without forcing checkout pressure?",
        },
        "over_messaged_low_value_unresponsive": {
            "expected_state": "fatigued_or_low_receptivity",
            "expected_action_family": "suppress",
            "quality_question": "Does Pulse stop low-value communications when fatigue is explicit?",
        },
        "checkout_payment_failure_urgent": {
            "expected_state": "high_intent_service_blocked",
            "expected_action_family": "service_recovery_or_cart_reminder",
            "quality_question": "Does Pulse resolve the payment issue before pushing offers?",
        },
        "category_explorer_email_engaged": {
            "expected_state": "exploration_receptive",
            "expected_action_family": "send_content",
            "quality_question": "Does Pulse recommend content for an engaged explorer?",
        },
        "high_value_low_trust_recent_claim": {
            "expected_state": "low_trust_high_value",
            "expected_action_family": "service_recovery_or_suppress",
            "quality_question": "Does Pulse protect a high-value customer from mistimed promos?",
        },
    },
    "historical_outcomes": [
        {
            "state_vector": {
                "purchase_readiness": 0.88,
                "communication_fatigue": 0.25,
                "trust_level": 0.82,
                "retention_risk": 0.20,
                "engagement_probability": 0.72,
            },
            "action": "send_cart_reminder",
            "converted": True,
            "revenue": 185,
            "engagement": 0.64,
            "retention": 0.45,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.86,
                "communication_fatigue": 0.22,
                "trust_level": 0.84,
                "retention_risk": 0.18,
                "engagement_probability": 0.76,
            },
            "action": "send_product_recommendation",
            "converted": True,
            "revenue": 155,
            "engagement": 0.70,
            "retention": 0.48,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.72,
                "communication_fatigue": 0.82,
                "trust_level": 0.32,
                "retention_risk": 0.74,
                "engagement_probability": 0.44,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 135,
            "engagement": 0.20,
            "retention": 0.88,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.68,
                "communication_fatigue": 0.86,
                "trust_level": 0.28,
                "retention_risk": 0.82,
                "engagement_probability": 0.38,
            },
            "action": "send_retention_message",
            "converted": False,
            "revenue": 96,
            "engagement": 0.42,
            "retention": 0.91,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.40,
                "communication_fatigue": 0.22,
                "trust_level": 0.76,
                "retention_risk": 0.18,
                "engagement_probability": 0.66,
            },
            "action": "send_content",
            "converted": True,
            "revenue": 72,
            "engagement": 0.91,
            "retention": 0.55,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.35,
                "communication_fatigue": 0.18,
                "trust_level": 0.80,
                "retention_risk": 0.16,
                "engagement_probability": 0.70,
            },
            "action": "send_content",
            "converted": True,
            "revenue": 64,
            "engagement": 0.88,
            "retention": 0.58,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.76,
                "communication_fatigue": 0.35,
                "trust_level": 0.72,
                "retention_risk": 0.28,
                "engagement_probability": 0.62,
            },
            "action": "send_discount_offer",
            "converted": True,
            "revenue": 128,
            "engagement": 0.74,
            "retention": 0.52,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.78,
                "communication_fatigue": 0.30,
                "trust_level": 0.70,
                "retention_risk": 0.26,
                "engagement_probability": 0.60,
            },
            "action": "send_cart_reminder",
            "converted": True,
            "revenue": 118,
            "engagement": 0.62,
            "retention": 0.45,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.25,
                "communication_fatigue": 0.72,
                "trust_level": 0.34,
                "retention_risk": 0.88,
                "engagement_probability": 0.28,
            },
            "action": "send_retention_message",
            "converted": False,
            "revenue": 142,
            "engagement": 0.48,
            "retention": 0.94,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.20,
                "communication_fatigue": 0.78,
                "trust_level": 0.30,
                "retention_risk": 0.86,
                "engagement_probability": 0.24,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 128,
            "engagement": 0.18,
            "retention": 0.90,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.62,
                "communication_fatigue": 0.18,
                "trust_level": 0.90,
                "retention_risk": 0.12,
                "engagement_probability": 0.82,
            },
            "action": "send_product_recommendation",
            "converted": True,
            "revenue": 205,
            "engagement": 0.82,
            "retention": 0.62,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.58,
                "communication_fatigue": 0.16,
                "trust_level": 0.92,
                "retention_risk": 0.10,
                "engagement_probability": 0.86,
            },
            "action": "send_content",
            "converted": True,
            "revenue": 110,
            "engagement": 0.94,
            "retention": 0.70,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.82,
                "communication_fatigue": 0.58,
                "trust_level": 0.55,
                "retention_risk": 0.44,
                "engagement_probability": 0.52,
            },
            "action": "send_discount_offer",
            "converted": True,
            "revenue": 168,
            "engagement": 0.66,
            "retention": 0.50,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.80,
                "communication_fatigue": 0.62,
                "trust_level": 0.46,
                "retention_risk": 0.50,
                "engagement_probability": 0.48,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 150,
            "engagement": 0.24,
            "retention": 0.82,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.70,
                "communication_fatigue": 0.42,
                "trust_level": 0.66,
                "retention_risk": 0.36,
                "engagement_probability": 0.56,
            },
            "action": "send_product_recommendation",
            "converted": True,
            "revenue": 150,
            "engagement": 0.60,
            "retention": 0.48,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.45,
                "communication_fatigue": 0.68,
                "trust_level": 0.38,
                "retention_risk": 0.72,
                "engagement_probability": 0.34,
            },
            "action": "send_retention_message",
            "converted": False,
            "revenue": 118,
            "engagement": 0.44,
            "retention": 0.88,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.30,
                "communication_fatigue": 0.88,
                "trust_level": 0.22,
                "retention_risk": 0.92,
                "engagement_probability": 0.34
            },
            "action": "service_recovery",
            "converted": False,
            "revenue": 165,
            "engagement": 0.58,
            "retention": 0.96
        },
        {
            "state_vector": {
                "purchase_readiness": 0.62,
                "communication_fatigue": 0.84,
                "trust_level": 0.30,
                "retention_risk": 0.78,
                "engagement_probability": 0.45
            },
            "action": "service_recovery",
            "converted": False,
            "revenue": 150,
            "engagement": 0.60,
            "retention": 0.94
        },
        {
            "state_vector": {
                "purchase_readiness": 0.50,
                "communication_fatigue": 0.70,
                "trust_level": 0.36,
                "retention_risk": 0.68,
                "engagement_probability": 0.42
            },
            "action": "service_recovery",
            "converted": False,
            "revenue": 132,
            "engagement": 0.55,
            "retention": 0.90
        },
        {
            "state_vector": {
                "purchase_readiness": 0.48,
                "communication_fatigue": 0.74,
                "trust_level": 0.35,
                "retention_risk": 0.70,
                "engagement_probability": 0.32,
            },
            "action": "suppress",
            "converted": False,
            "revenue": 132,
            "engagement": 0.18,
            "retention": 0.86,
        },
        {
            "state_vector": {
                "purchase_readiness": 0.64,
                "communication_fatigue": 0.28,
                "trust_level": 0.78,
                "retention_risk": 0.24,
                "engagement_probability": 0.64,
            },
            "action": "send_cart_reminder",
            "converted": True,
            "revenue": 122,
            "engagement": 0.62,
            "retention": 0.50,
        },
    ],
    "users": [
        {
            "user_id": "ECOM-001",
            "scenario": "high_intent_cart_abandon_high_trust",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product Clicked",
                    "Product Viewed",
                    "Product Added",
                    "Cart Viewed",
                    "Checkout Started",
                    "Checkout Step Viewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "email",
                    "message": "I liked the recommendations. Please send me similar styles.",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "repeat_buyer",
                "total_orders": 14,
                "average_order_value": 165,
                "last_purchase_days_ago": 18,
                "preferred_channel": "email",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 11,
                "messages_7d": 2,
            },
        },
        {
            "user_id": "ECOM-002",
            "scenario": "high_intent_high_fatigue_low_trust",
            "events": {
                "raw_events": [
                    "Product Viewed",
                    "Product Viewed",
                    "Product Added",
                    "Cart Viewed",
                    "Checkout Started",
                    "Product Removed",
                    "Product Added",
                ]
            },
            "comms_history": [
                {
                    "channel": "whatsapp",
                    "message": "Please stop sending so many reminders. This is frustrating.",
                },
                {
                    "channel": "support_ticket",
                    "message": "My last order issue is still unresolved.",
                },
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "cart_abandoner",
                "total_orders": 9,
                "average_order_value": 210,
                "last_purchase_days_ago": 26,
                "preferred_channel": "push",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 1,
                "events_7d": 9,
                "messages_7d": 8,
                "recent_complaint": True,
            },
        },
        {
            "user_id": "ECOM-003",
            "scenario": "browse_only_new_user_no_comms",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product List Filtered",
                    "Product Viewed",
                    "Products Searched",
                    "Product Viewed",
                ]
            },
            "comms_history": [],
            "crm_context": {
                "customer_tier": "new",
                "ltv_segment": "unknown",
                "lifecycle_stage": "new_user",
                "total_orders": 0,
                "average_order_value": 0,
                "last_purchase_days_ago": None,
                "preferred_channel": "push",
                "timezone": "America/New_York",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 5,
                "messages_7d": 1,
            },
        },
        {
            "user_id": "ECOM-004",
            "scenario": "dormant_high_value_returning_customer",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product Viewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "email",
                    "message": "I have not shopped recently, but I still like the brand.",
                }
            ],
            "crm_context": {
                "customer_tier": "platinum",
                "ltv_segment": "high_value",
                "lifecycle_stage": "dormant",
                "total_orders": 31,
                "average_order_value": 245,
                "last_purchase_days_ago": 118,
                "preferred_channel": "email",
                "timezone": "Europe/London",
            },
            "user_state": {
                "inactive_days": 21,
                "events_7d": 1,
                "messages_7d": 0,
            },
        },
        {
            "user_id": "ECOM-005",
            "scenario": "recent_purchase_loyal_promoter",
            "events": {
                "raw_events": [
                    "Product Viewed",
                    "Product Added",
                    "Checkout Started",
                    "Payment Info Entered",
                    "Order Completed",
                    "Product Reviewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "chat",
                    "message": "Great delivery experience. I will buy again.",
                }
            ],
            "crm_context": {
                "customer_tier": "platinum",
                "ltv_segment": "high_value",
                "lifecycle_stage": "loyal",
                "total_orders": 42,
                "average_order_value": 190,
                "last_purchase_days_ago": 2,
                "preferred_channel": "in_app",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 13,
                "messages_7d": 2,
            },
        },
        {
            "user_id": "ECOM-006",
            "scenario": "discount_sensitive_coupon_seeker",
            "events": {
                "raw_events": [
                    "Products Searched",
                    "Product Viewed",
                    "Coupon Entered",
                    "Coupon Applied",
                    "Product Added",
                    "Cart Viewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "email",
                    "message": "Do you have a better discount before I place the order?",
                }
            ],
            "crm_context": {
                "customer_tier": "silver",
                "ltv_segment": "price_sensitive",
                "lifecycle_stage": "deal_seeker",
                "total_orders": 6,
                "average_order_value": 58,
                "last_purchase_days_ago": 34,
                "preferred_channel": "email",
                "timezone": "America/Los_Angeles",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 8,
                "messages_7d": 3,
            },
        },
        {
            "user_id": "ECOM-007",
            "scenario": "refund_complaint_retention_risk",
            "events": {
                "raw_events": [
                    "Order Refunded",
                    "Product Viewed",
                    "Product Removed",
                    "Order Cancelled",
                ]
            },
            "comms_history": [
                {
                    "channel": "support_ticket",
                    "message": "This refund experience is unacceptable. I am thinking of leaving.",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "service_recovery",
                "total_orders": 17,
                "average_order_value": 135,
                "last_purchase_days_ago": 9,
                "preferred_channel": "phone",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 4,
                "events_7d": 3,
                "messages_7d": 6,
                "recent_complaint": True,
            },
        },
        {
            "user_id": "ECOM-008",
            "scenario": "wishlist_consideration_mid_funnel",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product Viewed",
                    "Product Added to Wishlist",
                    "Product Viewed",
                    "Product Added to Wishlist",
                ]
            },
            "comms_history": [
                {
                    "channel": "push",
                    "message": "I am comparing products and may buy later.",
                }
            ],
            "crm_context": {
                "customer_tier": "silver",
                "ltv_segment": "mid_value",
                "lifecycle_stage": "consideration",
                "total_orders": 3,
                "average_order_value": 92,
                "last_purchase_days_ago": 45,
                "preferred_channel": "push",
                "timezone": "Asia/Singapore",
            },
            "user_state": {
                "inactive_days": 1,
                "events_7d": 6,
                "messages_7d": 2,
            },
        },
        {
            "user_id": "ECOM-009",
            "scenario": "over_messaged_low_value_unresponsive",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product Viewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "sms",
                    "message": "Too many messages. I do not want these offers.",
                }
            ],
            "crm_context": {
                "customer_tier": "bronze",
                "ltv_segment": "low_value",
                "lifecycle_stage": "fatigued",
                "total_orders": 1,
                "average_order_value": 24,
                "last_purchase_days_ago": 96,
                "preferred_channel": "none",
                "timezone": "America/New_York",
            },
            "user_state": {
                "inactive_days": 10,
                "events_7d": 1,
                "messages_7d": 12,
            },
        },
        {
            "user_id": "ECOM-010",
            "scenario": "checkout_payment_failure_urgent",
            "events": {
                "raw_events": [
                    "Product Viewed",
                    "Product Added",
                    "Cart Viewed",
                    "Checkout Started",
                    "Payment Info Entered",
                    "Checkout Step Viewed",
                ]
            },
            "comms_history": [
                {
                    "channel": "chat",
                    "message": "My payment failed twice. Please fix this urgently.",
                }
            ],
            "crm_context": {
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "lifecycle_stage": "checkout_blocked",
                "total_orders": 12,
                "average_order_value": 142,
                "last_purchase_days_ago": 22,
                "preferred_channel": "chat",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 10,
                "messages_7d": 4,
            },
        },
        {
            "user_id": "ECOM-011",
            "scenario": "category_explorer_email_engaged",
            "events": {
                "raw_events": [
                    "Product List Viewed",
                    "Product List Filtered",
                    "Product Clicked",
                    "Product Viewed",
                    "Products Searched",
                ]
            },
            "comms_history": [
                {
                    "channel": "email",
                    "message": "I open your emails for new launches and lookbooks.",
                }
            ],
            "crm_context": {
                "customer_tier": "silver",
                "ltv_segment": "mid_value",
                "lifecycle_stage": "category_explorer",
                "total_orders": 5,
                "average_order_value": 88,
                "last_purchase_days_ago": 19,
                "preferred_channel": "email",
                "timezone": "Europe/Berlin",
            },
            "user_state": {
                "inactive_days": 0,
                "events_7d": 7,
                "messages_7d": 2,
            },
        },
        {
            "user_id": "ECOM-012",
            "scenario": "high_value_low_trust_recent_claim",
            "events": {
                "raw_events": [
                    "Product Viewed",
                    "Product Added",
                    "Cart Viewed",
                    "Product Removed",
                ]
            },
            "comms_history": [
                {
                    "channel": "support_ticket",
                    "message": "I do not trust this anymore after my last damaged delivery.",
                }
            ],
            "crm_context": {
                "customer_tier": "platinum",
                "ltv_segment": "high_value",
                "lifecycle_stage": "trust_recovery",
                "total_orders": 36,
                "average_order_value": 260,
                "last_purchase_days_ago": 6,
                "preferred_channel": "email",
                "timezone": "Asia/Kolkata",
            },
            "user_state": {
                "inactive_days": 2,
                "events_7d": 5,
                "messages_7d": 5,
                "recent_complaint": True,
            },
        },
    ],
}
