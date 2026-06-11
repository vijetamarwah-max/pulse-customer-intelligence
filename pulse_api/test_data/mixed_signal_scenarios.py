from .ecommerce_comprehensive import _crm, _user
from .ecommerce_synthetic import ECOMMERCE_SYNTHETIC_TEST_PAYLOAD


MIXED_SIGNAL_SCENARIO_PAYLOAD = {
    "workspace_id": "mixed_signal_eval",
    "source_name": "synthetic_mixed_signal_scenarios",
    "business_goal": "increase_revenue",
    "constraints": {
        "discounts_allowed": True,
        "send_allowed": True,
        "quiet_hours": {"start": "21:00", "end": "09:00"},
    },
    "historical_outcomes": ECOMMERCE_SYNTHETIC_TEST_PAYLOAD["historical_outcomes"],
    "users": [
        _user(
            "MIX-001",
            "explores_but_ignores_all_comms_14d",
            [
                "Product List Viewed", "Product List Filtered", "Product Viewed",
                "Products Searched", "Product Viewed", "Product Clicked",
                "Product Viewed", "Product List Viewed", "Product Viewed",
                "Products Searched", "Product Viewed", "app_close",
            ],
            [
                {"channel": "push", "direction": "outbound", "message": "Ignored browsing nudge.", "opened": False, "clicked": False},
                {"channel": "email", "direction": "outbound", "message": "Ignored category digest.", "opened": False, "clicked": False},
            ],
            _crm("silver", "mid_value", "explorer_unresponsive", 3, 74, 44, "email", "Asia/Kolkata", nps=20),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 6, "ignored_comms_days": 14},
            {"expected": "observe or content, no aggressive promo; confidence should be moderate"},
            0,
        ),
        _user(
            "MIX-002",
            "high_cart_intent_but_recent_negative_support",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Payment Info Entered", "Product Viewed", "Product Added",
                "Cart Viewed", "Checkout Step Viewed", "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "My last delivery issue is unresolved. I do not trust this yet.", "sentiment_hint": "negative"}
            ],
            _crm("gold", "high_value", "cart_abandoner", 12, 180, 18, "email", "Asia/Kolkata", "open_ticket", True, -45),
            {"inactive_days": 0, "events_7d": 10, "messages_7d": 4, "recent_complaint": True, "support_ticket_open_days": 5},
            {"expected": "service recovery beats cart reminder despite high purchase intent"},
            18,
        ),
        _user(
            "MIX-003",
            "recent_purchase_browsing_again_but_fatigued",
            [
                "Order Completed", "Product Reviewed", "app_open", "Product Viewed",
                "Product List Viewed", "Product Viewed", "push_sent", "push_ignored",
                "email_sent", "email_ignored", "Product Viewed", "app_close",
            ],
            [
                {"channel": "whatsapp", "message": "I just bought something. Please do not keep nudging me.", "sentiment_hint": "negative"}
            ],
            _crm("gold", "high_value", "recent_buyer", 18, 125, 1, "email", "Asia/Kolkata", nps=30),
            {"inactive_days": 0, "events_7d": 11, "messages_7d": 8},
            {"expected": "suppress or low-pressure content; not hard sell"},
            36,
        ),
        _user(
            "MIX-004",
            "dormant_high_value_positive_comms",
            [
                "email_opened", "Product List Viewed", "Product Viewed",
                "Product Added to Wishlist", "Product Viewed", "app_close",
                "email_opened", "Product Viewed", "app_close",
            ],
            [
                {"channel": "email", "message": "I still like the brand, I just have not needed anything recently.", "sentiment_hint": "positive"}
            ],
            _crm("platinum", "high_value", "dormant", 30, 230, 130, "email", "Europe/London", nps=45),
            {"inactive_days": 35, "events_7d": 1, "messages_7d": 1},
            {"expected": "inactivity-led retention, winback/content, not service recovery"},
            54,
        ),
        _user(
            "MIX-005",
            "discount_seeker_but_premium_tier_no_discount_policy",
            [
                "Products Searched", "Product Viewed", "Coupon Entered",
                "Product Added", "Cart Viewed", "Checkout Started",
                "Coupon Entered", "Product Removed", "Product Viewed",
            ],
            [
                {"channel": "chat", "message": "Can you give me a discount?", "sentiment_hint": "neutral"}
            ],
            _crm("platinum", "high_value", "premium_consideration", 22, 320, 20, "email", "Asia/Dubai", nps=50),
            {"inactive_days": 0, "events_7d": 9, "messages_7d": 2},
            {"expected": "discount suppressed by policy; recommendation/content alternative"},
            72,
        ),
        _user(
            "MIX-006",
            "urgent_checkout_need_but_quiet_hours",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Payment Info Entered", "Checkout Step Viewed", "Cart Viewed",
                "Checkout Started", "app_close",
            ],
            [
                {"channel": "chat", "message": "I need this today, but do not message late night.", "sentiment_hint": "urgent"}
            ],
            _crm("gold", "high_value", "urgent_buyer", 9, 140, 12, "push", "Asia/Kolkata", nps=35),
            {"inactive_days": 0, "events_7d": 9, "messages_7d": 1},
            {"expected": "send but move time out of quiet hours"},
            90,
        ),
        _user(
            "MIX-007",
            "loyal_opens_email_but_push_unresponsive",
            [
                "push_sent", "push_ignored", "push_sent", "push_ignored",
                "email_opened", "email_clicked", "Product Viewed", "Product Added",
                "Cart Viewed", "email_opened", "Product Viewed",
            ],
            [
                {"channel": "email", "message": "Email is fine. Push notifications are annoying.", "sentiment_hint": "neutral"}
            ],
            _crm("gold", "high_value", "channel_preference_email", 19, 115, 16, "email", "Asia/Kolkata", nps=40),
            {"inactive_days": 0, "events_7d": 10, "messages_7d": 4},
            {"expected": "email preferred over push if sending"},
            108,
        ),
        _user(
            "MIX-008",
            "low_value_high_complaint_but_browsing",
            [
                "Product List Viewed", "Product Viewed", "Product Viewed",
                "Product Removed", "support_complaint", "Product Viewed",
                "app_close", "email_sent", "email_ignored", "Product Viewed",
            ],
            [
                {"channel": "support_ticket", "message": "This is frustrating and nobody helped me.", "sentiment_hint": "negative"}
            ],
            _crm("bronze", "low_value", "complaint", 1, 30, 80, "none", "America/New_York", "open_ticket", False, -55),
            {"inactive_days": 3, "events_7d": 5, "messages_7d": 5, "recent_complaint": True},
            {"expected": "suppress or service recovery; no promo"},
            126,
        ),
    ],
}

MIXED_SIGNAL_SCENARIO_PAYLOAD["users"][4]["constraints"] = {
    "custom_rules": [
        {
            "id": "no_discount_for_platinum",
            "when": {"field": "support_status", "op": "!=", "value": "irrelevant"},
            "actions": [
                {"type": "suppress_action", "value": "send_discount_offer"},
                {"type": "add_reason", "value": "custom_rule_no_discount_for_platinum"}
            ],
        }
    ]
}
