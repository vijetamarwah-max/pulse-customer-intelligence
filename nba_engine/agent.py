from .candidates.candidate_generator import CandidateGenerator
from .delivery.delivery_planner import DeliveryPlanner
from .explanation.explanation_builder import ExplanationBuilder
from .explanation.llm_reasoning_builder import LLMReasoningBuilder
from .policy.business_goal_engine import BusinessGoalEngine
from .policy.constraints_engine import ConstraintsEngine
from .schema import NBARecommendation
from .scoring.action_ranker import ActionRanker
from .scoring.confidence_engine import ConfidenceEngine
from .scoring.value_calculator import ValueCalculator
from .selector.action_selector import ActionSelector


class NBADecisionEngine:
    def __init__(self) -> None:
        self.candidates = CandidateGenerator()
        self.constraints = ConstraintsEngine()
        self.goal_engine = BusinessGoalEngine()
        self.value_calculator = ValueCalculator()
        self.ranker = ActionRanker()
        self.confidence_engine = ConfidenceEngine()
        self.selector = ActionSelector()
        self.delivery_planner = DeliveryPlanner()
        self.explainer = ExplanationBuilder()
        self.llm_reasoner = LLMReasoningBuilder()

    def run(
        self,
        user_id,
        behavioral_state,
        predicted_outcomes,
        goal,
        constraints,
        behavioral_confidence,
        outcome_confidence,
        user_context=None,
    ) -> NBARecommendation:
        candidate_actions = self.candidates.generate()
        allowed_actions = self.constraints.apply(
            candidate_actions,
            constraints,
            behavioral_state=behavioral_state,
        )
        evaluated_constraints = self.constraints.evaluated_constraints()
        goal_weights = self.goal_engine.get_weights(goal)
        action_scores = self.value_calculator.calculate(
            predicted_outcomes,
            goal_weights,
            allowed_actions,
            behavioral_state=behavioral_state,
        )
        ranked_actions = self.ranker.rank(action_scores)
        selected_action = self.selector.select(ranked_actions)
        delivery_plan = self.delivery_planner.build(
            selected_action,
            behavioral_state,
            evaluated_constraints,
            user_context=user_context,
        )
        confidence = self.confidence_engine.compute(
            behavioral_confidence,
            outcome_confidence,
        )
        reasoning = self.explainer.build(selected_action, behavioral_state, goal)
        llm_reasoning = self.llm_reasoner.build(
            selected_action=selected_action,
            behavioral_state=behavioral_state,
            ranked_actions=ranked_actions,
            counterfactuals=ranked_actions,
            goal=goal,
        )

        return NBARecommendation(
            user_id=user_id,
            recommended_action=selected_action,
            confidence=confidence,
            expected_incremental_value=ranked_actions.get(selected_action, 0.0),
            ranked_actions=ranked_actions,
            counterfactuals=ranked_actions,
            delivery_plan=delivery_plan,
            reasoning=reasoning,
            llm_reasoning=llm_reasoning,
        )
