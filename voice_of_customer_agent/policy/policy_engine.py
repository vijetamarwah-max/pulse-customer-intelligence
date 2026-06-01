from typing import Dict


class PolicyEngine:
    def apply(self, llm_output: Dict[str, object]) -> Dict[str, object]:
        signals = llm_output["signals"]
        tags = list(llm_output["behavioral_tags"])

        if signals["frustration_signal"] > 0.85:
            tags.append("manual_review_required")

        if signals["retention_risk"] > 0.90:
            tags.append("retention_intervention_required")

        if signals["escalation_risk"] > 0.80:
            tags.append("escalation_watch")

        if signals["trust_signal"] < 0.35:
            tags.append("trust_rebuild_needed")

        llm_output["behavioral_tags"] = sorted(set(tags))
        return llm_output
