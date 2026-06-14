from fastapi.testclient import TestClient

from .main import app


LOVABLE_UPLOAD_PAYLOAD = {
    "workspace": "Flipster Ecommerce",
    "source": "manual_upload",
    "data": {
        "workspace": "Pulse AI Demo",
        "users": [
            {
                "user_id": "u_001",
                "traits": {
                    "tier": "loyal",
                    "city": "Mumbai",
                },
                "events": [
                    {
                        "type": "product_view",
                        "ts": "2026-06-09T18:22:00Z",
                        "sku": "AUR-101",
                    },
                    {
                        "type": "wishlist_add",
                        "ts": "2026-06-09T18:23:00Z",
                        "sku": "AUR-101",
                    },
                ],
                "comms": [
                    {
                        "channel": "push",
                        "ts": "2026-06-08T13:00:00Z",
                        "opened": True,
                    }
                ],
            }
        ],
    },
}


def main() -> None:
    client = TestClient(app)
    sample = client.get("/api/demo/enterprise-upload-sample")
    if sample.status_code != 200:
        raise AssertionError(sample.text)
    sample_body = sample.json()
    sample_users = sample_body["data"]["users"]
    if len(sample_users) != 5:
        raise AssertionError("Enterprise upload sample must contain 5 users.")
    if any(not user.get("events") for user in sample_users):
        raise AssertionError("Every sample user must include event rows.")

    response = client.post("/api/enterprise-data", json=LOVABLE_UPLOAD_PAYLOAD)
    if response.status_code != 200:
        raise AssertionError(response.text)

    body = response.json()
    action_centre = client.get(
        f"/api/action-centre?workspace_id={body['workspace_id']}"
    )
    if action_centre.status_code != 200:
        raise AssertionError(action_centre.text)

    details = action_centre.json()["action_centre"]["recommendation_details"]
    first_detail = details["u_001"]
    if not first_detail["event_stream"]:
        raise AssertionError("Normalized Lovable upload must expose event_stream.")

    print(
        {
            "ingest": response.status_code,
            "sample_users": len(sample_users),
            "workspace_id": body["workspace_id"],
            "users_ingested": body["users_ingested"],
            "action_centre": action_centre.status_code,
            "event_stream_count": len(first_detail["event_stream"]),
        }
    )


if __name__ == "__main__":
    main()
