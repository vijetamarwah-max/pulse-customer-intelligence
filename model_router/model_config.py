MODEL_CONFIG = {
    "event_taxonomy_classification": {
        "model": "gpt-5.1",
        "reasoning_effort": "medium",
        "usage": "Classify enterprise event names into semantic taxonomy mappings.",
    },
    "event_runtime_fallback": {
        "model": "gpt-5-mini",
        "reasoning_effort": "low",
        "usage": "Resolve low-confidence or unknown runtime event interpretation only.",
    },
    "voc_reasoning": {
        "model": "gpt-5.1",
        "reasoning_effort": "medium",
        "usage": "Infer sentiment, urgency, trust, retention risk, and escalation risk.",
    },
    "nba_explanation": {
        "model": "gpt-5-mini",
        "reasoning_effort": "none",
        "usage": "Explain an already-computed NBA recommendation and counterfactuals.",
    },
    "audio_transcription": {
        "model": "gpt-4o-transcribe",
        "reasoning_effort": "none",
        "usage": "Transcribe customer audio before VoC reasoning.",
    },
}
