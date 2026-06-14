from fastapi.testclient import TestClient

from .main import app


def main() -> None:
    client = TestClient(app)
    ingest = client.post("/api/demo/run-manual-event-stream")
    if ingest.status_code != 200:
        raise AssertionError(ingest.text)

    action_centre = client.get("/api/action-centre")
    if action_centre.status_code != 200:
        raise AssertionError(action_centre.text)

    rows = action_centre.json()["action_centre"]["recommendation_queue"]
    auto_rows = [row for row in rows if row["auto_approve_eligible"]]

    print(
        [
            {
                "user_id": row["user_id"],
                "action": row["recommended_action"],
                "confidence": row["confidence_percent"],
                "band": row["confidence_band"],
            }
            for row in rows
        ]
    )

    if len(auto_rows) < 3:
        raise AssertionError("Demo should include at least 3 auto-approve recommendations.")


if __name__ == "__main__":
    main()
