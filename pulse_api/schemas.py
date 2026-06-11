from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, str]


class DashboardData(BaseModel):
    metrics: Dict[str, object]
    evidence: List[Dict[str, object]]
    journey_diagnostics: List[Dict[str, object]]
    user_decisions: List[Dict[str, object]]
    data_mode: str = "demo"
    connection_status: Optional[Dict[str, object]] = None
    action_centre: Optional[Dict[str, object]] = None


class ProfileResponse(BaseModel):
    user: Dict[str, object]
    workspace: Dict[str, object]
    permissions: List[str]


class BehavioralStateRequest(BaseModel):
    event_input: Dict
    voc_input: Dict
    crm_input: Dict


class EnterpriseUserRecord(BaseModel):
    user_id: str
    scenario: Optional[str] = None
    events: Dict[str, object]
    comms_history: List[Dict[str, object]] = Field(default_factory=list)
    crm_context: Dict[str, object] = Field(default_factory=dict)
    user_state: Dict[str, object] = Field(default_factory=dict)
    constraints: Dict[str, object] = Field(default_factory=dict)


class EnterpriseDataIngestionRequest(BaseModel):
    workspace_id: str = "default"
    source_name: str = "manual_upload"
    business_goal: str = "increase_revenue"
    constraints: Dict[str, object] = Field(default_factory=dict)
    users: List[EnterpriseUserRecord]
    historical_outcomes: Optional[List[Dict[str, object]]] = None


class EnterpriseDataIngestionResponse(BaseModel):
    status: str
    workspace_id: str
    source_name: str
    users_ingested: int
    action_centre_url: str


class ActionCentreResponse(BaseModel):
    workspace_id: str
    data_mode: str
    connection_status: Dict[str, object]
    recommendations: List[Dict[str, object]]
    metrics: Dict[str, object]
    processing_trace: List[Dict[str, object]] = Field(default_factory=list)
    action_centre: Dict[str, object] = Field(default_factory=dict)


class APIMessage(BaseModel):
    status: str
    message: Optional[str] = None
