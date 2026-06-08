from typing import Dict, List, Optional

from pydantic import BaseModel


class UserTrainingRecord(BaseModel):
    user_id: str
    event_stream: List[Dict]
    communication_history: List[Dict]
    crm_context: Dict = {}
    behavioral_state: Dict
    action: str
    outcome: Dict
    occurred_at: Optional[str] = None
