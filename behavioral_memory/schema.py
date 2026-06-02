from typing import Dict

from pydantic import BaseModel, Field


class PredictedOutcome(BaseModel):
    revenue: float
    engagement: float = Field(ge=0.0, le=1.0)
    retention: float = Field(ge=0.0, le=1.0)
    conversion_probability: float = Field(ge=0.0, le=1.0)
    sample_size: int = Field(ge=0)
    average_similarity: float = Field(ge=0.0, le=1.0)


class OutcomeEstimate(BaseModel):
    user_id: str
    predicted_outcomes: Dict[str, PredictedOutcome]
    confidence: float = Field(ge=0.0, le=1.0)
