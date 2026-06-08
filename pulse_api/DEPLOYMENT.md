# Deploy Pulse AI API

## Render

1. Push this repository to GitHub.
2. In Render, create a new Blueprint or Web Service from the repository.
3. Use `render.yaml` when creating a Blueprint, or configure manually:

```text
Runtime: Docker
Health check path: /api/health
```

4. Set these environment variables in Render:

```text
PULSE_CORS_ORIGINS=https://pulse-customer-intelligence.lovable.app,https://pulse-behavior-ai.lovable.app,https://id-preview--8ca02ac1-f8a8-4c13-ba27-d65509f12369.lovable.app,https://your-production-domain.com
OPENAI_API_KEY=your_real_key
PULSE_DATABASE_URL=your_postgres_pgvector_url
NBA_LLM_MODEL=gpt-5-mini
EVENT_TAXONOMY_MODEL=gpt-5.1
EVENT_RUNTIME_FALLBACK_MODEL=gpt-5-mini
VOC_REASONING_MODEL=gpt-5.1
OPENAI_TRANSCRIPTION_MODEL=gpt-4o-transcribe
```

5. After deployment, verify:

```text
https://your-render-service.onrender.com/api/health
https://your-render-service.onrender.com/api/profile
https://your-render-service.onrender.com/api/get-data
```

## Lovable

Use your deployed backend base URL:

```text
https://your-render-service.onrender.com
```

Lovable should call:

```text
GET /api/profile
GET /api/get-data
POST /api/login
POST /api/behavioral-state
```
