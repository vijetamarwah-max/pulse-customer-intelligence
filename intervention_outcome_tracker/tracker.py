from .attribution.attribution_engine import AttributionEngine
from .dashboard.dashboard_api import DashboardAPI
from .evidence.decision_evidence_engine import DecisionEvidenceEngine
from .experiments.lift_calculator import LiftCalculator
from .ingestion.event_mapper import EventMapper
from .ingestion.execution_listener import ExecutionListener
from .ingestion.outcome_listener import OutcomeListener
from .ledger.decision_ledger import DecisionLedger
from .metrics.business_metrics import BusinessMetrics
from .metrics.suppression_metrics import SuppressionMetrics
from .metrics.win_rate_metrics import WinRateMetrics
from .schema import DecisionOutcomeRecord, TrackerSummary


class InterventionOutcomeTracker:
    def __init__(self):
        self.execution_listener = ExecutionListener()
        self.outcome_listener = OutcomeListener()
        self.event_mapper = EventMapper()
        self.attribution = AttributionEngine()
        self.lift = LiftCalculator()
        self.ledger = DecisionLedger()
        self.business_metrics = BusinessMetrics()
        self.suppression_metrics = SuppressionMetrics()
        self.win_rate_metrics = WinRateMetrics()
        self.evidence_engine = DecisionEvidenceEngine()
        self.dashboard = DashboardAPI()

    def run(self, recommendations, outcomes):
        outcomes_by_user = self.event_mapper.by_user_id(outcomes)
        control_revenue = self._control_revenue(recommendations, outcomes_by_user)
        wins = 0
        pulse_total = 0

        for recommendation in recommendations:
            execution = self.execution_listener.capture(recommendation)
            outcome = self.outcome_listener.capture(
                outcomes_by_user.get(execution["user_id"], {})
            )

            attributed = self.attribution.attribute(outcome)
            revenue = float(outcome.get("revenue", 0.0))
            is_pulse = execution.get("group") == "PULSE"
            incremental_value = (
                self.lift.calculate(revenue, control_revenue)
                if is_pulse and attributed
                else 0.0
            )

            if is_pulse:
                pulse_total += 1
                if revenue > control_revenue:
                    wins += 1

            record = DecisionOutcomeRecord(
                user_id=execution["user_id"],
                state_label=execution.get("state_label", "unknown"),
                recommendation=execution["recommendation"],
                channel=execution.get("channel", "unknown"),
                send_time=execution.get("send_time", "unknown"),
                group=execution.get("group", "PULSE"),
                executed=bool(execution.get("executed", True)),
                attributed=attributed,
                outcome=outcome,
                incremental_value=incremental_value,
            )

            self.ledger.write(self._dump(record))

        records = self.ledger.all()
        summary = {
            "incremental_revenue": self.business_metrics.incremental_revenue(records),
            "decision_win_rate": self.win_rate_metrics.calculate(wins, pulse_total),
            "suppressed_messages": self.suppression_metrics.total_suppressed(records),
            "total_records": len(records),
        }
        summary["evidence"] = self.evidence_engine.build(records, summary)

        return TrackerSummary(**self.dashboard.build_response(summary))

    def _control_revenue(self, recommendations, outcomes_by_user):
        control_revenues = []

        for recommendation in recommendations:
            if recommendation.get("group") != "CONTROL":
                continue

            outcome = outcomes_by_user.get(recommendation["user_id"], {})
            control_revenues.append(float(outcome.get("revenue", 0.0)))

        if not control_revenues:
            return 0.0

        return sum(control_revenues) / len(control_revenues)

    def _dump(self, model):
        if hasattr(model, "model_dump"):
            return model.model_dump()
        return model.dict()
