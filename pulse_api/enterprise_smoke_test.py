from fastapi.testclient import TestClient

from .main import app


def main() -> None:
    client = TestClient(app)

    demo_payload = client.get("/api/demo/manual-event-stream")
    ingest = client.post("/api/demo/run-manual-event-stream")
    action_centre = client.get("/api/action-centre")
    dashboard = client.get("/api/get-data")

    print(
        {
            "demo_payload": demo_payload.status_code,
            "ingest": ingest.status_code,
            "action_centre": action_centre.status_code,
            "get_data": dashboard.status_code,
            "data_mode": dashboard.json().get("data_mode"),
            "recommendations": len(action_centre.json().get("recommendations", [])),
            "processing_traces": len(
                action_centre.json().get("processing_trace", [])
            ),
            "metrics": action_centre.json().get("metrics"),
        }
    )


if __name__ == "__main__":
    main()
