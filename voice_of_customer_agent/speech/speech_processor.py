import os
from pathlib import Path
from typing import Dict

from model_router.routing_policy import ModelRoutingPolicy

from ..config import OPENAI_TRANSCRIPTION_MODEL_USE_CASE


class SpeechProcessor:
    def __init__(self) -> None:
        self._load_local_env()
        self.model_router = ModelRoutingPolicy()

    def process_audio(self, file_path: str) -> Dict[str, object]:
        """Transcribe audio and return normalized speech metadata.

        The OpenAI transcription endpoint supports m4a, mp3, mp4, mpeg, mpga,
        wav, and webm. Acoustic values remain lightweight placeholders until a
        dedicated prosody/tone model is plugged in.
        """

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Set it before running real audio "
                "transcription."
            )

        audio_path = Path(file_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The openai package is not installed. Run: "
                "python -m pip install -r voice_of_customer_agent/requirements.txt"
            ) from exc

        client = OpenAI()
        with audio_path.open("rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=self.model_router.model_for(OPENAI_TRANSCRIPTION_MODEL_USE_CASE),
                file=audio_file,
                response_format="text",
            )

        transcript = getattr(transcription, "text", transcription)
        if not isinstance(transcript, str):
            transcript = str(transcript)

        return {
            "source_file": str(audio_path),
            "transcript": transcript.strip(),
            "tone": "transcribed",
            "speech_intensity": 0.0,
            "pause_density": 0.0,
        }

    def _load_local_env(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
