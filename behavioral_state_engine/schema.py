from typing import Dict

from pydantic import BaseModel, Field


class BehavioralStateVector(BaseModel):
    purchase_readiness: float = Field(ge=0.0, le=1.0)
    engagement_probability: float = Field(ge=0.0, le=1.0)
    communication_fatigue: float = Field(ge=0.0, le=1.0)
    retention_risk: float = Field(ge=0.0, le=1.0)
    trust_level: float = Field(ge=0.0, le=1.0)
    discount_sensitivity: float = Field(ge=0.0, le=1.0)
    brand_affinity: float = Field(ge=0.0, le=1.0)
    intervention_receptiveness: float = Field(ge=0.0, le=1.0)
    complaint_retention_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    inactivity_retention_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    cart_intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    checkout_intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    wishlist_intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    browse_intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    coupon_intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    recent_conversion_signal: float = Field(default=0.0, ge=0.0, le=1.0)
    service_blocker_intensity: float = Field(default=0.0, ge=0.0, le=1.0)


class BehavioralStateOutput(BaseModel):
    user_id: str
    state_vector: BehavioralStateVector
    state_label: str
    confidence: float = Field(ge=0.0, le=1.0)
    source_weights: Dict[str, float]
