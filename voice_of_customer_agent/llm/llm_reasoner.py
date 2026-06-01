from typing import Dict

from ..config import DEFAULT_CONFIDENCE


class VOCLLMReasoner:
    def infer(
        self,
        transcript: str,
        embedding_scores: Dict[str, float],
        acoustic_features: Dict[str, object],
    ) -> Dict[str, object]:
        frustration = embedding_scores.get("frustration_signal", 0.0)
        urgency = embedding_scores.get("urgency_signal", 0.0)
        retention = embedding_scores.get("retention_risk", 0.0)
        trust = 1.0 - embedding_scores.get("trust_erosion_signal", 0.0)

        speech_intensity = float(acoustic_features.get("speech_intensity", 0.0))
        pause_density = float(acoustic_features.get("pause_density", 0.0))
        escalation = frustration * 0.45 + urgency * 0.2 + speech_intensity * 0.35
        engagement = self._estimate_engagement(transcript, pause_density)

        tags = []
        if frustration > 0.7:
            tags.append("emotionally_negative")
        if escalation > 0.65:
            tags.append("high_attention_required")
        if urgency > 0.7:
            tags.append("time_sensitive")
        if trust < 0.4:
            tags.append("trust_erosion")
        if retention > 0.7:
            tags.append("retention_risk")

        confidence = min(
            0.95,
            max(DEFAULT_CONFIDENCE, (frustration + urgency + retention + engagement) / 4),
        )

        return {
            "signals": {
                "frustration_signal": frustration,
                "urgency_signal": urgency,
                "trust_signal": trust,
                "retention_risk": retention,
                "engagement_signal": engagement,
                "escalation_risk": escalation,
            },
            "behavioral_tags": tags,
            "confidence": confidence,
            "explanation": (
                "Customer communication was converted into behavioral signals "
                "using similarity scores, semantic reasoning, and acoustic context."
            ),
        }

    def _estimate_engagement(self, transcript: str, pause_density: float) -> float:
        word_count = len(transcript.split())
        text_engagement = min(1.0, word_count / 80)
        pause_penalty = min(0.25, pause_density * 0.25)
        return max(0.0, min(1.0, 0.45 + text_engagement - pause_penalty))
