from typing import Dict, List

from pydantic import BaseModel, Field


class NBARecommendation(BaseModel):
    user_id: str
    recommended_action: str
    confidence: float = Field(ge=0.0, le=1.0)
    expected_incremental_value: float
    ranked_actions: Dict[str, float]
    counterfactuals: Dict[str, float]
    delivery_plan: Dict[str, object] = {}
    reasoning: List[str]
    llm_reasoning: str
