import json
from pathlib import Path
from typing import Dict, Iterable


class SemanticEventMapper:
    """Lookup-based semantic event mapper.

    LLMs should classify enterprise event types when the taxonomy is built or
    refreshed, not once per user. Runtime user scoring uses this deterministic
    mapping table.
    """

    def __init__(self, taxonomy_path=None):
        self.taxonomy_path = taxonomy_path or Path(__file__).with_name("event_taxonomy.json")
        self.taxonomy = self._load_taxonomy()

    def map_event(self, raw_event_name: str) -> str:
        return self.taxonomy.get(raw_event_name, "unknown")

    def summarize(self, raw_events: Iterable[str]) -> Dict[str, int]:
        summary = {
            "purchase_intent_events": 0,
            "exploration_intent_events": 0,
            "consideration_intent_events": 0,
            "churn_risk_events": 0,
            "conversion_events": 0,
            "unknown_events": 0,
        }

        for event_name in raw_events:
            semantic_type = self.map_event(event_name)
            key = f"{semantic_type}_events"
            if key in summary:
                summary[key] += 1
            else:
                summary["unknown_events"] += 1

        return summary

    def _load_taxonomy(self) -> Dict[str, str]:
        return json.loads(Path(self.taxonomy_path).read_text(encoding="utf-8"))
