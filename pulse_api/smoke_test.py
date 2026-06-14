from fastapi.testclient import TestClient

from .config import DEFAULT_CORS_ORIGINS
from .main import app


def main():
    client = TestClient(app)
    lovable_origin = "https://pulse-customer-intelligence.lovable.app"

    health = client.get("/api/health")
    login = client.post(
        "/api/login",
        json={"email": "pm@pulse.ai", "password": "demo-password"},
    )
    data = client.get(
        "/api/get-data",
        headers={"Origin": lovable_origin},
    )
    data_body = data.json()
    profile = client.get(
        "/api/profile",
        headers={"Origin": lovable_origin},
    )
    behavioral_state = client.post(
        "/api/behavioral-state",
        json={
            "event": {
                "user_id": "U100",
                "signals": {
                    "purchase_intent": 0.82,
                    "exploration_intent": 0.45,
                    "churn_risk": 0.22,
                },
                "tags": ["high_consideration_user"],
                "confidence": 0.86,
            },
            "voc": {
                "user_id": "U100",
                "signals": {
                    "frustration_signal": 0.68,
                    "urgency_signal": 0.72,
                    "trust_signal": 0.41,
                    "retention_risk": 0.63,
                    "engagement_signal": 0.55,
                    "escalation_risk": 0.70,
                },
                "tags": ["emotionally_negative"],
                "confidence": 0.82,
            },
            "crm_context": {
                "user_id": "U100",
                "customer_tier": "gold",
                "ltv_segment": "high_value",
                "total_orders": 16,
                "average_order_value": 240,
            },
        },
    )

    print(
        {
            "health": health.status_code,
            "login": login.status_code,
            "get_data": data.status_code,
            "get_data_recommendations": len(
                data_body.get("action_centre", {}).get("recommendation_queue", [])
            ),
            "profile": profile.status_code,
            "behavioral_state": behavioral_state.status_code,
            "cors_origin": data.headers.get("access-control-allow-origin"),
            "expected_origin": lovable_origin,
        }
    )


if __name__ == "__main__":
    main()
