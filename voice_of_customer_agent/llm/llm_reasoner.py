import json
import os
from pathlib import Path
from typing import Dict

from model_router.routing_policy import ModelRoutingPolicy

from ..config import DEFAULT_CONFIDENCE
from ..config import VOC_REASONING_MODEL_USE_CASE
from .prompts import VOC_REASONING_SYSTEM_PROMPT


class VOCLLMReasoner:
    def __init__(self) -> None:
        self._load_local_env()
        self.model_router = ModelRoutingPolicy()
        self.model_use_case = VOC_REASONING_MODEL_USE_CASE
        self.model = self.model_router.model_for(self.model_use_case)

    def infer(
        self,
        transcript: str,
        embedding_scores: Dict[str, float],
        acoustic_features: Dict[str, object],
    ) -> Dict[str, object]:
        if self._usable_api_key():
            try:
                return self._infer_with_openai(
                    transcript,
                    embedding_scores,
                    acoustic_features,
                )
            except Exception:
                return self._infer_locally(
                    transcript,
                    embedding_scores,
                    acoustic_features,
                )

        return self._infer_locally(transcript, embedding_scores, acoustic_features)

    def _infer_locally(
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
            "model_route": {
                "use_case": self.model_use_case,
                "model": self.model_router.model_for(self.model_use_case),
                "reasoning_effort": self.model_router.reasoning_effort_for(
                    self.model_use_case
                ),
            },
        }

    def _infer_with_openai(
        self,
        transcript: str,
        embedding_scores: Dict[str, float],
        acoustic_features: Dict[str, object],
    ) -> Dict[str, object]:
        from openai import OpenAI

        model_route = {
            "use_case": self.model_use_case,
            "model": self.model,
            "reasoning_effort": self.model_router.reasoning_effort_for(
                self.model_use_case
            ),
        }
        payload = {
            "transcript": transcript,
            "embedding_scores": embedding_scores,
            "acoustic_features": acoustic_features,
            "model_route": model_route,
        }

        response = OpenAI(api_key=self._usable_api_key()).responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": VOC_REASONING_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, indent=2),
                },
            ],
            **self._reasoning_kwargs(),
        )

        result = json.loads(response.output_text)
        result["model_route"] = model_route
        return self._coerce_result(result)

    def _estimate_engagement(self, transcript: str, pause_density: float) -> float:
        word_count = len(transcript.split())
        text_engagement = min(1.0, word_count / 80)
        pause_penalty = min(0.25, pause_density * 0.25)
        return max(0.0, min(1.0, 0.45 + text_engagement - pause_penalty))

    def _coerce_result(self, result: Dict) -> Dict[str, object]:
        signals = result.get("signals", {})
        return {
            "signals": {
                "frustration_signal": self._bounded(
                    signals.get("frustration_signal", 0.0)
                ),
                "urgency_signal": self._bounded(signals.get("urgency_signal", 0.0)),
                "trust_signal": self._bounded(signals.get("trust_signal", 0.0)),
                "retention_risk": self._bounded(signals.get("retention_risk", 0.0)),
                "engagement_signal": self._bounded(
                    signals.get("engagement_signal", 0.0)
                ),
                "escalation_risk": self._bounded(
                    signals.get("escalation_risk", 0.0)
                ),
            },
            "behavioral_tags": list(result.get("behavioral_tags", [])),
            "confidence": self._bounded(result.get("confidence", DEFAULT_CONFIDENCE)),
            "explanation": str(result.get("explanation", "")),
            "model_route": result["model_route"],
        }

    def _reasoning_kwargs(self) -> Dict:
        effort = self.model_router.reasoning_effort_for(self.model_use_case)
        if effort == "none":
            return {}
        return {"reasoning": {"effort": effort}}

    def _usable_api_key(self):
        value = os.getenv("OPENAI_API_KEY")
        if not value or "your_" in value:
            return None
        return value

    def _bounded(self, value) -> float:
        return max(0.0, min(1.0, float(value)))

    def _load_local_env(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            if value and "your_" not in value:
                os.environ.setdefault(key.strip(), value)
