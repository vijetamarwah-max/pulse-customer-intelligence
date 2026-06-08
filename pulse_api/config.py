import os


DEFAULT_CORS_ORIGINS = [
    "https://pulse-behavior-ai.lovable.app",
    "https://id-preview--8ca02ac1-f8a8-4c13-ba27-d65509f12369.lovable.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


def get_cors_origins():
    configured = os.getenv("PULSE_CORS_ORIGINS")
    if not configured:
        return DEFAULT_CORS_ORIGINS

    return [origin.strip() for origin in configured.split(",") if origin.strip()]
