from typing import Any, Dict

from .contracts.crm_contract import CRMContract
from .contracts.event_contract import EventUnderstandingContract
from .contracts.voc_contract import VOCContract
from .features.feature_builder import FeatureBuilder
from .features.feature_normalizer import FeatureNormalizer
from .fusion.signal_fusion import SignalFusionEngine
from .fusion.source_weighting import SourceWeighting
from .models.confidence_calibrator import ConfidenceCalibrator
from .models.scoring_models import BehavioralScoringModels
from .schema import BehavioralStateOutput
from .state.state_constructor import StateConstructor
from .state.state_labels import StateLabeler


class BehavioralStateEngine:
    def __init__(self) -> None:
        self.fusion_engine = SignalFusionEngine()
        self.weighting = SourceWeighting()
        self.feature_builder = FeatureBuilder()
        self.normalizer = FeatureNormalizer()
        self.scoring = BehavioralScoringModels()
        self.confidence = ConfidenceCalibrator()
        self.labeler = StateLabeler()
        self.constructor = StateConstructor()

    def run(
        self,
        event_input: Dict[str, Any],
        voc_input: Dict[str, Any],
        crm_input: Dict[str, Any],
    ) -> BehavioralStateOutput:
        event_contract = EventUnderstandingContract(**event_input)
        voc_contract = VOCContract(**voc_input)
        crm_contract = CRMContract(**crm_input)

        if len({event_contract.user_id, voc_contract.user_id, crm_contract.user_id}) != 1:
            raise ValueError("All Behavioral State Engine inputs must use the same user_id.")

        fused_state = self.fusion_engine.fuse(
            event_contract.intent_signals,
            voc_contract.signals,
            crm_contract.crm_context,
        )

        engineered_features = self.feature_builder.build(fused_state)
        normalized_state = self.normalizer.normalize(fused_state)
        normalized_features = self.normalizer.normalize(engineered_features)
        scored_state = self.scoring.score(normalized_state, normalized_features)

        confidence = self.confidence.calibrate(
            event_contract.confidence,
            voc_contract.confidence,
        )

        state_label = self.labeler.label(scored_state)

        return self.constructor.construct(
            user_id=event_contract.user_id,
            scored_state=scored_state,
            state_label=state_label,
            confidence=confidence,
            source_weights=self.weighting.get_weights(),
        )
