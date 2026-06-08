import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from training_data_pipeline.training_record_builder import TrainingRecordBuilder


def main():
    base_dir = Path(__file__).resolve().parent
    records = json.loads(
        (base_dir / "real_user_training_records.json").read_text(encoding="utf-8")
    )
    builder = TrainingRecordBuilder()

    built = [builder.build(record) for record in records]
    print(json.dumps(built, indent=2))


if __name__ == "__main__":
    main()
