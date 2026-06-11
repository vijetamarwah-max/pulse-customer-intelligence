from collections import defaultdict
from typing import Dict, List, Tuple


class OutcomeEstimator:
    CANDIDATE_ACTIONS = [
        "suppress",
        "send_product_recommendation",
        "send_content",
        "send_cart_reminder",
        "send_retention_message",
        "send_discount_offer",
        "service_recovery",
    ]

    def estimate(self, similar_records: List[Tuple[float, Dict]]) -> Dict[str, Dict[str, float]]:
        action_stats = defaultdict(list)

        for similarity, record in similar_records:
            action_stats[record["action"]].append((similarity, record))

        predictions = {}

        for action, rows in action_stats.items():
            total_weight = sum(similarity for similarity, _ in rows) or 1.0
            weighted_revenue = sum(
                similarity * float(record.get("revenue", 0.0))
                for similarity, record in rows
            )
            weighted_engagement = sum(
                similarity * float(record.get("engagement", 0.0))
                for similarity, record in rows
            )
            weighted_retention = sum(
                similarity * float(record.get("retention", 0.0))
                for similarity, record in rows
            )
            weighted_conversion = sum(
                similarity * float(bool(record.get("converted", False)))
                for similarity, record in rows
            )

            predictions[action] = {
                "revenue": round(weighted_revenue / total_weight, 3),
                "engagement": round(weighted_engagement / total_weight, 3),
                "retention": round(weighted_retention / total_weight, 3),
                "conversion_probability": round(weighted_conversion / total_weight, 3),
                "sample_size": len(rows),
                "average_similarity": round(
                    sum(similarity for similarity, _ in rows) / len(rows),
                    3,
                ),
            }

        state_vector = self._nearest_state(similar_records)
        for action in self.CANDIDATE_ACTIONS:
            if action not in predictions:
                predictions[action] = self._cold_start_prior(action, state_vector)

        return predictions

    def _nearest_state(self, similar_records: List[Tuple[float, Dict]]) -> Dict:
        if not similar_records:
            return {}

        return similar_records[0][1].get("state_vector", {})

    def _cold_start_prior(self, action: str, state: Dict) -> Dict[str, float]:
        purchase = float(state.get("purchase_readiness", 0.0))
        fatigue = float(state.get("communication_fatigue", 0.0))
        trust = float(state.get("trust_level", 0.0))
        retention = float(state.get("retention_risk", 0.0))
        engagement = float(state.get("engagement_probability", 0.0))

        priors = {
            "suppress": {
                "revenue": 35 + fatigue * 80 + (1 - trust) * 35,
                "engagement": 0.08 + max(0.0, 0.18 - engagement * 0.1),
                "retention": 0.45 + fatigue * 0.28 + retention * 0.25,
                "conversion_probability": 0.05,
            },
            "send_product_recommendation": {
                "revenue": 55 + purchase * 115 + trust * 35,
                "engagement": 0.25 + engagement * 0.45,
                "retention": 0.35 + trust * 0.2,
                "conversion_probability": 0.2 + purchase * 0.55,
            },
            "send_content": {
                "revenue": 30 + engagement * 60 + trust * 20,
                "engagement": 0.45 + engagement * 0.42,
                "retention": 0.42 + trust * 0.22,
                "conversion_probability": 0.15 + engagement * 0.25,
            },
            "send_cart_reminder": {
                "revenue": 45 + purchase * 125,
                "engagement": 0.28 + purchase * 0.35,
                "retention": 0.35 + trust * 0.18,
                "conversion_probability": 0.18 + purchase * 0.58,
            },
            "send_retention_message": {
                "revenue": 40 + retention * 85 + trust * 20,
                "engagement": 0.25 + retention * 0.28,
                "retention": 0.50 + retention * 0.36 + (1 - trust) * 0.12,
                "conversion_probability": 0.08 + retention * 0.22,
            },
            "send_discount_offer": {
                "revenue": 50 + purchase * 95 + trust * 20,
                "engagement": 0.32 + purchase * 0.32,
                "retention": 0.32 + trust * 0.16,
                "conversion_probability": 0.18 + purchase * 0.5,
            },
            "service_recovery": {
                "revenue": 45 + retention * 75 + (1 - trust) * 65 + fatigue * 45,
                "engagement": 0.35 + fatigue * 0.22 + retention * 0.18,
                "retention": 0.62 + retention * 0.25 + (1 - trust) * 0.18,
                "conversion_probability": 0.05 + purchase * 0.18,
            },
        }

        prior = priors[action]
        return {
            "revenue": round(prior["revenue"], 3),
            "engagement": round(min(max(prior["engagement"], 0.0), 1.0), 3),
            "retention": round(min(max(prior["retention"], 0.0), 1.0), 3),
            "conversion_probability": round(
                min(max(prior["conversion_probability"], 0.0), 1.0),
                3,
            ),
            "sample_size": 0,
            "average_similarity": 0.0,
            "source": "cold_start_prior",
        }
