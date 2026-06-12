import os

from .demo_manual_event_stream import DEMO_MANUAL_EVENT_STREAM

os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"

from .recommendation_service import RecommendationService


def main() -> None:
    users = DEMO_MANUAL_EVENT_STREAM["users"]
    raw_event_counts = [len(user["events"].get("raw_events", [])) for user in users]
    event_stream_counts = [
        len(user["events"].get("event_stream", [])) for user in users
    ]
    if len(users) != 5:
        raise AssertionError("Manual demo payload must contain exactly 5 users.")
    if any(count == 0 for count in raw_event_counts):
        raise AssertionError("Every demo user must include raw_events.")
    if any(count == 0 for count in event_stream_counts):
        raise AssertionError("Every demo user must include event_stream.")

    computed = RecommendationService().build_action_centre(DEMO_MANUAL_EVENT_STREAM)
    details = computed["action_centre"]["recommendation_details"]
    first_detail = details[users[0]["user_id"]]
    if not first_detail.get("event_stream"):
        raise AssertionError("Action Centre detail must expose event_stream.")
    if not first_detail.get("recent_activity"):
        raise AssertionError("Action Centre detail must expose recent_activity.")

    print(
        {
            "users": len(users),
            "raw_event_counts": raw_event_counts,
            "event_stream_counts": event_stream_counts,
            "recommendation_details": len(details),
            "first_detail_recent_activity": len(first_detail["recent_activity"]),
            "first_event": users[0]["events"]["event_stream"][0],
        }
    )


if __name__ == "__main__":
    main()
