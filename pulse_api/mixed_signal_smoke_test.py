import os

from fastapi.testclient import TestClient

from .main import app


def main() -> None:
    os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"
    client = TestClient(app)
    corpus = client.get("/api/test-data/mixed-signal-scenarios")
    ingest = client.post("/api/test-data/run-mixed-signal-scenarios")
    action_centre = client.get("/api/action-centre?workspace_id=mixed_signal_eval")
    recommendations = action_centre.json().get("recommendations", [])

    print(
        {
            "corpus": corpus.status_code,
            "ingest": ingest.status_code,
            "action_centre": action_centre.status_code,
            "outputs": [
                {
                    "user_id": item["user_id"],
                    "scenario": item["scenario"],
                    "state_label": item["behavioral_state"]["state_label"],
                    "recommended_action": item["recommended_action"],
                    "confidence": item["confidence"],
                    "delivery_plan": item["delivery_plan"],
                }
                for item in recommendations
            ],
        }
    )


if __name__ == "__main__":
    main()
