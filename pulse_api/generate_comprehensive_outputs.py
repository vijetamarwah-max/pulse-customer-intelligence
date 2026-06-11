import argparse
import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from behavioral_memory.embedding_generator import EmbeddingGenerator
from model_router.routing_policy import ModelRoutingPolicy
from pulse_api.recommendation_service import RecommendationService
from pulse_api.test_data.ecommerce_comprehensive import (
    COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD,
)


def main() -> None:
    args = _parse_args()
    _load_local_env()

    if args.disable_runtime_llm:
        os.environ["PULSE_DISABLE_RUNTIME_LLM"] = "true"
    else:
        os.environ.pop("PULSE_DISABLE_RUNTIME_LLM", None)

    payload = deepcopy(COMPREHENSIVE_ECOMMERCE_TEST_PAYLOAD)
    payload["workspace_id"] = args.workspace_id
    payload["users"] = payload["users"][args.offset : args.offset + args.limit]

    if args.force_event_llm:
        for user in payload["users"]:
            user.setdefault("events", {})["force_llm_reasoning"] = True

    service = RecommendationService()
    output = service.build_action_centre(payload)
    run_id = _run_id()
    output["run_metadata"] = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime_llm_enabled": not args.disable_runtime_llm,
        "force_event_llm": args.force_event_llm,
        "users_processed": len(payload["users"]),
        "offset": args.offset,
        "model_routes": ModelRoutingPolicy().describe(),
        "workspace_id": args.workspace_id,
    }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{run_id}_action_centre_outputs.json"
    vector_path = output_dir / f"{run_id}_vector_memory_records.jsonl"
    summary_path = output_dir / f"{run_id}_summary.json"

    _write_json(output_path, output)
    vector_records = _build_vector_records(output["recommendations"], run_id)
    _write_jsonl(vector_path, vector_records)

    pgvector_status = _maybe_upsert_pgvector(
        vector_records,
        enabled=args.upsert_pgvector,
    )

    summary = {
        "run_id": run_id,
        "output_path": str(output_path),
        "vector_records_path": str(vector_path),
        "users_processed": len(payload["users"]),
        "offset": args.offset,
        "recommendations": len(output["recommendations"]),
        "state_labels": sorted(
            {
                item["behavioral_state"]["state_label"]
                for item in output["recommendations"]
            }
        ),
        "recommended_actions": sorted(
            {item["recommended_action"] for item in output["recommendations"]}
        ),
        "pgvector": pgvector_status,
    }
    _write_json(summary_path, summary)
    print(json.dumps(summary, indent=2))


def _build_vector_records(recommendations: List[Dict], run_id: str) -> List[Dict]:
    embedder = EmbeddingGenerator()
    records = []
    for item in recommendations:
        state_vector = item["behavioral_state"]["state_vector"]
        action = item["recommended_action"]
        records.append(
            {
                "memory_id": f"{run_id}:{item['user_id']}:{action}",
                "user_id": item["user_id"],
                "scenario": item.get("scenario"),
                "action": action,
                "state_vector": state_vector,
                "embedding": embedder.generate(state_vector),
                "outcome": {
                "outcome_type": "llm_generated_synthetic_prediction",
                "expected_incremental_value": item["expected_incremental_value"],
                "expected_value_per_comms": item.get("delivery_plan", {}).get("should_send")
                and item["expected_incremental_value"]
                or 0.0,
                "confidence": item["confidence"],
                "confidence_band": _confidence_band(item["confidence"]),
                "ranked_actions": item["ranked_actions"],
                    "counterfactuals": item["counterfactuals"],
                    "predicted_outcomes": item["predicted_outcomes"],
                },
                "metadata": {
                    "run_id": run_id,
                    "state_label": item["behavioral_state"]["state_label"],
                    "source": "comprehensive_synthetic_ecommerce_llm_run",
                    "llm_reasoning": item["llm_reasoning"],
                },
            }
        )

    return records


def _confidence_band(confidence):
    if confidence >= 0.8:
        return "auto_approve"
    if confidence >= 0.6:
        return "observe"
    return "reject"


def _maybe_upsert_pgvector(records: List[Dict], enabled: bool) -> Dict:
    if not enabled:
        return {
            "enabled": False,
            "status": "skipped",
        }

    if not os.getenv("PULSE_DATABASE_URL"):
        return {
            "enabled": True,
            "status": "skipped_missing_pulse_database_url",
        }

    try:
        from pulse_vector_store.behavioral_memory_pgvector import (
            BehavioralMemoryPGVectorStore,
        )

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

        return {
            "enabled": True,
            "status": "upserted",
            "records": len(records),
        }
    except Exception as exc:
        return {
            "enabled": True,
            "status": "failed",
            "error": str(exc),
        }


def _write_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, records: Iterable[Dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("ecommerce_comprehensive_%Y%m%dT%H%M%SZ")


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
    parser = argparse.ArgumentParser(
        description="Generate Pulse outputs for the comprehensive e-commerce corpus."
    )
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument(
        "--workspace-id",
        default="ecommerce_comprehensive_llm_eval",
    )
    parser.add_argument(
        "--output-dir",
        default="pulse_api/generated_outputs",
    )
    parser.add_argument(
        "--force-event-llm",
        action="store_true",
        help="Force event runtime LLM reasoning for each synthetic user.",
    )
    parser.add_argument(
        "--disable-runtime-llm",
        action="store_true",
        help="Run deterministic fallbacks instead of OpenAI calls.",
    )
    parser.add_argument(
        "--upsert-pgvector",
        action="store_true",
        help="Upsert vector memory records into pgvector when PULSE_DATABASE_URL is set.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
