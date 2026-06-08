from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from behavioral_state_engine.agent import BehavioralStateEngine

from .config import get_cors_origins
from .schemas import (
    APIMessage,
    BehavioralStateRequest,
    DashboardData,
    LoginRequest,
    LoginResponse,
    ProfileResponse,
)


app = FastAPI(
    title="Pulse AI API",
    version="0.1.0",
    description="REST API for the Pulse AI decisioning frontend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)


@app.get("/api/health", response_model=APIMessage)
def health():
    return {"status": "ok", "message": "Pulse AI API is running"}


@app.post("/api/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required.")

    return {
        "access_token": "demo-pulse-token",
        "token_type": "bearer",
        "user": {
            "email": payload.email,
            "role": "lifecycle_pm",
            "workspace": "Pulse AI Demo",
        },
    }


@app.get("/api/get-data", response_model=DashboardData)
def get_data():
    return {
        "metrics": {
            "incremental_revenue": 418000,
            "suppression_safety": 0.93,
            "budget_leakage": 71000,
            "communication_reduction": 0.22,
        },
        "evidence": [
            {
                "title": "Suppression protected revenue in high-fatigue users",
                "detail": "Holdout users generated 4.1% less revenue than Pulse-suppressed users.",
                "value": 184000,
                "severity": "positive",
            },
            {
                "title": "Onboarding step 3 is over-sending",
                "detail": "Push plus WhatsApp overlap creates 2.8 contacts in 24h for 31% of new users.",
                "value": 22000,
                "severity": "warning",
            },
        ],
        "journey_diagnostics": [
            {
                "journey_step": "Onboarding step 3",
                "segment": "Activated, no order",
                "send_pressure": 0.86,
                "incremental_value": 0.22,
                "fatigue_lift": 0.71,
                "recommended_action": "Suppress WhatsApp if push was ignored in last 12h.",
            },
            {
                "journey_step": "Cart reminder",
                "segment": "High intent",
                "send_pressure": 0.64,
                "incremental_value": 0.68,
                "fatigue_lift": 0.37,
                "recommended_action": "Send only when trust score is above 0.55.",
            },
        ],
        "user_decisions": [
            {
                "user_id": "A",
                "state_label": "high_intent_high_fatigue",
                "recommended_action": "suppress",
                "confidence": 0.87,
                "counterfactuals": {
                    "suppress": 18.28,
                    "send_product_recommendation": 14.22,
                    "send_content": 5.31,
                },
            },
            {
                "user_id": "B",
                "state_label": "low_trust_high_fatigue",
                "recommended_action": "service_recovery",
                "confidence": 0.82,
                "counterfactuals": {
                    "service_recovery": 22.4,
                    "suppress": 17.1,
                    "send_purchase_nudge": 4.8,
                },
            },
        ],
    }


@app.get("/api/profile", response_model=ProfileResponse)
def profile():
    return {
        "user": {
            "id": "pm-demo",
            "name": "Lifecycle PM",
            "email": "pm@pulse.ai",
            "role": "lifecycle_pm",
        },
        "workspace": {
            "id": "pulse-demo",
            "name": "Pulse AI Demo",
            "connected_platform": "Braze",
            "business_goal": "maximize_revenue",
        },
        "permissions": [
            "view_dashboard",
            "review_decisions",
            "simulate_suppression",
            "export_evidence",
        ],
    }


@app.post("/api/behavioral-state")
def behavioral_state(payload: BehavioralStateRequest):
    engine = BehavioralStateEngine()
    return _dump_model(
        engine.run(
            event_input=payload.event_input,
            voc_input=payload.voc_input,
            crm_input=payload.crm_input,
        )
    )


def _dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
