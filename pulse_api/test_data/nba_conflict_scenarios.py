from .ecommerce_comprehensive import _crm, _user
from .ecommerce_synthetic import ECOMMERCE_SYNTHETIC_TEST_PAYLOAD


NBA_CONFLICT_SCENARIO_PAYLOAD = {
    "workspace_id": "nba_conflict_eval",
    "source_name": "synthetic_nba_conflict_scenarios",
    "business_goal": "increase_revenue",
    "constraints": {
        "discounts_allowed": True,
        "send_allowed": True,
        "suppress_if_high_fatigue": False,
        "quiet_hours": {"start": "21:00", "end": "09:00"},
    },
    "historical_outcomes": ECOMMERCE_SYNTHETIC_TEST_PAYLOAD["historical_outcomes"],
    "users": [
        _user(
            "NBA-CONFLICT-001",
            "high_intent_low_fatigue_should_send",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Payment Info Entered", "Checkout Step Viewed", "Cart Viewed",
                "Product Viewed", "Product Added", "Cart Viewed", "app_close",
            ],
            [
                {"channel": "chat", "message": "I will complete the order later today.", "sentiment_hint": "positive"}
            ],
            _crm("gold", "high_value", "cart_abandoner", 12, 155, 18, "push", "Asia/Kolkata", nps=55),
            {"inactive_days": 0, "events_7d": 11, "messages_7d": 1},
            {"expected": "send/cart reminder or recommendation; no suppression"},
            0,
        ),
        _user(
            "NBA-CONFLICT-002",
            "high_intent_high_fatigue_should_not_promo",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Product Removed", "Product Added", "Cart Viewed", "push_sent",
                "push_ignored", "whatsapp_sent", "whatsapp_ignored", "Product Removed",
            ],
            [
                {"channel": "whatsapp", "message": "I want to buy but these reminders are too much.", "sentiment_hint": "negative"},
                {"channel": "support_ticket", "message": "My last issue is still unresolved.", "sentiment_hint": "negative"},
            ],
            _crm("gold", "high_value", "cart_abandoner", 10, 180, 12, "email", "Asia/Kolkata", "open_ticket", True, -35),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 10, "recent_complaint": True, "support_ticket_open_days": 4},
            {"expected": "service recovery or suppress despite high intent"},
            24,
        ),
        _user(
            "NBA-CONFLICT-003",
            "nba_channel_whatsapp_user_prefers_push",
            [
                "app_open", "Product List Viewed", "Product Viewed", "email_opened",
                "Product Viewed", "Product Added to Wishlist", "Product Viewed",
                "app_close", "email_opened", "Product Viewed",
            ],
            [
                {"channel": "email", "message": "Please use push notifications. I do not check WhatsApp for offers.", "sentiment_hint": "neutral"}
            ],
            _crm("silver", "mid_value", "dormant", 4, 75, 96, "push", "Asia/Kolkata", nps=20),
            {"inactive_days": 28, "events_7d": 1, "messages_7d": 1},
            {"expected": "retention action channel should resolve to push"},
            48,
            "mobile_app",
            "android",
        ),
        _user(
            "NBA-CONFLICT-004",
            "recommended_time_inside_quiet_hours",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Payment Info Entered", "Checkout Step Viewed", "Cart Viewed",
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "app_close",
            ],
            [
                {"channel": "chat", "message": "I need this urgently but message me tomorrow if it is late.", "sentiment_hint": "urgent"}
            ],
            _crm("gold", "high_value", "urgent_buyer", 8, 130, 15, "push", "Asia/Kolkata", nps=40),
            {"inactive_days": 0, "events_7d": 9, "messages_7d": 1},
            {"expected": "candidate 22:00 should move to quiet-hour end"},
            72,
        ),
        _user(
            "NBA-CONFLICT-005",
            "support_ticket_open_14_days_do_not_disturb",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Product Viewed", "Product Added", "Cart Viewed", "Product Viewed",
                "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "The support ticket has been open for weeks. Do not send me promos.", "sentiment_hint": "negative"}
            ],
            _crm("platinum", "high_value", "support_open", 22, 240, 9, "whatsapp", "Asia/Kolkata", "open_ticket", True, -55),
            {"inactive_days": 0, "events_7d": 8, "messages_7d": 4, "recent_complaint": True, "support_ticket_open_days": 16},
            {"expected": "hard suppress because support ticket open for 14+ days"},
            96,
        ),
    ],
}

NBA_CONFLICT_SCENARIO_PAYLOAD["users"][-1]["constraints"] = {
    "custom_rules": [
        {
            "id": "support_ticket_open_14_days_do_not_disturb",
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
