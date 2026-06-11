import json
import os

from voice_of_customer_agent.agent import VoiceOfCustomerAgent


NOISY_KANNADA_TRANSCRIPT = """
[background traffic, overlapping voice]
Naanu three times follow-up madidini. Refund issue innu resolve agilla.
Customer support yaaru sariyagi help madilla. Tumba frustrating ide.
Nimage helbeku, ivattu resolve agbeku illa andre next month service cancel madthini.
[noise] order amount block aagide, trust swalpa kammi aagide.
"""


def main() -> None:
    os.environ.pop("PULSE_DISABLE_RUNTIME_LLM", None)
    agent = VoiceOfCustomerAgent()
    result = agent.run(
        user_id="VOC-KN-001",
        input_type="text",
        raw_input=NOISY_KANNADA_TRANSCRIPT,
    )
    payload = result.model_dump() if hasattr(result, "model_dump") else result.dict()

    semantic_confidence = _semantic_confidence(payload)
    print(
        json.dumps(
            {
                "test_type": "noisy_kannada_transcript_semantic_eval",
                "asr_limitation": "No raw audio file was provided, so this evaluates semantic robustness from a noisy transcript hypothesis, not transcription WER.",
                "transcript": NOISY_KANNADA_TRANSCRIPT.strip(),
                "voc_output": payload,
                "semantic_adequacy_confidence": semantic_confidence,
                "assessment": _assessment(payload, semantic_confidence),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def _semantic_confidence(payload):
    signals = payload["signals"]
    strong_negative = max(
        signals["frustration_signal"],
        signals["urgency_signal"],
        signals["retention_risk"],
        signals["escalation_risk"],
    )
    low_trust = 1 - signals["trust_signal"]
    return round(min(payload["confidence"], (strong_negative * 0.7) + (low_trust * 0.3)), 3)


def _assessment(payload, confidence):
    signals = payload["signals"]
    if confidence >= 0.8 and signals["frustration_signal"] > 0.65:
        return "Good enough for semantic meaning, sentiment, and tone extraction."
    if confidence >= 0.6:
        return "Usable, but route to observe/manual review before automation."
    return "Insufficient confidence; request clearer audio or human review."


if __name__ == "__main__":
    main()
