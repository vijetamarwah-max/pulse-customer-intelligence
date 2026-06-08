import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from training_data_pipeline import MemoryTrainingPipeline


def main():
    base_dir = Path(__file__).resolve().parent
    result = MemoryTrainingPipeline().run(base_dir / "real_user_training_records.json")
    print(result)


if __name__ == "__main__":
    main()
