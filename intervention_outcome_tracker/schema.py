from typing import Dict, List

from pydantic import BaseModel


class DecisionOutcomeRecord(BaseModel):
    user_id: str
    state_label: str = "unknown"
    recommendation: str
    channel: str = "unknown"
    send_time: str = "unknown"
    group: str
    executed: bool
    attributed: bool
    outcome: Dict
    incremental_value: float


class TrackerSummary(BaseModel):
    incremental_revenue: float
    decision_win_rate: float
    suppressed_messages: int
    total_records: int
    evidence: List[str]
