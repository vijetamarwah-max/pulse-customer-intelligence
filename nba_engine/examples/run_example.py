import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from nba_engine.agent import NBADecisionEngine


def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    behavioral_state = json.loads(
        (base_dir / "behavioral_state.json").read_text(encoding="utf-8")
    )
    predicted_outcomes = json.loads(
        (base_dir / "predicted_outcomes.json").read_text(encoding="utf-8")
    )
    goal = json.loads((base_dir / "goal.json").read_text(encoding="utf-8"))
    constraints = json.loads(
        (base_dir / "constraints.json").read_text(encoding="utf-8")
    )

    engine = NBADecisionEngine()
    result = engine.run(
        user_id=behavioral_state["user_id"],
        behavioral_state=behavioral_state["state_vector"],
        predicted_outcomes=predicted_outcomes,
        goal=goal["goal"],
        constraints=constraints,
        behavioral_confidence=behavioral_state["confidence"],
        outcome_confidence=0.86,
    )

    print(json.dumps(dump_model(result), indent=2))


if __name__ == "__main__":
    main()
