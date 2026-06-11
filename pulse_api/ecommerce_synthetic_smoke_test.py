import os

from fastapi.testclient import TestClient

from .main import app


def main() -> None:
    os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"

    client = TestClient(app)

    corpus = client.get("/api/test-data/ecommerce-scenarios")
    ingest = client.post("/api/test-data/run-ecommerce-scenarios")
    action_centre = client.get("/api/action-centre?workspace_id=ecommerce_synthetic_eval")
    dashboard = client.get("/api/get-data")

    action_body = action_centre.json()
    recommendations = action_body.get("recommendations", [])

    print(
        {
            "corpus": corpus.status_code,
            "ingest": ingest.status_code,
            "action_centre": action_centre.status_code,
            "get_data": dashboard.status_code,
            "users_in_corpus": len(corpus.json().get("users", [])),
            "recommendations": len(recommendations),
            "processing_traces": len(action_body.get("processing_trace", [])),
            "state_labels": sorted(
                {
                    item["behavioral_state"]["state_label"]
                    for item in recommendations
                }
            ),
            "actions": sorted(
                {
                    item["recommended_action"]
                    for item in recommendations
                }
            ),
            "scenario_actions": {
                item.get("scenario", item["user_id"]): {
                    "state_label": item["behavioral_state"]["state_label"],
                    "recommended_action": item["recommended_action"],
                }
                for item in recommendations
            },
            "metrics": action_body.get("metrics"),
        }
    )


if __name__ == "__main__":
    main()
