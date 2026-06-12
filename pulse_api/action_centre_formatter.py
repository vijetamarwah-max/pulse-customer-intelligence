class ActionCentreFormatter:
    def build(self, recommendations):
        rows = [self._row(item) for item in recommendations]
        return {
            "recommendation_queue": rows,
            "recommendation_details": {
                item["user_id"]: self._detail(item) for item in recommendations
            },
            "execution_summary": self._summary(rows),
        }

    def _row(self, item):
        confidence_percent = round(item["confidence"] * 100)
        delivery_plan = item.get("delivery_plan", {})
        return {
            "user_id": item["user_id"],
            "user_name": self._display_name(item),
            "scenario": item.get("scenario"),
            "recommended_action": item["recommended_action"],
            "action_label": self._action_label(item["recommended_action"]),
            "channel": delivery_plan.get("channel"),
            "send_window": delivery_plan.get("send_time"),
            "suggested_copy": self._suggested_copy(item),
            "confidence": item["confidence"],
            "confidence_percent": confidence_percent,
            "confidence_band": self._confidence_band(item["confidence"]),
            "execution_status": self._execution_status(item["confidence"]),
            "auto_approve_eligible": item["confidence"] >= 0.8,
            "expected_value": round(item.get("expected_incremental_value", 0.0), 2),
            "expected_value_per_comms": self._expected_value_per_comms(item),
            "should_send": delivery_plan.get("should_send", False),
            "content_type": delivery_plan.get("content_type"),
            "conflict_resolution": delivery_plan.get("conflict_resolution", []),
        }

    def _detail(self, item):
        state = item["behavioral_state"]["state_vector"]
        delivery_plan = item.get("delivery_plan", {})
        return {
            "user_id": item["user_id"],
            "scenario": item.get("scenario"),
            "source_data": item.get("source_data", {}),
            "behavioral_profile": {
                "state_label": item["behavioral_state"]["state_label"],
                "signals": {
                    "purchase_intent": round(state.get("purchase_readiness", 0) * 100),
                    "fatigue": round(state.get("communication_fatigue", 0) * 100),
                    "churn_risk": round(state.get("retention_risk", 0) * 100),
                    "discount_sensitivity": round(state.get("discount_sensitivity", 0) * 100),
                    "trust_level": round(state.get("trust_level", 0) * 100),
                    "intervention_receptiveness": round(state.get("intervention_receptiveness", 0) * 100),
                },
            },
            "recommended_action": {
                "action": item["recommended_action"],
                "action_label": self._action_label(item["recommended_action"]),
                "channel": delivery_plan.get("channel"),
                "send_window": delivery_plan.get("send_time"),
                "content_type": delivery_plan.get("content_type"),
                "suggested_copy": self._suggested_copy(item),
                "confidence": item["confidence"],
                "confidence_percent": round(item["confidence"] * 100),
                "confidence_band": self._confidence_band(item["confidence"]),
                "execution_status": self._execution_status(item["confidence"]),
                "expected_value": round(item.get("expected_incremental_value", 0.0), 2),
                "expected_value_per_comms": self._expected_value_per_comms(item),
                "conversion_lift": self._conversion_lift(item),
                "fatigue_impact": self._fatigue_impact(item),
                "should_send": delivery_plan.get("should_send", False),
                "conflict_resolution": delivery_plan.get("conflict_resolution", []),
            },
            "why_this_action": self._why_this_action(item),
            "recent_activity": self._recent_activity(item),
            "event_stream": item.get("source_data", {}).get("event_stream", []),
            "communication_history": item.get("source_data", {}).get("comms_history", []),
            "crm_context": item.get("source_data", {}).get("crm_context", {}),
            "top_behavioral_signals": self._top_behavioral_signals(item),
            "alternatives_ruled_out": self._alternatives(item),
            "similar_users": self._similar_users(item),
            "raw_reasoning": {
                "deterministic_reasons": item.get("reasoning", []),
                "llm_reasoning": item.get("llm_reasoning"),
            },
        }

    def _confidence_band(self, confidence):
        if confidence >= 0.8:
            return "auto_approve"
        if confidence >= 0.6:
            return "observe"
        return "reject"

    def _execution_status(self, confidence):
        if confidence >= 0.8:
            return "Auto"
        if confidence >= 0.6:
            return "Observe"
        return "Reject"

    def _expected_value_per_comms(self, item):
        if not item.get("delivery_plan", {}).get("should_send", False):
            return 0.0
        return round(item.get("expected_incremental_value", 0.0), 2)

    def _action_label(self, action):
        labels = {
            "suppress": "Suppress - cooldown",
            "send_product_recommendation": "Personalized recommendation",
            "send_content": "Browse follow-up",
            "send_cart_reminder": "Cart recovery nudge",
            "send_retention_message": "Re-engagement series",
            "send_discount_offer": "Discount offer",
            "service_recovery": "Service recovery",
        }
        return labels.get(action, action.replace("_", " ").title())

    def _suggested_copy(self, item):
        action = item["recommended_action"]
        scenario_name = (item.get("scenario") or item["user_id"]).replace("_", " ")
        if action == "suppress":
            return f"No message - {scenario_name} is better protected by cooldown."
        if action == "service_recovery":
            return "We are sorry about the recent issue. Our team is prioritizing a resolution before sending offers."
        if action == "send_retention_message":
            return "It has been a while. Here are fresh picks based on what you liked before."
        if action == "send_cart_reminder":
            return "Still thinking it over? Your cart is saved and ready when you are."
        if action == "send_discount_offer":
            return "A limited offer is available on the items you were considering."
        if action == "send_content":
            return "Picked up where you left off with a few ideas you may like."
        return "Recommended picks are ready based on your recent browsing."

    def _why_this_action(self, item):
        state = item["behavioral_state"]["state_vector"]
        return (
            f"Pulse selected {self._action_label(item['recommended_action'])} because "
            f"purchase intent is {round(state.get('purchase_readiness', 0) * 100)}%, "
            f"fatigue is {round(state.get('communication_fatigue', 0) * 100)}%, "
            f"trust is {round(state.get('trust_level', 0) * 100)}%, and expected value is "
            f"{round(item.get('expected_incremental_value', 0.0), 2)}."
        )

    def _top_behavioral_signals(self, item):
        state = item["behavioral_state"]["state_vector"]
        candidates = [
            ("Purchase readiness", state.get("purchase_readiness", 0)),
            ("Communication fatigue", state.get("communication_fatigue", 0)),
            ("Trust level", state.get("trust_level", 0)),
            ("Retention risk", state.get("retention_risk", 0)),
            ("Discount sensitivity", state.get("discount_sensitivity", 0)),
            ("Brand affinity", state.get("brand_affinity", 0)),
        ]
        return [
            {"label": label, "weight": round(value * 100), "description": self._signal_description(label, value)}
            for label, value in sorted(candidates, key=lambda row: row[1], reverse=True)[:4]
        ]

    def _signal_description(self, label, value):
        return f"{round(value * 100)} signal strength"

    def _recent_activity(self, item):
        source_data = item.get("source_data", {})
        event_stream = source_data.get("event_stream", [])
        activity = []

        for event in event_stream[-6:]:
            activity.append(
                {
                    "type": "event",
                    "label": event.get("event_name"),
                    "timestamp": event.get("timestamp"),
                    "channel": event.get("channel"),
                    "description": self._event_description(event),
                    "metadata": {
                        "source": event.get("source"),
                        "device": event.get("device"),
                        "properties": event.get("properties", {}),
                    },
                }
            )

        for comm in source_data.get("comms_history", [])[-3:]:
            activity.append(
                {
                    "type": "communication",
                    "label": f"{comm.get('channel', 'communication')} message",
                    "timestamp": comm.get("sent_at"),
                    "channel": comm.get("channel"),
                    "description": comm.get("message"),
                    "metadata": {
                        "direction": comm.get("direction"),
                        "sentiment_hint": comm.get("sentiment_hint"),
                    },
                }
            )

        return sorted(
            activity,
            key=lambda row: row.get("timestamp") or "",
            reverse=True,
        )[:8]

    def _event_description(self, event):
        properties = event.get("properties", {})
        product = properties.get("product_name")
        category = properties.get("category")
        if product and category:
            return f"{event.get('event_name')} - {product} ({category})"
        if product:
            return f"{event.get('event_name')} - {product}"
        return event.get("event_name")

    def _alternatives(self, item):
        selected = item["recommended_action"]
        ranked = item.get("ranked_actions", {})
        alternatives = []
        for action, value in ranked.items():
            if action == selected:
                continue
            alternatives.append(
                {
                    "action": action,
                    "action_label": self._action_label(action),
                    "expected_value": round(value, 2),
                    "reason": f"Lower expected value than selected action by {round(ranked[selected] - value, 2)}.",
                }
            )
            if len(alternatives) == 3:
                break
        return alternatives

    def _similar_users(self, item):
        outcomes = item.get("predicted_outcomes", {}).get("predicted_outcomes", {})
        selected = item["recommended_action"]
        metrics = outcomes.get(selected, {})
        sample_size = metrics.get("sample_size", 0)
        similarity = metrics.get("average_similarity", 0)
        return {
            "matched_users": sample_size,
            "average_similarity": similarity,
            "evidence": f"{sample_size} similar records; average similarity {round(similarity * 100)}%.",
        }

    def _conversion_lift(self, item):
        selected = item["recommended_action"]
        outcomes = item.get("predicted_outcomes", {}).get("predicted_outcomes", {})
        selected_conversion = outcomes.get(selected, {}).get("conversion_probability", 0)
        baseline = outcomes.get("suppress", {}).get("conversion_probability", 0)
        return round((selected_conversion - baseline) * 100, 1)

    def _fatigue_impact(self, item):
        action = item["recommended_action"]
        if action == "suppress":
            return "-4 pts"
        if action == "service_recovery":
            return "-2 pts"
        if action in {"send_discount_offer", "send_cart_reminder"}:
            return "+3 pts"
        return "+1 pts"

    def _display_name(self, item):
        return item.get("scenario") or item["user_id"]

    def _summary(self, rows):
        return {
            "total": len(rows),
            "auto_execute": sum(1 for row in rows if row["confidence_band"] == "auto_approve"),
            "observation": sum(1 for row in rows if row["confidence_band"] == "observe"),
            "reject": sum(1 for row in rows if row["confidence_band"] == "reject"),
        }
