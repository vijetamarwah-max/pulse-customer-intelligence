import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from voice_of_customer_agent.agent import VoiceOfCustomerAgent


def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main() -> None:
    agent = VoiceOfCustomerAgent()
    base_dir = Path(__file__).resolve().parent

    chat_text = (base_dir / "sample_chat.txt").read_text(encoding="utf-8")

    chat_result = agent.run(
        user_id="U100",
        input_type="chat",
        raw_input=chat_text,
    )

    print("\nCHAT RESULT:\n")
    print(json.dumps(dump_model(chat_result), indent=2))

    audio_result = agent.run(
        user_id="U101",
        input_type="audio",
        raw_input=str(base_dir / "sample_call.m4a"),
    )

    print("\nAUDIO RESULT:\n")
    print(json.dumps(dump_model(audio_result), indent=2))


if __name__ == "__main__":
    main()
