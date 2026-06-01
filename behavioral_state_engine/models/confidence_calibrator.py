from ..config import CRM_WEIGHT, DEFAULT_CRM_CONFIDENCE, EVENT_AGENT_WEIGHT, VOC_AGENT_WEIGHT


class ConfidenceCalibrator:
    def calibrate(
        self,
        event_confidence: float,
        voc_confidence: float,
        crm_confidence: float = DEFAULT_CRM_CONFIDENCE,
    ) -> float:
        weighted_confidence = (
            event_confidence * EVENT_AGENT_WEIGHT
            + voc_confidence * VOC_AGENT_WEIGHT
            + crm_confidence * CRM_WEIGHT
        )

        return round(min(max(weighted_confidence, 0.0), 1.0), 3)
