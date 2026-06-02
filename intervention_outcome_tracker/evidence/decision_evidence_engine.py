class DecisionEvidenceEngine:
    def build(self, records, summary):
        evidence = []

        evidence.append(
            f"Pulse generated {summary['incremental_revenue']} incremental revenue "
            "against the control baseline."
        )

        evidence.append(
            f"Pulse decision win rate was {summary['decision_win_rate']} across "
            f"{summary['total_records']} tracked decisions."
        )

        if summary["suppressed_messages"]:
            evidence.append(
                f"Pulse suppressed {summary['suppressed_messages']} messages while "
                "still measuring downstream business outcomes."
            )

        attributed = len([record for record in records if record.get("attributed")])
        evidence.append(f"{attributed} outcomes were attributed to tracked decisions.")

        return evidence
