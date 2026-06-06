from .config import CRITICAL_REALTIME_EVENTS, EVENT_UNDERSTANDING_BATCH_INTERVAL_HOURS


class EventProcessingPolicy:
    def should_process_realtime(self, event_name: str) -> bool:
        return event_name in CRITICAL_REALTIME_EVENTS

    def batch_interval_hours(self) -> int:
        return EVENT_UNDERSTANDING_BATCH_INTERVAL_HOURS
