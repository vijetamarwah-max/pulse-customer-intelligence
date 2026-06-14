import os
from contextlib import contextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from behavioral_state_engine.agent import BehavioralStateEngine

from .config import get_cors_origins
from .demo_manual_event_stream import DEMO_MANUAL_EVENT_STREAM
from .schemas import (
    ActionCentreResponse,
    APIMessage,
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
    allow_origin_regex=r"https://.*\.lovable\.app",
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

    computed = _build_default_demo_dashboard()
    return {
        "metrics": computed["metrics"],
        "evidence": computed["evidence"],
        "journey_diagnostics": computed["journey_diagnostics"],
        "user_decisions": computed["user_decisions"],
        "data_mode": "demo",
        "connection_status": {
            **computed["connection_status"],
            "connected": False,
            "message": "Demo payload loaded. Process editable enterprise data to switch this workspace to live mode.",
        },
        "action_centre": computed["action_centre"],
    }


@app.post(
    "/api/enterprise-data",
    response_model=EnterpriseDataIngestionResponse,
)
def ingest_enterprise_data(payload: Dict[str, Any]):
    return _ingest_enterprise_payload(_normalize_enterprise_payload(payload))


def _ingest_enterprise_payload(payload: EnterpriseDataIngestionRequest):
    payload_dict = _dump_model(payload)
    with _runtime_llm_mode(enabled=bool(payload_dict.pop("runtime_llm_enabled", False))):
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


DEMO_WORKSPACE_IDS = {"default", "flipster_ecommerce"}


def _build_default_demo_dashboard(workspace_id: str = "default") -> Dict[str, Any]:
    payload = _dump_model(EnterpriseDataIngestionRequest(**DEMO_MANUAL_EVENT_STREAM))
    payload["workspace_id"] = workspace_id
    if workspace_id == "flipster_ecommerce":
        payload["source_name"] = "manual_upload"
    with _runtime_llm_mode(enabled=False):
        return recommendation_service.build_action_centre(payload)


@app.get("/api/demo/manual-event-stream")
def demo_manual_event_stream():
    return DEMO_MANUAL_EVENT_STREAM


@app.get("/api/demo/enterprise-upload-sample")
def demo_enterprise_upload_sample():
    return _lovable_upload_sample(DEMO_MANUAL_EVENT_STREAM)


@app.post(
    "/api/demo/run-manual-event-stream",
    response_model=EnterpriseDataIngestionResponse,
)
def run_demo_manual_event_stream(payload: Dict[str, Any] | None = None):
    if payload and payload.get("users"):
        payload = _normalize_enterprise_payload(
            {
                "workspace_id": payload.get("workspace_id", "default"),
                "source_name": payload.get("source_name", "manual_demo_event_stream"),
                "business_goal": payload.get("business_goal", "increase_revenue"),
                "constraints": payload.get("constraints", {}),
                "users": payload["users"],
                "historical_outcomes": payload.get("historical_outcomes"),
            }
        )
    else:
        payload = EnterpriseDataIngestionRequest(**DEMO_MANUAL_EVENT_STREAM)
    return _ingest_enterprise_payload(payload)


@app.get("/api/test-data/ecommerce-scenarios")
def ecommerce_scenarios():
    return ECOMMERCE_SYNTHETIC_TEST_PAYLOAD


@app.post(
    "/api/test-data/run-ecommerce-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_ecommerce_scenarios():
    payload = EnterpriseDataIngestionRequest(**ECOMMERCE_SYNTHETIC_TEST_PAYLOAD)
    return _ingest_enterprise_payload(payload)


@app.get("/api/test-data/lifecycle")
def lifecycle_scenarios():
    return DEMO_MANUAL_EVENT_STREAM


@app.post(
    "/api/test-data/run-lifecycle",
    response_model=EnterpriseDataIngestionResponse,
)
def run_lifecycle_scenarios():
    payload = EnterpriseDataIngestionRequest(**DEMO_MANUAL_EVENT_STREAM)
    return _ingest_enterprise_payload(payload)


@app.get("/api/test-data/ecommerce-comprehensive-scenarios")
def ecommerce_comprehensive_scenarios():
    return COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD


@app.post(
    "/api/test-data/run-ecommerce-comprehensive-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_ecommerce_comprehensive_scenarios():
    payload = EnterpriseDataIngestionRequest(**COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD)
    return _ingest_enterprise_payload(payload)


@app.get("/api/test-data/nba-conflict-scenarios")
def nba_conflict_scenarios():
    return NBA_CONFLICT_SCENARIO_PAYLOAD


@app.post(
    "/api/test-data/run-nba-conflict-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_nba_conflict_scenarios():
    payload = EnterpriseDataIngestionRequest(**NBA_CONFLICT_SCENARIO_PAYLOAD)
    return _ingest_enterprise_payload(payload)


@app.get("/api/test-data/mixed-signal-scenarios")
def mixed_signal_scenarios():
    return MIXED_SIGNAL_SCENARIO_PAYLOAD


@app.post(
    "/api/test-data/run-mixed-signal-scenarios",
    response_model=EnterpriseDataIngestionResponse,
)
def run_mixed_signal_scenarios():
    payload = EnterpriseDataIngestionRequest(**MIXED_SIGNAL_SCENARIO_PAYLOAD)
    return _ingest_enterprise_payload(payload)


@app.get("/api/action-centre", response_model=ActionCentreResponse)
def action_centre(workspace_id: str = "default"):
    workspace = workspace_store.get(workspace_id)
    if workspace_id in DEMO_WORKSPACE_IDS and _is_stale_demo_workspace(workspace):
        computed = _build_default_demo_dashboard(workspace_id)
        return _action_centre_response(computed)

    if workspace:
        computed = workspace["computed"]
        return _action_centre_response(computed)

    if workspace_id in DEMO_WORKSPACE_IDS:
        computed = _build_default_demo_dashboard(workspace_id)
        return _action_centre_response(computed)

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="No enterprise data has been ingested for this workspace yet.",
        )

    computed = workspace["computed"]
    return _action_centre_response(computed)


def _action_centre_response(computed: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "workspace_id": computed["workspace_id"],
        "data_mode": computed["data_mode"],
        "connection_status": computed["connection_status"],
        "recommendations": computed["recommendations"],
        "metrics": computed["metrics"],
        "processing_trace": computed["processing_trace"],
        "action_centre": computed["action_centre"],
    }


def _is_stale_demo_workspace(workspace) -> bool:
    if not workspace:
        return False

    payload = workspace.get("payload", {})
    source_name = payload.get("source_name")
    workspace_id = payload.get("workspace_id")
    users = payload.get("users", [])
    if workspace_id not in DEMO_WORKSPACE_IDS:
        return False
    if len(users) != 5:
        return False
    if source_name not in {"manual_upload", "manual_demo_event_stream", "manual_5_user_event_stream_demo"}:
        return False

    metrics = workspace.get("computed", {}).get("metrics", {})
    return float(metrics.get("average_confidence", 0.0)) < 0.75


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
def behavioral_state(payload: Dict[str, Any]):
    engine = BehavioralStateEngine()
    normalized = _normalize_behavioral_state_payload(payload)
    return _dump_model(
        engine.run(
            event_input=normalized["event_input"],
            voc_input=normalized["voc_input"],
            crm_input=normalized["crm_input"],
        )
    )


def _normalize_enterprise_payload(payload: Dict[str, Any]) -> EnterpriseDataIngestionRequest:
    """Accept Pulse-native payloads and Lovable/manual upload payloads.

    Pulse-native shape:
    {"workspace_id": "...", "source_name": "...", "users": [...]}

    Lovable upload shape seen in production:
    {"workspace": "...", "source": "...", "data": {"workspace": "...", "users": [...]}}
    """
    if "users" in payload:
        return EnterpriseDataIngestionRequest(**payload)

    nested_data = payload.get("data") or {}
    nested_users = nested_data.get("users") or []
    normalized_users = [_normalize_user_record(user) for user in nested_users]
    workspace_name = (
        payload.get("workspace_id")
        or payload.get("workspace")
        or nested_data.get("workspace")
        or "default"
    )

    normalized = {
        "workspace_id": _workspace_id(workspace_name),
        "source_name": payload.get("source_name") or payload.get("source") or "manual_upload",
        "business_goal": payload.get("business_goal") or nested_data.get("business_goal") or "increase_revenue",
        "constraints": payload.get("constraints") or nested_data.get("constraints") or {},
        "users": normalized_users,
        "historical_outcomes": payload.get("historical_outcomes") or nested_data.get("historical_outcomes"),
    }
    return EnterpriseDataIngestionRequest(**normalized)


def _normalize_behavioral_state_payload(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Accept backend-native and frontend-friendly behavioral state payloads.

    Native shape:
    {"event_input": {...}, "voc_input": {...}, "crm_input": {...}}

    Frontend aliases:
    {"event": {...}, "voc": {...}, "crm": {...}}
    {"event_understanding": {...}, "voice_of_customer": {...}, "crm_context": {...}}
    """
    event_input = (
        payload.get("event_input")
        or payload.get("event")
        or payload.get("event_understanding")
        or payload.get("event_agent")
    )
    voc_input = (
        payload.get("voc_input")
        or payload.get("voc")
        or payload.get("voice_of_customer")
        or payload.get("voc_agent")
    )
    crm_input = (
        payload.get("crm_input")
        or payload.get("crm")
        or payload.get("crm_context")
        or payload.get("profile")
    )

    if not event_input or not voc_input or not crm_input:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Behavioral state requires event, VoC, and CRM inputs.",
                "accepted_shapes": [
                    {"event_input": {}, "voc_input": {}, "crm_input": {}},
                    {"event": {}, "voc": {}, "crm": {}},
                    {"event_understanding": {}, "voice_of_customer": {}, "crm_context": {}},
                ],
            },
        )

    event_input = _normalize_event_input(event_input)
    voc_input = _normalize_voc_input(voc_input, event_input["user_id"])
    crm_input = _normalize_crm_input(crm_input, event_input["user_id"])

    return {
        "event_input": event_input,
        "voc_input": voc_input,
        "crm_input": crm_input,
    }


def _normalize_event_input(event_input: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "user_id": event_input.get("user_id", "unknown_user"),
        "intent_signals": event_input.get("intent_signals", event_input.get("signals", {})),
        "behavioral_tags": event_input.get("behavioral_tags", event_input.get("tags", [])),
        "confidence": event_input.get("confidence", 0.7),
    }


def _normalize_voc_input(voc_input: Dict[str, Any], fallback_user_id: str) -> Dict[str, Any]:
    return {
        "user_id": voc_input.get("user_id", fallback_user_id),
        "signals": voc_input.get("signals", {}),
        "behavioral_tags": voc_input.get("behavioral_tags", voc_input.get("tags", [])),
        "confidence": voc_input.get("confidence", 0.7),
    }


def _normalize_crm_input(crm_input: Dict[str, Any], fallback_user_id: str) -> Dict[str, Any]:
    crm_context = crm_input.get("crm_context")
    if crm_context is None:
        crm_context = {
            key: value
            for key, value in crm_input.items()
            if key not in {"user_id", "confidence", "behavioral_tags", "tags"}
        }

    return {
        "user_id": crm_input.get("user_id", fallback_user_id),
        "crm_context": crm_context,
    }


def _normalize_user_record(user: Dict[str, Any]) -> Dict[str, Any]:
    traits = user.get("traits") or user.get("crm_context") or {}
    events = user.get("events") or {}
    comms = user.get("comms") or user.get("comms_history") or []
    event_names = _event_names(events)

    return {
        "user_id": user["user_id"],
        "scenario": user.get("scenario") or user.get("label"),
        "events": {
            "raw_events": event_names,
            "event_stream": _event_stream(events),
        },
        "comms_history": [_normalize_comm_record(comm) for comm in comms],
        "crm_context": _normalize_traits(traits),
        "user_state": {
            **(user.get("user_state") or {}),
            "events_7d": len(event_names),
            "messages_7d": len(comms),
        },
        "constraints": user.get("constraints") or {},
    }


def _event_names(events: Any) -> list:
    if isinstance(events, dict):
        if "raw_events" in events:
            return events["raw_events"]
        if "event_stream" in events:
            return [event.get("event_name") for event in events["event_stream"]]
        return []

    return [
        event.get("event_name") or event.get("type") or event.get("name")
        for event in events
        if event.get("event_name") or event.get("type") or event.get("name")
    ]


def _event_stream(events: Any) -> list:
    if isinstance(events, dict):
        return events.get("event_stream") or []

    normalized = []
    for index, event in enumerate(events):
        event_name = event.get("event_name") or event.get("type") or event.get("name")
        if not event_name:
            continue
        properties = {
            key: value
            for key, value in event.items()
            if key not in {"event_name", "type", "name", "ts", "timestamp", "source", "channel", "device"}
        }
        normalized.append(
            {
                "event_id": event.get("event_id") or f"manual_evt_{index + 1:02d}",
                "event_name": event_name,
                "timestamp": event.get("timestamp") or event.get("ts"),
                "source": event.get("source") or "manual_upload",
                "channel": event.get("channel") or "web",
                "device": event.get("device"),
                "properties": properties,
            }
        )
    return normalized


def _normalize_comm_record(comm: Dict[str, Any]) -> Dict[str, Any]:
    channel = comm.get("channel", "communication")
    message = comm.get("message") or comm.get("body") or comm.get("text")
    if not message:
        opened = comm.get("opened")
        clicked = comm.get("clicked")
        engagement = "opened" if opened else "ignored"
        if clicked:
            engagement = "clicked"
        message = f"{channel} communication was {engagement}."

    return {
        "channel": channel,
        "direction": comm.get("direction") or "outbound",
        "message": message,
        "sent_at": comm.get("sent_at") or comm.get("timestamp") or comm.get("ts"),
        "opened": comm.get("opened"),
        "clicked": comm.get("clicked"),
        "sentiment_hint": comm.get("sentiment_hint"),
    }


def _normalize_traits(traits: Dict[str, Any]) -> Dict[str, Any]:
    tier = traits.get("customer_tier") or traits.get("tier") or "unknown"
    return {
        **traits,
        "customer_tier": tier,
        "ltv_segment": traits.get("ltv_segment") or _ltv_segment_for_tier(tier),
        "geography": traits.get("geography") or traits.get("city"),
        "total_orders": traits.get("total_orders", 0),
        "average_order_value": traits.get("average_order_value", 0),
        "last_purchase_days_ago": traits.get("last_purchase_days_ago", 30),
        "preferred_channel": traits.get("preferred_channel") or "push",
        "timezone": traits.get("timezone") or "Asia/Kolkata",
        "support_status": traits.get("support_status") or "none",
    }


def _ltv_segment_for_tier(tier: str) -> str:
    if tier in {"loyal", "gold", "platinum", "vip"}:
        return "high_value"
    if tier in {"silver", "returning"}:
        return "mid_value"
    if tier in {"bronze", "new"}:
        return "low_value"
    return "unknown"


def _workspace_id(workspace_name: str) -> str:
    clean = str(workspace_name).strip().lower().replace(" ", "_")
    return clean or "default"


def _lovable_upload_sample(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "workspace": "Flipster Ecommerce",
        "source": "manual_upload",
        "data": {
            "workspace": "Pulse AI Demo",
            "business_goal": payload.get("business_goal", "increase_revenue"),
            "constraints": payload.get("constraints", {}),
            "historical_outcomes": payload.get("historical_outcomes", []),
            "users": [_to_lovable_user(user) for user in payload.get("users", [])],
        },
    }


def _to_lovable_user(user: Dict[str, Any]) -> Dict[str, Any]:
    crm_context = user.get("crm_context", {})
    return {
        "user_id": user["user_id"],
        "label": user.get("scenario"),
        "traits": {
            "tier": crm_context.get("customer_tier"),
            "ltv_segment": crm_context.get("ltv_segment"),
            "city": crm_context.get("geography", "Mumbai"),
            "preferred_channel": crm_context.get("preferred_channel"),
            "support_status": crm_context.get("support_status"),
            "nps": crm_context.get("nps"),
            "total_orders": crm_context.get("total_orders"),
            "average_order_value": crm_context.get("average_order_value"),
            "last_purchase_days_ago": crm_context.get("last_purchase_days_ago"),
        },
        "events": [
            {
                "type": event.get("event_name"),
                "ts": event.get("timestamp"),
                **(event.get("properties") or {}),
            }
            for event in user.get("events", {}).get("event_stream", [])
        ],
        "comms": [
            {
                "channel": comm.get("channel"),
                "direction": comm.get("direction"),
                "ts": comm.get("sent_at"),
                "message": comm.get("message"),
                "opened": comm.get("opened"),
                "clicked": comm.get("clicked"),
                "sentiment_hint": comm.get("sentiment_hint"),
            }
            for comm in user.get("comms_history", [])
        ],
        "user_state": user.get("user_state", {}),
    }


@contextmanager
def _runtime_llm_mode(enabled: bool):
    previous = os.environ.get("PULSE_DISABLE_RUNTIME_LLM")
    if not enabled:
        os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("PULSE_DISABLE_RUNTIME_LLM", None)
        else:
            os.environ["PULSE_DISABLE_RUNTIME_LLM"] = previous


def _dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
