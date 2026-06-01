from typing import Dict

from .embeddings.embedding_engine import VOCEmbeddingEngine
from .embeddings.similarity import SimilarityMatcher
from .llm.llm_reasoner import VOCLLMReasoner
from .policy.policy_engine import PolicyEngine
from .schema import VOCOutput
from .speech.acoustic_features import AcousticFeatureExtractor
from .speech.speech_processor import SpeechProcessor


class VoiceOfCustomerAgent:
    def __init__(self) -> None:
        self.speech_processor = SpeechProcessor()
        self.acoustic_extractor = AcousticFeatureExtractor()
        self.embedding_engine = VOCEmbeddingEngine()
        self.matcher = SimilarityMatcher()
        self.llm = VOCLLMReasoner()
        self.policy_engine = PolicyEngine()

    def build_embedding_vector(self, text: str):
        normalized_text = text.lower()

        frustration = int(
            any(
                phrase in normalized_text
                for phrase in [
                    "frustrating",
                    "disappointed",
                    "resolved",
                    "nobody helped",
                    "unacceptable",
                ]
            )
        )

        urgency = int(
            any(
                phrase in normalized_text
                for phrase in [
                    "urgent",
                    "immediately",
                    "as soon as possible",
                    "asap",
                ]
            )
        )

        retention = int(
            any(
                phrase in normalized_text
                for phrase in [
                    "cancel",
                    "leave",
                    "leaving",
                    "done with this service",
                    "thinking of leaving",
                ]
            )
        )

        return [frustration, urgency, retention]

    def run(self, user_id: str, input_type: str, raw_input: str) -> VOCOutput:
        if input_type == "audio":
            speech_data = self.speech_processor.process_audio(raw_input)
            transcript = str(speech_data["transcript"])
            acoustic_features = self.acoustic_extractor.extract(speech_data)
        else:
            transcript = raw_input
            acoustic_features = {
                "tone_signal": "text_only",
                "speech_intensity": 0.0,
                "pause_density": 0.0,
            }

        vector = self.build_embedding_vector(transcript)
        user_embedding = self.embedding_engine.embed(vector)
        embedding_scores = self.matcher.score(user_embedding, self.embedding_engine)
        llm_output = self.llm.infer(transcript, embedding_scores, acoustic_features)
        final_output = self.policy_engine.apply(llm_output)

        return VOCOutput(
            user_id=user_id,
            transcript=transcript,
            signals=final_output["signals"],
            behavioral_tags=final_output["behavioral_tags"],
            confidence=final_output["confidence"],
            signal_sources=embedding_scores,
            explanation=final_output["explanation"],
        )
