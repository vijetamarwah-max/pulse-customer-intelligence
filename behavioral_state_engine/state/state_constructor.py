from typing import Dict

from ..schema import BehavioralStateOutput


class StateConstructor:
    def construct(
        self,
        user_id: str,
        scored_state: Dict[str, float],
        state_label: str,
        confidence: float,
        source_weights: Dict[str, float],
    ) -> BehavioralStateOutput:
        return BehavioralStateOutput(
            user_id=user_id,
            state_vector=scored_state,
            state_label=state_label,
            confidence=confidence,
            source_weights=source_weights,
        )
