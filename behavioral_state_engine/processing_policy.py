from .config import CRITICAL_REALTIME_EVENTS, DEFAULT_BATCH_REFRESH_HOURS


class BehavioralStateProcessingPolicy:
    """Hybrid processing policy for cost-efficient state refreshes."""

    def should_refresh_realtime(self, event_name: str) -> bool:
        return event_name in CRITICAL_REALTIME_EVENTS

    def batch_refresh_hours(self) -> int:
        return DEFAULT_BATCH_REFRESH_HOURS
