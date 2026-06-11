from datetime import datetime, timedelta


class DeliveryPlanner:
    SEND_ACTIONS = {
        "send_product_recommendation",
        "send_content",
        "send_cart_reminder",
        "send_retention_message",
        "send_discount_offer",
        "service_recovery",
    }

    CONTENT_BY_ACTION = {
        "send_product_recommendation": "personalized_product_recommendation",
        "send_content": "educational_or_inspiration_content",
        "send_cart_reminder": "cart_completion_reminder",
        "send_retention_message": "winback_or_retention_message",
        "send_discount_offer": "price_incentive_offer",
        "service_recovery": "service_recovery_apology_or_resolution",
    }

    def build(self, action, behavioral_state, constraints, user_context=None):
        user_context = user_context or {}
        constraints = constraints or {}
        crm_context = user_context.get("crm_context", {})
        user_state = user_context.get("user_state", {})
        conflict_resolution = []
        custom_reasons = list(constraints.get("custom_rule_reasons") or [])

        if action == "suppress":
            reasons = ["suppression_selected_no_delivery"]
            if self._do_not_disturb_support(user_state, crm_context, constraints):
                reasons.append("support_ticket_do_not_disturb_policy_overrode_delivery")
            reasons.extend(custom_reasons)
            return {
                "should_send": False,
                "channel": None,
                "send_time": None,
                "content_type": "no_message",
                "conflict_resolution": reasons,
            }

        channel_plan = self._channel(action, crm_context, constraints, conflict_resolution)
        time_plan = self._time(action, crm_context, constraints, conflict_resolution)
        content_type = self.CONTENT_BY_ACTION.get(action, "generic_intervention")

        if self._do_not_disturb_support(user_state, crm_context, constraints):
            return {
                "should_send": False,
                "channel": None,
                "send_time": None,
                "content_type": "no_message_support_policy",
                "conflict_resolution": conflict_resolution
                + ["support_ticket_do_not_disturb_policy_overrode_delivery"],
            }

        return {
            "should_send": True,
            "channel": channel_plan,
            "send_time": time_plan,
            "content_type": content_type,
            "conflict_resolution": conflict_resolution,
        }

    def _channel(self, action, crm_context, constraints, conflict_resolution):
        preferred = crm_context.get("preferred_channel") or constraints.get("preferred_channel")
        allowed = constraints.get("allowed_channels") or [
            "push",
            "email",
            "whatsapp",
            "sms",
            "in_app",
            "chat",
            "phone",
        ]
        blocked = set(constraints.get("blocked_channels") or [])

        model_channel = self._model_channel(action, crm_context)
        if model_channel in blocked or model_channel not in allowed:
            fallback = self._first_allowed(preferred, allowed, blocked)
            conflict_resolution.append(
                f"model_channel_{model_channel}_blocked_or_disallowed_used_{fallback}"
            )
            return fallback

        if preferred and preferred != model_channel and preferred in allowed and preferred not in blocked:
            conflict_resolution.append(
                f"user_preferred_channel_{preferred}_overrode_model_channel_{model_channel}"
            )
            return preferred

        return model_channel

    def _model_channel(self, action, crm_context):
        if action == "service_recovery":
            if crm_context.get("preferred_channel") in {"phone", "chat", "email"}:
                return crm_context["preferred_channel"]
            return "email"
        if action == "send_retention_message":
            return "whatsapp"
        if action == "send_cart_reminder":
            return "push"
        if action == "send_discount_offer":
            return "email"
        if action == "send_content":
            return "email"
        return "push"

    def _first_allowed(self, preferred, allowed, blocked):
        if preferred and preferred in allowed and preferred not in blocked:
            return preferred
        for channel in allowed:
            if channel not in blocked:
                return channel
        return None

    def _time(self, action, crm_context, constraints, conflict_resolution):
        timezone = crm_context.get("timezone", "UTC")
        candidate_hour = self._candidate_hour(action)
        quiet_hours = constraints.get("quiet_hours") or {}
        send_time = f"{candidate_hour:02d}:00"

        if self._is_quiet_hour(candidate_hour, quiet_hours):
            adjusted_hour = self._quiet_hour_end(quiet_hours)
            conflict_resolution.append(
                f"candidate_send_time_{send_time}_inside_quiet_hours_moved_to_{adjusted_hour:02d}:00"
            )
            send_time = f"{adjusted_hour:02d}:00"

        return {
            "local_time": send_time,
            "timezone": timezone,
        }

    def _candidate_hour(self, action):
        if action in {"send_cart_reminder", "service_recovery"}:
            return 22
        if action == "send_content":
            return 11
        if action == "send_discount_offer":
            return 19
        if action == "send_retention_message":
            return 18
        return 20

    def _is_quiet_hour(self, hour, quiet_hours):
        if not quiet_hours:
            return False
        start = self._hour(quiet_hours.get("start", "21:00"))
        end = self._hour(quiet_hours.get("end", "09:00"))
        if start > end:
            return hour >= start or hour < end
        return start <= hour < end

    def _quiet_hour_end(self, quiet_hours):
        return self._hour(quiet_hours.get("end", "09:00"))

    def _hour(self, value):
        return int(str(value).split(":", 1)[0])

    def _do_not_disturb_support(self, user_state, crm_context, constraints):
        if not constraints.get("do_not_disturb_if_support_ticket_open_days"):
            return False
        days = int(constraints["do_not_disturb_if_support_ticket_open_days"])
        support_status = crm_context.get("support_status")
        open_days = int(user_state.get("support_ticket_open_days", 0) or crm_context.get("support_ticket_open_days", 0) or 0)
        return support_status in {"open_ticket", "escalated_ticket"} and open_days >= days
