from fastapi.testclient import TestClient

from .config import DEFAULT_CORS_ORIGINS
from .main import app


def main():
    client = TestClient(app)

    health = client.get("/api/health")
    login = client.post(
        "/api/login",
        json={"email": "pm@pulse.ai", "password": "demo-password"},
    )
    data = client.get(
        "/api/get-data",
        headers={"Origin": DEFAULT_CORS_ORIGINS[0]},
    )
    profile = client.get(
        "/api/profile",
        headers={"Origin": DEFAULT_CORS_ORIGINS[0]},
    )

    print(
        {
            "health": health.status_code,
            "login": login.status_code,
            "get_data": data.status_code,
            "profile": profile.status_code,
            "cors_origin": data.headers.get("access-control-allow-origin"),
        }
    )


if __name__ == "__main__":
    main()
