from pulse_vector_store import BehavioralMemoryPGVectorStore

from .real_data_loader import RealDataLoader
from .training_record_builder import TrainingRecordBuilder


class MemoryTrainingPipeline:
    def __init__(self, store=None) -> None:
        self._load_local_env()
        self.loader = RealDataLoader()
        self.builder = TrainingRecordBuilder()
        self.store = store or BehavioralMemoryPGVectorStore()

    def run(self, training_file_path):
        raw_records = self.loader.load_json(training_file_path)
        self.store.initialize()

        inserted = 0
        for raw_record in raw_records:
            memory_record = self.builder.build(raw_record)
            self.store.upsert_memory(**memory_record)
            inserted += 1

        return {"inserted": inserted}

    def _load_local_env(self):
        import os
        from pathlib import Path

        env_path = Path(__file__).resolve().parents[1] / ".env"
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            if value and "your_" not in value:
                os.environ.setdefault(key.strip(), value)
