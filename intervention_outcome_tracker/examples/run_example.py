import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from intervention_outcome_tracker.tracker import InterventionOutcomeTracker


def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main():
    base_dir = Path(__file__).resolve().parent
    recommendations = json.loads(
        (base_dir / "recommendations.json").read_text(encoding="utf-8")
    )
    outcomes = json.loads((base_dir / "outcomes.json").read_text(encoding="utf-8"))

    tracker = InterventionOutcomeTracker()
    summary = tracker.run(recommendations, outcomes)

    print(json.dumps(dump_model(summary), indent=2))


if __name__ == "__main__":
    main()
