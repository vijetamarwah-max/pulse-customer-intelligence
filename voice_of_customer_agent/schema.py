from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class VOCSignals(BaseModel):
    frustration_signal: float = Field(ge=0.0, le=1.0)
    urgency_signal: float = Field(ge=0.0, le=1.0)
    trust_signal: float = Field(ge=0.0, le=1.0)
    retention_risk: float = Field(ge=0.0, le=1.0)
    engagement_signal: float = Field(ge=0.0, le=1.0)
    escalation_risk: float = Field(ge=0.0, le=1.0)


class VOCOutput(BaseModel):
    user_id: str
    transcript: Optional[str] = None
    signals: VOCSignals
    behavioral_tags: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
    signal_sources: Dict[str, float]
