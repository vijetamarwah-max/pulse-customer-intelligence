from typing import Dict, List, Optional

from pydantic import BaseModel


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


class ProfileResponse(BaseModel):
    user: Dict[str, object]
    workspace: Dict[str, object]
    permissions: List[str]


class BehavioralStateRequest(BaseModel):
    event_input: Dict
    voc_input: Dict
    crm_input: Dict


class APIMessage(BaseModel):
    status: str
    message: Optional[str] = None
