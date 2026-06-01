import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from behavioral_state_engine.agent import BehavioralStateEngine


def dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main() -> None:
    engine = BehavioralStateEngine()
    base_dir = Path(__file__).resolve().parent

    event_input = json.loads((base_dir / "sample_event.json").read_text(encoding="utf-8"))
    voc_input = json.loads((base_dir / "sample_voc.json").read_text(encoding="utf-8"))
    crm_input = json.loads((base_dir / "sample_crm.json").read_text(encoding="utf-8"))

    result = engine.run(event_input, voc_input, crm_input)

    print(json.dumps(dump_model(result), indent=2))


if __name__ == "__main__":
    main()
