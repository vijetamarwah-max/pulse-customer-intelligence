from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class EventUnderstandingContract(BaseModel):
    user_id: str
    intent_signals: Dict[str, float]
    behavioral_tags: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    generated_at: Optional[datetime] = None
