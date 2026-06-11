from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from behavioral_state_engine.agent import BehavioralStateEngine

from .config import get_cors_origins
from .demo_manual_event_stream import DEMO_MANUAL_EVENT_STREAM
from .schemas import (
    ActionCentreResponse,
    APIMessage,
    BehavioralStateRequest,
    DashboardData,
    EnterpriseDataIngestionRequest,
    EnterpriseDataIngestionResponse,
    LoginRequest,
    LoginResponse,
    ProfileResponse,
)
from .recommendation_service import RecommendationService
from .test_data.ecommerce_comprehensive import COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD
from .test_data.ecommerce_synthetic import ECOMMERCE_SYNTHETIC_TEST_PAYLOAD
from .test_data.mixed_signal_scenarios import MIXED_SIGNAL_SCENARIO_PAYLOAD
from .test_data.nba_conflict_scenarios import NBA_CONFLICT_SCENARIO_PAYLOAD
from .workspace_store import WorkspaceStore


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

workspace_store = WorkspaceStore()
recommendation_service = RecommendationService()


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
    workspace = workspace_store.get()
    if workspace:
        computed = workspace["computed"]
        return {
            "metrics": computed["metrics"],
            "evidence": computed["evidence"],
            "journey_diagnostics": computed["journey_diagnostics"],
            "user_decisions": computed["user_decisions"],
            "data_mode": computed["data_mode"],
            "connection_status": computed["connection_status"],
            "action_centre": computed["action_centre"],
        }

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
        "data_mode": "demo",
        "connection_status": {
            "connected": False,
            "source_name": None,
            "users_ingested": 0,
            "recommendations_ready": 0,
            "message": "Connect enterprise events, communication history, and CRM context to generate live Action Centre recommendations.",
        },
        "action_centre": None,
    }


@app.post(
    "/api/enterprise-data",
    response_model=EnterpriseDataIngestionResponse,
)
def ingest_enterprise_data(payload: EnterpriseDataIngestionRequest):
    payload_dict = _dump_model(payload)
    computed = recommendation_service.build_action_centre(payload_dict)
    workspace_store.save(
        workspace_id=payload.workspace_id,
        payload=payload_dict,
        computed=computed,
    )

    return {
        "status": "ok",
        "workspace_id": payload.workspace_id,
        "source_name": payload.source_name,
        "users_ingested": len(payload.users),
        "action_centre_url": "/api/action-centre",
    }


@app.get("/api/demo/manual-event-stream")
def demo_manual_event_stream():
    return DEMO_MANUAL_EVENT_STREAM


@app.post(
    "/api/demo/run-manual-event-stream",
    response_model=EnterpriseDataIngestionResponse,
)
def run_demo_manual_event_stream():
    payload = EnterpriseDataIngestionRequest(**DEMO_MANUAL_EVENT_STREAM)
    return ingest_enterprise_data(payload)


@app.get("/api/test-data/ecommerce-scenarios")
def ecommerce_scenarios():
    return ECOMMERCE_SYNTHETIC_TEST_PAYLOAD


@app.post(
    "/api/test-data/run-ecommerce-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_ecommerce_scenarios():
    payload = EnterpriseDataIngestionRequest(**ECOMMERCE_SYNTHETIC_TEST_PAYLOAD)
    return ingest_enterprise_data(payload)


@app.get("/api/test-data/ecommerce-comprehensive-scenarios")
def ecommerce_comprehensive_scenarios():
    return COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD


@app.post(
    "/api/test-data/run-ecommerce-comprehensive-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_ecommerce_comprehensive_scenarios():
    payload = EnterpriseDataIngestionRequest(**COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD)
    return ingest_enterprise_data(payload)


@app.get("/api/test-data/nba-conflict-scenarios")
def nba_conflict_scenarios():
    return NBA_CONFLICT_SCENARIO_PAYLOAD


@app.post(
    "/api/test-data/run-nba-conflict-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_nba_conflict_scenarios():
    payload = EnterpriseDataIngestionRequest(**NBA_CONFLICT_SCENARIO_PAYLOAD)
    return ingest_enterprise_data(payload)


@app.get("/api/test-data/mixed-signal-scenarios")
def mixed_signal_scenarios():
    return MIXED_SIGNAL_SCENARIO_PAYLOAD


@app.post(
    "/api/test-data/run-mixed-signal-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_mixed_signal_scenarios():
    payload = EnterpriseDataIngestionRequest(**MIXED_SIGNAL_SCENARIO_PAYLOAD)
    return ingest_enterprise_data(payload)


@app.get("/api/action-centre", response_model=ActionCentreResponse)
def action_centre(workspace_id: str = "default"):
    workspace = workspace_store.get(workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="No enterprise data has been ingested for this workspace yet.",
        )

    computed = workspace["computed"]
    return {
        "workspace_id": computed["workspace_id"],
        "data_mode": computed["data_mode"],
        "connection_status": computed["connection_status"],
        "recommendations": computed["recommendations"],
        "metrics": computed["metrics"],
        "processing_trace": computed["processing_trace"],
        "action_centre": computed["action_centre"],
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
