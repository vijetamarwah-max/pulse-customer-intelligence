import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from behavioral_memory.agent import BehavioralMemoryOutcomeEstimator


def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    historical = json.loads(
        (base_dir / "historical_outcomes.json").read_text(encoding="utf-8")
    )
    users = json.loads((base_dir / "current_users.json").read_text(encoding="utf-8"))

    estimator = BehavioralMemoryOutcomeEstimator(top_k=3)

    for user in users:
        result = estimator.run(
            user_id=user["user_id"],
            state_vector=user["state_vector"],
            historical_records=historical,
        )

        print("\n====================")
        print(json.dumps(dump_model(result), indent=2))


if __name__ == "__main__":
    main()
