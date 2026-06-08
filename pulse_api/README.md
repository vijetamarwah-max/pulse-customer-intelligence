# Pulse AI API

FastAPI backend for the Pulse AI frontend.

## CORS

Allowed origins are configured in `pulse_api/config.py` and can be overridden
with:

```text
PULSE_CORS_ORIGINS=https://pulse-behavior-ai.lovable.app,https://your-production-domain.com
```

Default allowed origins include:

- `https://pulse-behavior-ai.lovable.app`
- `https://id-preview--8ca02ac1-f8a8-4c13-ba27-d65509f12369.lovable.app`
- local development origins

## Run

```bash
uvicorn pulse_api.main:app --reload --host 0.0.0.0 --port 8000
```

Production entrypoint:

```bash
uvicorn pulse_api.asgi:app --host 0.0.0.0 --port 8000
```

## Smoke Test

```bash
python -m pulse_api.smoke_test
```

## Frontend Endpoints

- `GET /api/profile`
- `GET /api/get-data`
- `POST /api/login`
- `POST /api/behavioral-state`

See `DEPLOYMENT.md` for Render deployment steps.
