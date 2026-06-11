import os

from fastapi.testclient import TestClient

from .main import app


def main() -> None:
    os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"

    client = TestClient(app)
    corpus = client.get("/api/test-data/ecommerce-comprehensive-scenarios")
    body = corpus.json()

    users = body.get("users", [])
    event_counts = [
        len(user.get("events", {}).get("raw_events", []))
        for user in users
    ]
    comms_counts = [
        len(user.get("comms_history", []))
        for user in users
    ]

    print(
        {
            "corpus": corpus.status_code,
            "users": len(users),
            "min_events_per_user": min(event_counts),
            "max_events_per_user": max(event_counts),
            "total_events": sum(event_counts),
            "total_comms": sum(comms_counts),
            "sample_scenarios": [
                user["scenario"] for user in users[:5]
            ],
            "crm_states": sorted(
                {
                    user["crm_context"]["lifecycle_stage"]
                    for user in users
                }
            ),
        }
    )


if __name__ == "__main__":
    main()
