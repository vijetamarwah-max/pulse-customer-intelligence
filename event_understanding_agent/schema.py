from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class IntentSignal(BaseModel):
    type: str
    strength: float = Field(ge=0.0, le=1.0)


class EventUnderstandingOutput(BaseModel):
    user_id: str
    purchase_intent: float = Field(ge=0.0, le=1.0)
    exploration_intent: float = Field(ge=0.0, le=1.0)
    churn_risk: float = Field(ge=0.0, le=1.0)
    behavioral_tags: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: Optional[str] = None
    signal_sources: Dict[str, float]
