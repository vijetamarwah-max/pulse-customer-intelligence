import os
from dataclasses import dataclass
from typing import Any

from fastapi.testclient import TestClient

from .main import app
from .test_data.ecommerce_synthetic import ECOMMERCE_SYNTHETIC_TEST_PAYLOAD
from .test_data.mixed_signal_scenarios import MIXED_SIGNAL_SCENARIO_PAYLOAD
from .test_data.nba_conflict_scenarios import NBA_CONFLICT_SCENARIO_PAYLOAD


@dataclass
class Check:
    name: str
    threshold: float = 1.0
    passed: int = 0
    total: int = 0

    @property
    def rate(self) -> float:
        return round(self.passed / self.total, 3) if self.total else 0.0

    @property
    def status(self) -> str:
        return "PASS" if self.rate >= self.threshold else "FAIL"


ACTION_FAMILIES = {
    "cart_reminder_or_product_recommendation": {"send_cart_reminder", "send_product_recommendation"},
    "suppress_or_service_recovery": {"suppress", "service_recovery"},
    "send_content_or_light_recommendation": {"send_content", "send_product_recommendation"},
    "send_retention_message": {"send_retention_message"},
    "send_content_or_product_recommendation": {"send_content", "send_product_recommendation"},
    "send_discount_offer": {"send_discount_offer"},
    "service_recovery_or_suppress": {"service_recovery", "suppress"},
    "send_content": {"send_content"},
    "service_recovery_or_cart_reminder": {"service_recovery", "send_cart_reminder"},
    "suppress": {"suppress"},
}

MIXED_EXPECTED_ACTIONS = {
    "explores_but_ignores_all_comms_14d": {"send_content", "suppress"},
    "high_cart_intent_but_recent_negative_support": {"service_recovery", "suppress"},
    "recent_purchase_browsing_again_but_fatigued": {"suppress", "send_content"},
    "dormant_high_value_positive_comms": {"send_retention_message", "send_content"},
    "discount_seeker_but_premium_tier_no_discount_policy": {
        "send_cart_reminder",
        "send_product_recommendation",
        "send_content",
        "suppress",
    },
    "urgent_checkout_need_but_quiet_hours": {"send_cart_reminder", "send_product_recommendation"},
    "loyal_opens_email_but_push_unresponsive": {
        "send_cart_reminder",
        "send_product_recommendation",
        "send_content",
    },
    "low_value_high_complaint_but_browsing": {"suppress", "service_recovery"},
}


def _run_suite(client: TestClient, run_path: str, workspace_id: str) -> list[dict[str, Any]]:
    run = client.post(run_path)
    run.raise_for_status()
    response = client.get(f"/api/action-centre?workspace_id={workspace_id}")
    response.raise_for_status()
    return response.json().get("recommendations", [])


def _extract_hour(send_time: Any) -> int | None:
    if not send_time:
        return None
    if isinstance(send_time, dict):
        send_time = send_time.get("time") or send_time.get("local_time") or send_time.get("value")
    if not isinstance(send_time, str):
        return None
    hour = int(send_time.split(":")[0])
    return hour


def _quiet_hour_violation(send_time: Any) -> bool:
    hour = _extract_hour(send_time)
    if hour is None:
        return False
    return hour >= 21 or hour < 9


def main() -> None:
    os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"
    client = TestClient(app)

    ecommerce = _run_suite(client, "/api/test-data/run-ecommerce-scenarios", "ecommerce_synthetic_eval")
    mixed = _run_suite(client, "/api/test-data/run-mixed-signal-scenarios", "mixed_signal_eval")
    conflict = _run_suite(client, "/api/test-data/run-nba-conflict-scenarios", "nba_conflict_eval")

    checks = {
        "recommendation_action_alignment": Check("recommendation_action_alignment", threshold=0.85),
        "suppression_or_service_recovery_recall": Check("suppression_or_service_recovery_recall", threshold=0.75),
        "hard_constraint_compliance": Check("hard_constraint_compliance", threshold=1.0),
        "mixed_signal_auto_approve_guardrail": Check("mixed_signal_auto_approve_guardrail", threshold=0.8),
        "delivery_metadata_completeness": Check("delivery_metadata_completeness", threshold=1.0),
        "action_centre_confidence_band_completeness": Check("action_centre_confidence_band_completeness", threshold=1.0),
        "expected_value_sanity": Check("expected_value_sanity", threshold=1.0),
    }
    failures = []

    expectation_by_scenario = ECOMMERCE_SYNTHETIC_TEST_PAYLOAD["evaluation_expectations"]
    for rec in ecommerce:
        scenario = rec["scenario"]
        expected_family = expectation_by_scenario[scenario]["expected_action_family"]
        expected_actions = ACTION_FAMILIES[expected_family]
        checks["recommendation_action_alignment"].total += 1
        action_matches = rec["recommended_action"] in expected_actions
        checks["recommendation_action_alignment"].passed += int(action_matches)
        if not action_matches:
            failures.append(
                {
                    "suite": "ecommerce_synthetic",
                    "scenario": scenario,
                    "actual_action": rec["recommended_action"],
                    "expected_actions": sorted(expected_actions),
                    "confidence": rec["confidence"],
                }
            )

        if "suppress" in expected_actions or "service_recovery" in expected_actions:
            checks["suppression_or_service_recovery_recall"].total += 1
            checks["suppression_or_service_recovery_recall"].passed += int(
                rec["recommended_action"] in {"suppress", "service_recovery"}
            )

    for rec in mixed:
        expected_actions = MIXED_EXPECTED_ACTIONS[rec["scenario"]]
        checks["recommendation_action_alignment"].total += 1
        action_matches = rec["recommended_action"] in expected_actions
        checks["recommendation_action_alignment"].passed += int(action_matches)
        if not action_matches:
            failures.append(
                {
                    "suite": "mixed_signal",
                    "scenario": rec["scenario"],
                    "actual_action": rec["recommended_action"],
                    "expected_actions": sorted(expected_actions),
                    "confidence": rec["confidence"],
                }
            )

        if "suppress" in expected_actions or "service_recovery" in expected_actions:
            checks["suppression_or_service_recovery_recall"].total += 1
            checks["suppression_or_service_recovery_recall"].passed += int(
                rec["recommended_action"] in {"suppress", "service_recovery"}
            )

        checks["mixed_signal_auto_approve_guardrail"].total += 1
        checks["mixed_signal_auto_approve_guardrail"].passed += int(float(rec["confidence"]) < 0.8)

    conflict_by_scenario = {rec["scenario"]: rec for rec in conflict}
    conflict_expectations = {
        "high_intent_low_fatigue_should_send": lambda r: r["recommended_action"] != "suppress"
        and r["delivery_plan"]["should_send"],
        "high_intent_high_fatigue_should_not_promo": lambda r: r["recommended_action"]
        in {"service_recovery", "suppress"},
        "nba_channel_whatsapp_user_prefers_push": lambda r: r["delivery_plan"]["channel"] == "push",
        "recommended_time_inside_quiet_hours": lambda r: not _quiet_hour_violation(
            r["delivery_plan"].get("send_time")
        ),
        "support_ticket_open_14_days_do_not_disturb": lambda r: r["recommended_action"] == "suppress"
        and not r["delivery_plan"]["should_send"]
        and "custom_rule_support_ticket_open_14_days" in r["delivery_plan"]["conflict_resolution"],
    }
    for scenario, assertion in conflict_expectations.items():
        checks["hard_constraint_compliance"].total += 1
        checks["hard_constraint_compliance"].passed += int(assertion(conflict_by_scenario[scenario]))

    all_recs = ecommerce + mixed + conflict
    for rec in all_recs:
        delivery = rec.get("delivery_plan", {})
        checks["delivery_metadata_completeness"].total += 1
        checks["delivery_metadata_completeness"].passed += int(
            all(
                key in delivery
                for key in ["should_send", "channel", "send_time", "content_type", "conflict_resolution"]
            )
        )

        checks["expected_value_sanity"].total += 1
        checks["expected_value_sanity"].passed += int(float(rec.get("expected_value", 0)) >= 0)

        checks["action_centre_confidence_band_completeness"].total += 1
        checks["action_centre_confidence_band_completeness"].passed += int("confidence" in rec)

    summary = {
        "suite_size": {
            "ecommerce_synthetic": len(ecommerce),
            "mixed_signal": len(mixed),
            "nba_conflict": len(conflict),
            "total_recommendations": len(all_recs),
        },
        "checks": {
            name: {
                "passed": check.passed,
                "total": check.total,
                "pass_rate": check.rate,
                "threshold": check.threshold,
                "status": check.status,
            }
            for name, check in checks.items()
        },
        "overall": {
            "passed": sum(check.passed for check in checks.values()),
            "total": sum(check.total for check in checks.values()),
        },
        "known_gaps": [
            "Auto-approve precision needs realized outcome labels; current suite only checks confidence gating.",
            "Transcription accuracy needs real audio ground truth; Kannada noisy test currently measures semantic adequacy only.",
            "Expected value calibration needs observed revenue outcomes; current check is a sanity check, not accuracy.",
        ],
        "recommendation_failures": failures,
    }
    summary["overall"]["pass_rate"] = round(summary["overall"]["passed"] / summary["overall"]["total"], 3)
    summary["overall"]["status"] = "PASS" if summary["overall"]["pass_rate"] >= 0.8 else "FAIL"

    print(summary)


if __name__ == "__main__":
    main()
