import argparse
import json
import os
from pathlib import Path

from pulse_vector_store.behavioral_memory_pgvector import BehavioralMemoryPGVectorStore


def main() -> None:
    args = _parse_args()
    _load_local_env()

    if not os.getenv("PULSE_DATABASE_URL"):
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "PULSE_DATABASE_URL is not set.",
                    "input_path": args.input_path,
                },
                indent=2,
            )
        )
        return

    records = _read_jsonl(Path(args.input_path))
    try:
        store = BehavioralMemoryPGVectorStore()
        store.initialize()

        for record in records:
            store.upsert_memory(
                memory_id=record["memory_id"],
                user_id=record["user_id"],
                action=record["action"],
                state_vector=record["state_vector"],
                outcome=record["outcome"],
                embedding=record["embedding"],
                metadata=record["metadata"],
            )

        result = {
            "status": "upserted",
            "records": len(records),
            "input_path": args.input_path,
        }
    except Exception as exc:
        result = {
            "status": "failed",
            "records_ready": len(records),
            "input_path": args.input_path,
            "error": str(exc),
        }

    print(json.dumps(result, indent=2))


def _read_jsonl(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _load_local_env() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
            continue

        key, value = clean_line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if value:
            os.environ.setdefault(key.strip(), value)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    return parser.parse_args()


if __name__ == "__main__":
    main()
