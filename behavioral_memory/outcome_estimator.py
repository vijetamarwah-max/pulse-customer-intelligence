from collections import defaultdict
from typing import Dict, List, Tuple


class OutcomeEstimator:
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

        return predictions
