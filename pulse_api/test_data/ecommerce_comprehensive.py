from datetime import datetime, timedelta

from .ecommerce_synthetic import ECOMMERCE_SYNTHETIC_TEST_PAYLOAD


BASE_TIME = datetime(2026, 6, 1, 9, 0, 0)


def _event_stream(raw_events, start_offset_hours, channel="web", device="ios"):
    return [
        {
            "event": event,
            "timestamp": (
                BASE_TIME + timedelta(hours=start_offset_hours, minutes=index * 11)
            ).isoformat() + "Z",
            "properties": {
                "channel": channel,
                "device": device,
                "session_index": start_offset_hours // 12 + 1,
                "sequence_position": index + 1,
            },
        }
        for index, event in enumerate(raw_events)
    ]


def _comms(records, start_offset_hours):
    enriched = []
    for index, record in enumerate(records):
        enriched.append(
            {
                "channel": record["channel"],
                "direction": record.get("direction", "inbound"),
                "timestamp": (
                    BASE_TIME + timedelta(hours=start_offset_hours, minutes=index * 37)
                ).isoformat() + "Z",
                "message": record["message"],
                "sentiment_hint": record.get("sentiment_hint", "neutral"),
                "metadata": {
                    "source": record.get("source", "synthetic"),
                    "thread_id": record.get("thread_id", f"thread-{start_offset_hours}-{index}"),
                    "campaign_id": record.get("campaign_id"),
                    "opened": record.get("opened"),
                    "clicked": record.get("clicked"),
                    "response_time_minutes": record.get("response_time_minutes"),
                },
            }
        )

    return enriched


def _user(
    user_id,
    scenario,
    raw_events,
    comms_history,
    crm_context,
    user_state,
    expectation,
    start_offset_hours,
    channel="web",
    device="ios",
):
    return {
        "user_id": user_id,
        "scenario": scenario,
        "events": {
            "raw_events": raw_events,
            "event_stream": _event_stream(raw_events, start_offset_hours, channel, device),
        },
        "comms_history": _comms(comms_history, start_offset_hours + 3),
        "crm_context": crm_context,
        "user_state": user_state,
        "expected_review": expectation,
    }


def _crm(
    tier,
    ltv,
    lifecycle,
    total_orders,
    aov,
    last_purchase_days_ago,
    preferred_channel,
    timezone,
    support_status="none",
    loyalty_member=True,
    nps=None,
):
    return {
        "customer_tier": tier,
        "ltv_segment": ltv,
        "lifecycle_stage": lifecycle,
        "total_orders": total_orders,
        "average_order_value": aov,
        "last_purchase_days_ago": last_purchase_days_ago,
        "preferred_channel": preferred_channel,
        "timezone": timezone,
        "support_status": support_status,
        "loyalty_member": loyalty_member,
        "nps": nps,
    }


COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD = {
    "workspace_id": "ecommerce_comprehensive_eval",
    "source_name": "comprehensive_synthetic_segment_ecommerce_stream",
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
            "ECOM-C001",
            "new_user_onboarding_product_explorer",
            [
                "Product List Viewed", "Product List Filtered", "Product Clicked",
                "Product Viewed", "Products Searched", "Product Viewed",
                "Product Added to Wishlist", "Product List Viewed", "Product Viewed",
                "Product Clicked", "Product Viewed", "app_open", "Product List Viewed",
                "Products Searched", "Product Viewed",
            ],
            [
                {"channel": "push", "direction": "outbound", "message": "Welcome offer viewed but not clicked.", "opened": True, "clicked": False},
                {"channel": "chat", "message": "I am just browsing and comparing sizes.", "sentiment_hint": "neutral"},
            ],
            _crm("new", "unknown", "new_user", 0, 0, None, "push", "Asia/Kolkata", loyalty_member=False),
            {"inactive_days": 0, "events_7d": 15, "messages_7d": 1},
            {"expected_state": "exploration", "expected_action_family": "light_content_or_recommendation"},
            0,
        ),
        _user(
            "ECOM-C002",
            "new_user_onboarding_over_messaged",
            [
                "app_open", "Product List Viewed", "Product Viewed", "push_sent",
                "push_ignored", "email_sent", "email_ignored", "whatsapp_sent",
                "Product Viewed", "push_sent", "push_ignored", "Product Removed",
                "app_close", "email_sent", "email_ignored", "sms_sent",
            ],
            [
                {"channel": "whatsapp", "message": "Too many messages already. Please stop.", "sentiment_hint": "negative"},
                {"channel": "sms", "direction": "outbound", "message": "Flash sale reminder ignored.", "opened": False, "clicked": False},
            ],
            _crm("new", "unknown", "new_user", 0, 0, None, "push", "Asia/Kolkata", loyalty_member=False, nps=-20),
            {"inactive_days": 2, "events_7d": 6, "messages_7d": 8},
            {"expected_state": "fatigued_new_user", "expected_action_family": "suppress"},
            8,
        ),
        _user(
            "ECOM-C003",
            "cart_abandoner_high_intent_low_fatigue",
            [
                "Product List Viewed", "Product Clicked", "Product Viewed",
                "Product Added", "Cart Viewed", "Checkout Started",
                "Checkout Step Viewed", "Checkout Step Completed", "Payment Info Entered",
                "Checkout Step Viewed", "Cart Viewed", "Product Viewed",
                "Product Added", "Cart Viewed", "app_close",
            ],
            [
                {"channel": "email", "direction": "outbound", "message": "Cart reminder opened.", "opened": True, "clicked": True},
                {"channel": "chat", "message": "I will finish checkout tonight.", "sentiment_hint": "positive"},
            ],
            _crm("gold", "high_value", "cart_abandoner", 8, 150, 21, "email", "America/New_York", nps=45),
            {"inactive_days": 0, "events_7d": 14, "messages_7d": 2},
            {"expected_state": "high_intent_receptive", "expected_action_family": "cart_reminder"},
            18,
            "web",
            "desktop",
        ),
        _user(
            "ECOM-C004",
            "cart_abandoner_high_fatigue_support_open",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Product Removed", "Product Added", "Cart Viewed", "push_sent",
                "push_ignored", "whatsapp_sent", "whatsapp_ignored", "Checkout Step Viewed",
                "Product Removed", "support_complaint", "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "My previous return is still unresolved and reminders are frustrating.", "sentiment_hint": "negative"},
                {"channel": "whatsapp", "direction": "outbound", "message": "Cart discount reminder ignored.", "opened": True, "clicked": False},
            ],
            _crm("gold", "high_value", "cart_abandoner", 11, 190, 14, "email", "Asia/Kolkata", "open_ticket", True, -45),
            {"inactive_days": 1, "events_7d": 10, "messages_7d": 9, "recent_complaint": True},
            {"expected_state": "high_intent_high_fatigue_low_trust", "expected_action_family": "suppress_or_service_recovery"},
            28,
        ),
        _user(
            "ECOM-C005",
            "discount_sensitive_coupon_loop",
            [
                "Products Searched", "Product Viewed", "Coupon Entered", "Coupon Applied",
                "Product Added", "Cart Viewed", "Coupon Entered", "Product Removed",
                "Product Viewed", "Coupon Applied", "Product Added", "Cart Viewed",
                "Checkout Started", "app_close", "Products Searched",
            ],
            [
                {"channel": "email", "message": "Do you have a better coupon before I buy?", "sentiment_hint": "neutral"},
                {"channel": "email", "direction": "outbound", "message": "10 percent coupon clicked.", "opened": True, "clicked": True},
            ],
            _crm("silver", "price_sensitive", "deal_seeker", 5, 52, 33, "email", "America/Los_Angeles", nps=20),
            {"inactive_days": 0, "events_7d": 13, "messages_7d": 3},
            {"expected_state": "high_intent_price_sensitive", "expected_action_family": "discount_offer"},
            39,
            "web",
            "android",
        ),
        _user(
            "ECOM-C006",
            "loyal_recent_purchase_do_not_discount",
            [
                "Product Viewed", "Product Added", "Checkout Started", "Payment Info Entered",
                "Order Completed", "Product Reviewed", "app_open", "Product List Viewed",
                "Product Viewed", "Product Added to Wishlist", "email_opened", "Product Viewed",
                "app_open", "Product List Viewed", "Product Reviewed",
            ],
            [
                {"channel": "chat", "message": "Great delivery experience. Keep me posted on premium launches.", "sentiment_hint": "positive"},
                {"channel": "email", "direction": "outbound", "message": "New collection email clicked.", "opened": True, "clicked": True},
            ],
            _crm("platinum", "high_value", "loyal", 46, 210, 2, "email", "Asia/Kolkata", nps=70),
            {"inactive_days": 0, "events_7d": 16, "messages_7d": 2},
            {"expected_state": "loyal_receptive", "expected_action_family": "content_or_recommendation_no_discount"},
            50,
        ),
        _user(
            "ECOM-C007",
            "refund_complaint_high_value_retention_risk",
            [
                "Order Refunded", "support_complaint", "Product Viewed", "Product Removed",
                "Order Cancelled", "app_open", "Product List Viewed", "app_close",
                "email_sent", "email_ignored", "support_complaint", "Product Viewed",
                "Product Removed", "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "This refund experience is unacceptable. I am thinking of leaving.", "sentiment_hint": "negative"},
                {"channel": "email", "direction": "outbound", "message": "Promo email ignored after complaint.", "opened": False, "clicked": False},
            ],
            _crm("platinum", "high_value", "service_recovery", 29, 260, 6, "phone", "Asia/Kolkata", "open_ticket", True, -60),
            {"inactive_days": 3, "events_7d": 5, "messages_7d": 7, "recent_complaint": True},
            {"expected_state": "high_retention_risk_low_trust", "expected_action_family": "service_recovery_or_suppress"},
            62,
        ),
        _user(
            "ECOM-C008",
            "dormant_high_value_soft_return",
            [
                "app_open", "Product List Viewed", "Product Viewed", "Products Searched",
                "Product Viewed", "Product Added to Wishlist", "app_close", "email_opened",
                "Product List Viewed", "Product Viewed", "app_close", "Product Viewed",
            ],
            [
                {"channel": "email", "message": "I have not shopped recently but still like the brand.", "sentiment_hint": "positive"},
                {"channel": "email", "direction": "outbound", "message": "Winback email opened.", "opened": True, "clicked": False},
            ],
            _crm("platinum", "high_value", "dormant", 33, 240, 126, "email", "Europe/London", nps=35),
            {"inactive_days": 24, "events_7d": 2, "messages_7d": 1},
            {"expected_state": "dormant_high_value", "expected_action_family": "retention_message_or_content"},
            74,
            "web",
            "desktop",
        ),
        _user(
            "ECOM-C009",
            "dormant_low_value_unresponsive",
            [
                "email_sent", "email_ignored", "push_sent", "push_ignored",
                "Product List Viewed", "app_close", "sms_sent", "sms_ignored",
                "email_sent", "email_ignored", "push_sent", "push_ignored",
            ],
            [
                {"channel": "sms", "message": "I am not interested in these offers.", "sentiment_hint": "negative"},
                {"channel": "push", "direction": "outbound", "message": "Clearance sale ignored.", "opened": False, "clicked": False},
            ],
            _crm("bronze", "low_value", "dormant", 1, 24, 180, "none", "America/New_York", loyalty_member=False, nps=-10),
            {"inactive_days": 42, "events_7d": 0, "messages_7d": 10},
            {"expected_state": "low_value_fatigued_dormant", "expected_action_family": "suppress"},
            86,
        ),
        _user(
            "ECOM-C010",
            "payment_failure_urgent_high_intent",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "Checkout Started",
                "Payment Info Entered", "Checkout Step Viewed", "Payment Info Entered",
                "Checkout Step Viewed", "Cart Viewed", "Product Viewed", "Checkout Started",
                "Payment Info Entered", "app_close",
            ],
            [
                {"channel": "chat", "message": "My payment failed twice. Please fix this urgently.", "sentiment_hint": "negative", "response_time_minutes": 4},
                {"channel": "email", "direction": "outbound", "message": "Payment help article clicked.", "opened": True, "clicked": True},
            ],
            _crm("gold", "high_value", "checkout_blocked", 12, 142, 22, "chat", "Asia/Kolkata", "open_ticket", True, 5),
            {"inactive_days": 0, "events_7d": 13, "messages_7d": 4},
            {"expected_state": "service_blocked_high_intent", "expected_action_family": "service_recovery_or_cart_reminder"},
            97,
        ),
        _user(
            "ECOM-C011",
            "wishlist_mid_funnel_consideration",
            [
                "Product List Viewed", "Product Viewed", "Product Added to Wishlist",
                "Product Viewed", "Product Added to Wishlist", "Products Searched",
                "Product Clicked", "Product Viewed", "email_opened", "Product Viewed",
                "Product Added to Wishlist", "app_close",
            ],
            [
                {"channel": "push", "message": "I am comparing products and may buy later.", "sentiment_hint": "neutral"},
                {"channel": "email", "direction": "outbound", "message": "Wishlist reminder opened.", "opened": True, "clicked": False},
            ],
            _crm("silver", "mid_value", "consideration", 3, 92, 45, "push", "Asia/Singapore", nps=25),
            {"inactive_days": 1, "events_7d": 9, "messages_7d": 2},
            {"expected_state": "consideration_mid_funnel", "expected_action_family": "content_or_recommendation"},
            108,
        ),
        _user(
            "ECOM-C012",
            "category_explorer_email_engaged",
            [
                "Product List Viewed", "Product List Filtered", "Product Clicked",
                "Product Viewed", "Products Searched", "Product List Viewed",
                "Product Clicked", "Product Viewed", "email_opened", "email_clicked",
                "Product List Filtered", "Product Viewed", "app_close",
            ],
            [
                {"channel": "email", "message": "I open your emails for new launches and lookbooks.", "sentiment_hint": "positive"},
                {"channel": "email", "direction": "outbound", "message": "Lookbook clicked.", "opened": True, "clicked": True},
            ],
            _crm("silver", "mid_value", "category_explorer", 5, 88, 19, "email", "Europe/Berlin", nps=40),
            {"inactive_days": 0, "events_7d": 8, "messages_7d": 2},
            {"expected_state": "exploration_receptive", "expected_action_family": "send_content"},
            119,
        ),
        _user(
            "ECOM-C013",
            "high_value_low_trust_recent_delivery_issue",
            [
                "Order Completed", "support_complaint", "Product Viewed", "Product Added",
                "Cart Viewed", "Product Removed", "Product Viewed", "app_close",
                "email_sent", "email_ignored", "Product Viewed", "Product Removed",
            ],
            [
                {"channel": "support_ticket", "message": "I do not trust this anymore after my last damaged delivery.", "sentiment_hint": "negative"},
                {"channel": "whatsapp", "direction": "outbound", "message": "Promo reminder seen but ignored.", "opened": True, "clicked": False},
            ],
            _crm("platinum", "high_value", "trust_recovery", 36, 260, 6, "email", "Asia/Kolkata", "open_ticket", True, -50),
            {"inactive_days": 2, "events_7d": 6, "messages_7d": 5, "recent_complaint": True},
            {"expected_state": "low_trust_high_value", "expected_action_family": "service_recovery_or_suppress"},
            130,
        ),
        _user(
            "ECOM-C014",
            "vip_replenishment_ready",
            [
                "Order Completed", "Product Reviewed", "app_open", "Product Viewed",
                "Product Added", "Cart Viewed", "Checkout Started", "Product Viewed",
                "Product Added", "Cart Viewed", "email_opened", "Product Viewed",
                "Product Added", "Checkout Started",
            ],
            [
                {"channel": "email", "message": "Please remind me when my usual product is back in stock.", "sentiment_hint": "positive"},
                {"channel": "email", "direction": "outbound", "message": "Replenishment reminder clicked.", "opened": True, "clicked": True},
            ],
            _crm("platinum", "high_value", "replenishment", 58, 175, 27, "email", "Asia/Kolkata", nps=68),
            {"inactive_days": 0, "events_7d": 14, "messages_7d": 1},
            {"expected_state": "high_intent_loyal", "expected_action_family": "product_recommendation_or_cart_reminder"},
            142,
        ),
        _user(
            "ECOM-C015",
            "subscription_cancelled_after_support",
            [
                "subscription_cancelled", "support_complaint", "app_open",
                "Product List Viewed", "Product Viewed", "Order Cancelled",
                "email_sent", "email_ignored", "app_close", "support_complaint",
                "Product Removed", "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "I cancelled because nobody helped me after repeated follow ups.", "sentiment_hint": "negative"},
                {"channel": "email", "direction": "outbound", "message": "Retention offer ignored.", "opened": False, "clicked": False},
            ],
            _crm("gold", "high_value", "cancelled", 18, 155, 11, "phone", "Asia/Kolkata", "escalated_ticket", True, -70),
            {"inactive_days": 14, "events_7d": 1, "messages_7d": 6, "recent_complaint": True},
            {"expected_state": "high_retention_risk", "expected_action_family": "service_recovery_or_retention"},
            154,
        ),
        _user(
            "ECOM-C016",
            "low_aov_flash_sale_responder",
            [
                "email_opened", "email_clicked", "Product List Viewed", "Product Viewed",
                "Coupon Applied", "Product Added", "Cart Viewed", "Checkout Started",
                "Order Completed", "Product Viewed", "Coupon Entered", "Product Added",
            ],
            [
                {"channel": "sms", "message": "Flash sale links work well for me.", "sentiment_hint": "positive"},
                {"channel": "sms", "direction": "outbound", "message": "Flash sale clicked.", "opened": True, "clicked": True},
            ],
            _crm("bronze", "price_sensitive", "deal_responder", 7, 31, 8, "sms", "Asia/Kolkata", loyalty_member=False, nps=30),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 2},
            {"expected_state": "price_sensitive_receptive", "expected_action_family": "discount_offer"},
            166,
            "mobile_web",
            "android",
        ),
        _user(
            "ECOM-C017",
            "returning_customer_whatsapp_negative",
            [
                "Product Viewed", "Product Added", "Cart Viewed", "whatsapp_sent",
                "whatsapp_ignored", "whatsapp_sent", "Product Removed", "app_close",
                "Product Viewed", "whatsapp_sent", "whatsapp_ignored", "Product Removed",
            ],
            [
                {"channel": "whatsapp", "message": "Do not message me on WhatsApp for shopping offers.", "sentiment_hint": "negative"},
                {"channel": "email", "direction": "outbound", "message": "Preference-centre email opened.", "opened": True, "clicked": False},
            ],
            _crm("silver", "mid_value", "channel_fatigued", 6, 84, 38, "email", "Asia/Kolkata", nps=0),
            {"inactive_days": 1, "events_7d": 7, "messages_7d": 7},
            {"expected_state": "channel_fatigue", "expected_action_family": "suppress_or_email_only"},
            178,
        ),
        _user(
            "ECOM-C018",
            "email_loyal_push_unresponsive",
            [
                "push_sent", "push_ignored", "push_sent", "push_ignored",
                "email_opened", "email_clicked", "Product List Viewed", "Product Viewed",
                "Product Added to Wishlist", "email_opened", "Product Viewed",
                "Product Added", "Cart Viewed",
            ],
            [
                {"channel": "email", "message": "Email works better for me than push.", "sentiment_hint": "positive"},
                {"channel": "push", "direction": "outbound", "message": "Push campaign ignored.", "opened": False, "clicked": False},
            ],
            _crm("gold", "high_value", "channel_preference_email", 21, 125, 16, "email", "Europe/London", nps=55),
            {"inactive_days": 0, "events_7d": 10, "messages_7d": 4},
            {"expected_state": "receptive_email_preferred", "expected_action_family": "email_recommendation"},
            190,
        ),
        _user(
            "ECOM-C019",
            "browse_after_bad_nps",
            [
                "Product List Viewed", "Product Viewed", "Product Viewed",
                "Product Removed", "support_complaint", "Product List Viewed",
                "Product Viewed", "app_close", "email_sent", "email_ignored",
                "Product Viewed", "Product Removed",
            ],
            [
                {"channel": "support_ticket", "message": "The product quality was disappointing and I expected better.", "sentiment_hint": "negative"},
            ],
            _crm("silver", "mid_value", "nps_detractor", 4, 70, 20, "email", "America/New_York", "closed_negative", True, -40),
            {"inactive_days": 2, "events_7d": 6, "messages_7d": 3, "recent_complaint": True},
            {"expected_state": "low_trust_explorer", "expected_action_family": "service_recovery_or_content"},
            202,
        ),
        _user(
            "ECOM-C020",
            "search_heavy_no_cart",
            [
                "Products Searched", "Product List Filtered", "Product Viewed",
                "Products Searched", "Product Viewed", "Product List Filtered",
                "Product Viewed", "Products Searched", "Product Viewed",
                "Product List Viewed", "Product Viewed", "app_close",
            ],
            [
                {"channel": "chat", "message": "I cannot find the right size.", "sentiment_hint": "neutral"},
            ],
            _crm("new", "unknown", "search_heavy", 0, 0, None, "in_app", "Asia/Kolkata", loyalty_member=False),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 1},
            {"expected_state": "exploration_with_assistance_need", "expected_action_family": "content_or_assistive_message"},
            214,
        ),
        _user(
            "ECOM-C021",
            "premium_browser_not_discount_sensitive",
            [
                "Product List Viewed", "Product Viewed", "Product Viewed",
                "Product Added", "Cart Viewed", "Product Removed", "Product Viewed",
                "Product Added to Wishlist", "email_opened", "Product Viewed",
                "Product Added", "Cart Viewed",
            ],
            [
                {"channel": "email", "message": "I am waiting for premium colors, not discounts.", "sentiment_hint": "positive"},
            ],
            _crm("platinum", "high_value", "premium_consideration", 24, 340, 17, "email", "Asia/Dubai", nps=50),
            {"inactive_days": 0, "events_7d": 11, "messages_7d": 1},
            {"expected_state": "premium_high_intent", "expected_action_family": "product_recommendation_no_discount"},
            226,
        ),
        _user(
            "ECOM-C022",
            "return_window_anxiety",
            [
                "Order Completed", "Product Viewed", "Product Reviewed",
                "support_complaint", "Product List Viewed", "Product Viewed",
                "Product Added", "Cart Viewed", "Product Removed", "Product Viewed",
                "app_close",
            ],
            [
                {"channel": "chat", "message": "I am worried about returns. Last return took too long.", "sentiment_hint": "negative"},
            ],
            _crm("gold", "high_value", "return_anxiety", 16, 180, 10, "chat", "Asia/Kolkata", "recent_return", True, 5),
            {"inactive_days": 1, "events_7d": 8, "messages_7d": 2, "recent_complaint": True},
            {"expected_state": "trust_sensitive_purchase_intent", "expected_action_family": "service_recovery_or_assurance_content"},
            238,
        ),
        _user(
            "ECOM-C023",
            "in_app_engaged_recent_buyer_cross_sell",
            [
                "Order Completed", "app_open", "Product List Viewed", "Product Viewed",
                "Product Clicked", "Product Viewed", "Product Added to Wishlist",
                "app_open", "Product List Viewed", "Product Viewed", "Product Added",
                "Cart Viewed", "app_close",
            ],
            [
                {"channel": "in_app", "message": "I liked the accessory recommendations.", "sentiment_hint": "positive"},
            ],
            _crm("gold", "high_value", "cross_sell", 19, 132, 5, "in_app", "Asia/Singapore", nps=58),
            {"inactive_days": 0, "events_7d": 13, "messages_7d": 2},
            {"expected_state": "cross_sell_receptive", "expected_action_family": "product_recommendation"},
            250,
        ),
        _user(
            "ECOM-C024",
            "high_frequency_open_no_click",
            [
                "email_opened", "Product List Viewed", "Product Viewed",
                "email_opened", "Product Viewed", "push_sent", "push_opened",
                "Product List Viewed", "Product Viewed", "email_opened", "app_close",
                "push_sent", "push_opened",
            ],
            [
                {"channel": "email", "direction": "outbound", "message": "Opened three campaigns with no click.", "opened": True, "clicked": False},
            ],
            _crm("silver", "mid_value", "engaged_non_clicker", 2, 67, 52, "email", "Europe/Berlin", nps=15),
            {"inactive_days": 0, "events_7d": 11, "messages_7d": 6},
            {"expected_state": "engaged_low_conversion", "expected_action_family": "content_or_offer_test"},
            262,
        ),
        _user(
            "ECOM-C025",
            "subscription_member_low_activity",
            [
                "app_open", "Product List Viewed", "app_close", "email_opened",
                "Product Viewed", "app_close", "email_sent", "email_ignored",
                "Product List Viewed", "app_close",
            ],
            [
                {"channel": "email", "message": "I am still a member but have not needed anything recently.", "sentiment_hint": "neutral"},
            ],
            _crm("gold", "high_value", "subscription_member", 22, 120, 64, "email", "America/New_York", nps=42),
            {"inactive_days": 9, "events_7d": 2, "messages_7d": 2},
            {"expected_state": "low_activity_loyal", "expected_action_family": "content_or_reactivation"},
            274,
        ),
        _user(
            "ECOM-C026",
            "support_resolved_recovering_trust",
            [
                "support_complaint", "Order Refunded", "app_open", "Product List Viewed",
                "Product Viewed", "Product Added to Wishlist", "email_opened",
                "Product Viewed", "Product Added", "Cart Viewed", "app_close",
            ],
            [
                {"channel": "support_ticket", "message": "Thanks for finally resolving this. I may shop again.", "sentiment_hint": "mixed"},
                {"channel": "email", "direction": "outbound", "message": "Apology email clicked.", "opened": True, "clicked": True},
            ],
            _crm("gold", "high_value", "trust_recovering", 15, 160, 24, "email", "Asia/Kolkata", "resolved", True, 15),
            {"inactive_days": 2, "events_7d": 6, "messages_7d": 2},
            {"expected_state": "trust_recovering_consideration", "expected_action_family": "content_or_soft_recommendation"},
            286,
        ),
        _user(
            "ECOM-C027",
            "low_stock_urgency",
            [
                "Product Viewed", "Product Viewed", "Product Added", "Cart Viewed",
                "Checkout Started", "Product Viewed", "Product Added", "Cart Viewed",
                "Checkout Step Viewed", "app_close", "Product Viewed", "Cart Viewed",
            ],
            [
                {"channel": "chat", "message": "Is this item going out of stock? I need it urgently.", "sentiment_hint": "urgent"},
            ],
            _crm("silver", "mid_value", "urgent_buyer", 4, 98, 30, "push", "Asia/Kolkata", nps=30),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 2},
            {"expected_state": "urgent_high_intent", "expected_action_family": "cart_reminder_or_stock_alert"},
            298,
        ),
        _user(
            "ECOM-C028",
            "gift_shopper_one_time_spike",
            [
                "Products Searched", "Product List Filtered", "Product Viewed",
                "Product Viewed", "Product Added", "Cart Viewed", "Product Added",
                "Checkout Started", "Payment Info Entered", "Order Completed",
                "Product List Viewed", "app_close",
            ],
            [
                {"channel": "chat", "message": "This is a gift purchase, I may not need regular updates.", "sentiment_hint": "neutral"},
            ],
            _crm("new", "unknown", "gift_shopper", 1, 210, 1, "email", "Europe/London", loyalty_member=False, nps=25),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 1},
            {"expected_state": "recent_conversion_limited_receptivity", "expected_action_family": "suppress_or_light_content"},
            310,
        ),
        _user(
            "ECOM-C029",
            "bulk_buyer_b2b_like_pattern",
            [
                "Product List Viewed", "Product Viewed", "Product Added",
                "Product Viewed", "Product Added", "Product Viewed", "Product Added",
                "Cart Viewed", "Checkout Started", "Payment Info Entered",
                "Checkout Step Completed", "Order Completed", "Product List Viewed",
                "Product Added", "Cart Viewed",
            ],
            [
                {"channel": "email", "message": "Can you send invoice and bulk purchase updates by email?", "sentiment_hint": "positive"},
            ],
            _crm("platinum", "high_value", "bulk_buyer", 62, 520, 4, "email", "Asia/Kolkata", nps=65),
            {"inactive_days": 0, "events_7d": 15, "messages_7d": 1},
            {"expected_state": "high_value_bulk_receptive", "expected_action_family": "product_recommendation_or_account_message"},
            322,
            "web",
            "desktop",
        ),
        _user(
            "ECOM-C030",
            "holiday_campaign_collision",
            [
                "email_sent", "email_opened", "push_sent", "push_opened",
                "whatsapp_sent", "Product List Viewed", "Product Viewed",
                "Product Added", "Cart Viewed", "sms_sent", "Product Removed",
                "email_sent", "Product Viewed", "app_close",
            ],
            [
                {"channel": "whatsapp", "message": "I got the same holiday offer on every channel.", "sentiment_hint": "negative"},
                {"channel": "email", "direction": "outbound", "message": "Holiday campaign clicked once.", "opened": True, "clicked": True},
            ],
            _crm("gold", "high_value", "campaign_collision", 13, 145, 18, "email", "Asia/Kolkata", nps=5),
            {"inactive_days": 0, "events_7d": 12, "messages_7d": 9},
            {"expected_state": "journey_collision_fatigue", "expected_action_family": "suppress_or_single_channel"},
            334,
        ),
    ],
}
