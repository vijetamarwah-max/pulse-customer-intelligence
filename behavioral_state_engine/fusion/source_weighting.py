from ..config import CRM_WEIGHT, EVENT_AGENT_WEIGHT, VOC_AGENT_WEIGHT


class SourceWeighting:
    def get_weights(self):
        return {
            "event_agent": EVENT_AGENT_WEIGHT,
            "voc_agent": VOC_AGENT_WEIGHT,
            "crm_context": CRM_WEIGHT,
        }
