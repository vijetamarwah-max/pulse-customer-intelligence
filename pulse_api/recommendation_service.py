import json
from pathlib import Path
from typing import Dict, List

from behavioral_memory.agent import BehavioralMemoryOutcomeEstimator
from behavioral_state_engine.agent import BehavioralStateEngine
from event_understanding_agent.agent import EventUnderstandingAgent
from nba_engine.agent import NBADecisionEngine
from voice_of_customer_agent.agent import VoiceOfCustomerAgent


class RecommendationService:
    def __init__(self) -> None:
        self.event_agent = EventUnderstandingAgent()
        self.voc_agent = VoiceOfCustomerAgent()
        self.state_engine = BehavioralStateEngine()
        self.outcome_estimator = BehavioralMemoryOutcomeEstimator(top_k=3)
        self.nba_engine = NBADecisionEngine()

    def build_action_centre(self, payload: Dict) -> Dict:
        historical_outcomes = payload.get("historical_outcomes") or self._default_history()
        goal = payload.get("business_goal", "increase_revenue")
        constraints = payload.get("constraints") or self._default_constraints()

        recommendations = []
        for user in payload.get("users", []):
            recommendation = self._recommend_for_user(
                user=user,
                historical_outcomes=historical_outcomes,
                goal=goal,
                constraints=constraints,
            )
            recommendations.append(recommendation)

        return {
            "workspace_id": payload.get("workspace_id", "default"),
            "data_mode": "enterprise_connected",
            "connection_status": self._connection_status(payload, recommendations),
            "recommendations": recommendations,
            "processing_trace": [
                item["processing_trace"] for item in recommendations
            ],
            "metrics": self._metrics(recommendations),
            "evidence": self._evidence(recommendations),
            "journey_diagnostics": self._journey_diagnostics(recommendations),
            "user_decisions": [
                {
                    "user_id": item["user_id"],
                    "state_label": item["behavioral_state"]["state_label"],
                    "recommended_action": item["recommended_action"],
                    "confidence": item["confidence"],
                    "counterfactuals": item["counterfactuals"],
                }
                for item in recommendations
            ],
        }

    def _recommend_for_user(
        self,
        user: Dict,
        historical_outcomes: List[Dict],
        goal: str,
        constraints: Dict,
    ) -> Dict:
        user_id = user["user_id"]
        event_result = self.event_agent.run(
            user_id=user_id,
            events=user.get("events", {}),
            user_state=user.get("user_state", {}),
        )
        event_input = {
            "user_id": user_id,
            "intent_signals": {
                "purchase_intent": event_result.purchase_intent,
                "exploration_intent": event_result.exploration_intent,
                "churn_risk": event_result.churn_risk,
            },
            "behavioral_tags": event_result.behavioral_tags,
            "confidence": event_result.confidence,
        }

        voc_result = self._build_voc(user)
        voc_input = {
            "user_id": user_id,
            "signals": self._dump(voc_result.signals),
            "behavioral_tags": voc_result.behavioral_tags,
            "confidence": voc_result.confidence,
        }

        crm_input = {
            "user_id": user_id,
            "crm_context": user.get("crm_context", {}),
        }

        behavioral_state = self.state_engine.run(event_input, voc_input, crm_input)
        behavioral_state_dict = self._dump(behavioral_state)
        state_vector = behavioral_state_dict["state_vector"]
        outcome_estimate = self.outcome_estimator.run(
            user_id=user_id,
            state_vector=state_vector,
            historical_records=historical_outcomes,
        )
        outcome_dict = self._dump(outcome_estimate)

        nba = self.nba_engine.run(
            user_id=user_id,
            behavioral_state=state_vector,
            predicted_outcomes=outcome_dict["predicted_outcomes"],
            goal=goal,
            constraints=constraints,
            behavioral_confidence=behavioral_state_dict["confidence"],
            outcome_confidence=outcome_dict["confidence"],
        )
        nba_dict = self._dump(nba)

        return {
            "user_id": user_id,
            "recommended_action": nba_dict["recommended_action"],
            "confidence": nba_dict["confidence"],
            "expected_incremental_value": nba_dict["expected_incremental_value"],
            "ranked_actions": nba_dict["ranked_actions"],
            "counterfactuals": nba_dict["counterfactuals"],
            "reasoning": nba_dict["reasoning"],
            "llm_reasoning": nba_dict["llm_reasoning"],
            "behavioral_state": behavioral_state_dict,
            "event_signals": event_input,
            "voc_signals": voc_input,
            "predicted_outcomes": outcome_dict,
            "processing_trace": self._processing_trace(
                user=user,
                event_input=event_input,
                voc_input=voc_input,
                crm_input=crm_input,
                behavioral_state=behavioral_state_dict,
                outcome_dict=outcome_dict,
                nba_dict=nba_dict,
            ),
        }

    def _build_voc(self, user: Dict):
        comms_text = self._comms_to_text(user.get("comms_history", []))
        if not comms_text:
            comms_text = "No recent customer communication history is available."

        return self.voc_agent.run(
            user_id=user["user_id"],
            input_type="text",
            raw_input=comms_text,
        )

    def _comms_to_text(self, comms_history: List[Dict]) -> str:
        messages = []
        for item in comms_history:
            if isinstance(item, str):
                messages.append(item)
                continue

            text = item.get("message") or item.get("body") or item.get("text")
            if text:
                channel = item.get("channel", "communication")
                messages.append(f"{channel}: {text}")

        return "\n".join(messages)

    def _connection_status(self, payload: Dict, recommendations: List[Dict]) -> Dict:
        return {
            "connected": True,
            "source_name": payload.get("source_name", "manual_upload"),
            "users_ingested": len(payload.get("users", [])),
            "recommendations_ready": len(recommendations),
            "uses_enterprise_events": True,
            "uses_comms_history": any(
                bool(user.get("comms_history")) for user in payload.get("users", [])
            ),
            "uses_crm_context": any(
                bool(user.get("crm_context")) for user in payload.get("users", [])
            ),
        }

    def _metrics(self, recommendations: List[Dict]) -> Dict:
        total_value = sum(
            item.get("expected_incremental_value", 0.0) for item in recommendations
        )
        suppression_count = sum(
            1 for item in recommendations if item["recommended_action"] == "suppress"
        )
        service_recovery_count = sum(
            1
            for item in recommendations
            if item["recommended_action"] == "service_recovery"
        )
        avg_confidence = (
            sum(item["confidence"] for item in recommendations) / len(recommendations)
            if recommendations
            else 0.0
        )

        return {
            "users_scored": len(recommendations),
            "expected_incremental_value": round(total_value, 2),
            "suppression_recommendations": suppression_count,
            "service_recovery_recommendations": service_recovery_count,
            "average_confidence": round(avg_confidence, 3),
        }

    def _evidence(self, recommendations: List[Dict]) -> List[Dict]:
        high_fatigue = [
            item
            for item in recommendations
            if item["behavioral_state"]["state_vector"]["communication_fatigue"] > 0.65
        ]
        low_trust = [
            item
            for item in recommendations
            if item["behavioral_state"]["state_vector"]["trust_level"] < 0.5
        ]

        return [
            {
                "title": "Enterprise data is driving live recommendations",
                "detail": f"{len(recommendations)} users scored through Event, VoC, CRM, outcome, and NBA layers.",
                "value": len(recommendations),
                "severity": "positive",
            },
            {
                "title": "High-fatigue users need intervention control",
                "detail": f"{len(high_fatigue)} users have communication fatigue above 0.65.",
                "value": len(high_fatigue),
                "severity": "warning",
            },
            {
                "title": "Low-trust users should not receive generic conversion nudges",
                "detail": f"{len(low_trust)} users show trust below 0.50 from customer communication signals.",
                "value": len(low_trust),
                "severity": "warning",
            },
        ]

    def _journey_diagnostics(self, recommendations: List[Dict]) -> List[Dict]:
        diagnostics = []
        for item in recommendations:
            state = item["behavioral_state"]["state_vector"]
            diagnostics.append(
                {
                    "journey_step": f"User {item['user_id']} next intervention",
                    "segment": item["behavioral_state"]["state_label"],
                    "send_pressure": round(state["communication_fatigue"], 3),
                    "incremental_value": item["expected_incremental_value"],
                    "fatigue_lift": round(state["communication_fatigue"], 3),
                    "recommended_action": item["recommended_action"],
                }
            )

        return diagnostics

    def _processing_trace(
        self,
        user: Dict,
        event_input: Dict,
        voc_input: Dict,
        crm_input: Dict,
        behavioral_state: Dict,
        outcome_dict: Dict,
        nba_dict: Dict,
    ) -> Dict:
        raw_events = user.get("events", {}).get("raw_events", [])
        comms_history = user.get("comms_history", [])

        return {
            "user_id": user["user_id"],
            "steps": [
                {
                    "name": "Manual Event Stream",
                    "status": "processed",
                    "summary": f"{len(raw_events)} raw events received from manual demo upload.",
                    "data": {
                        "raw_events": raw_events,
                        "user_state": user.get("user_state", {}),
                    },
                },
                {
                    "name": "Event Understanding Agent",
                    "status": "processed",
                    "summary": "Raw events converted into purchase, exploration, and churn intent signals.",
                    "data": event_input,
                },
                {
                    "name": "Voice of Customer Agent",
                    "status": "processed",
                    "summary": f"{len(comms_history)} communication records converted into trust, urgency, retention, and fatigue signals.",
                    "data": voc_input,
                },
                {
                    "name": "CRM Context",
                    "status": "processed",
                    "summary": "Enterprise-owned customer facts joined without inference.",
                    "data": crm_input,
                },
                {
                    "name": "Behavioral State Engine",
                    "status": "processed",
                    "summary": f"Unified state label: {behavioral_state['state_label']}.",
                    "data": behavioral_state,
                },
                {
                    "name": "Outcome Estimator",
                    "status": "processed",
                    "summary": "Similar behavioral memories used to predict action outcomes.",
                    "data": outcome_dict,
                },
                {
                    "name": "NBA Decision Engine",
                    "status": "processed",
                    "summary": f"Recommended action: {nba_dict['recommended_action']}.",
                    "data": {
                        "recommended_action": nba_dict["recommended_action"],
                        "confidence": nba_dict["confidence"],
                        "expected_incremental_value": nba_dict[
                            "expected_incremental_value"
                        ],
                        "counterfactuals": nba_dict["counterfactuals"],
                        "llm_reasoning": nba_dict["llm_reasoning"],
                    },
                },
            ],
        }

    def _default_constraints(self) -> Dict:
        return {
            "discounts_allowed": False,
            "send_allowed": True,
            "suppress_if_high_fatigue": False,
        }

    def _default_history(self) -> List[Dict]:
        path = (
            Path(__file__).resolve().parents[1]
            / "behavioral_memory"
            / "examples"
            / "historical_outcomes.json"
        )
        return json.loads(path.read_text(encoding="utf-8"))

    def _dump(self, value):
        if hasattr(value, "model_dump"):
            return value.model_dump()
        if hasattr(value, "dict"):
            return value.dict()
        return value
