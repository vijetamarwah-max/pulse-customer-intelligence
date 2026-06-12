from .demo_manual_event_stream import DEMO_MANUAL_EVENT_STREAM


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

    print(
        {
            "users": len(users),
            "raw_event_counts": raw_event_counts,
            "event_stream_counts": event_stream_counts,
            "first_event": users[0]["events"]["event_stream"][0],
        }
    )


if __name__ == "__main__":
    main()
