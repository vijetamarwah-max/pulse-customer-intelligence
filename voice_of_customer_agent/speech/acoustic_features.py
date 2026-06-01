from typing import Dict


class AcousticFeatureExtractor:
    def extract(self, speech_data: Dict[str, object]) -> Dict[str, object]:
        return {
            "tone_signal": speech_data.get("tone", "neutral"),
            "speech_intensity": float(speech_data.get("speech_intensity", 0.0)),
            "pause_density": float(speech_data.get("pause_density", 0.0)),
        }
