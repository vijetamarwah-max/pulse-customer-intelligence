import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    args = _parse_args()
    output_dir = Path(args.output_dir)
    output_files = sorted(output_dir.glob("*_action_centre_outputs.json"))
    vector_files = sorted(output_dir.glob("*_vector_memory_records.jsonl"))

    if not output_files:
        raise FileNotFoundError(f"No output files found in {output_dir}.")

    selected_output_files = output_files[-args.last :]
    selected_vector_files = vector_files[-args.last :]
    merged = _merge_outputs(selected_output_files)
    run_id = datetime.now(timezone.utc).strftime("ecommerce_comprehensive_merged_%Y%m%dT%H%M%SZ")

    merged_path = output_dir / f"{run_id}_action_centre_outputs.json"
    vector_path = output_dir / f"{run_id}_vector_memory_records.jsonl"
    summary_path = output_dir / f"{run_id}_summary.json"

    merged_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    _merge_jsonl(selected_vector_files, vector_path)

    summary = {
        "run_id": run_id,
        "source_output_files": [str(path) for path in selected_output_files],
        "source_vector_files": [str(path) for path in selected_vector_files],
        "merged_output_path": str(merged_path),
        "merged_vector_records_path": str(vector_path),
        "users_processed": len(merged["recommendations"]),
        "state_labels": sorted(
            {
                item["behavioral_state"]["state_label"]
                for item in merged["recommendations"]
            }
        ),
        "recommended_actions": sorted(
            {item["recommended_action"] for item in merged["recommendations"]}
        ),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


def _merge_outputs(paths):
    merged = None
    recommendations = []
    processing_trace = []
    user_decisions = []

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if merged is None:
            merged = payload
        recommendations.extend(payload.get("recommendations", []))
        processing_trace.extend(payload.get("processing_trace", []))
        user_decisions.extend(payload.get("user_decisions", []))

    merged["recommendations"] = recommendations
    merged["processing_trace"] = processing_trace
    merged["user_decisions"] = user_decisions
    merged["metrics"] = {
        "users_scored": len(recommendations),
        "expected_incremental_value": round(
            sum(item.get("expected_incremental_value", 0.0) for item in recommendations),
            2,
        ),
        "suppression_recommendations": sum(
            1 for item in recommendations if item["recommended_action"] == "suppress"
        ),
        "service_recovery_recommendations": sum(
            1
            for item in recommendations
            if item["recommended_action"] == "service_recovery"
        ),
        "average_confidence": round(
            sum(item["confidence"] for item in recommendations) / len(recommendations),
            3,
        )
        if recommendations
        else 0.0,
    }
    merged["run_metadata"] = {
        "merged_from": [str(path) for path in paths],
        "merged_at": datetime.now(timezone.utc).isoformat(),
        "users_processed": len(recommendations),
    }
    return merged


def _merge_jsonl(paths, output_path):
    with output_path.open("w", encoding="utf-8") as writer:
        for path in paths:
            writer.write(path.read_text(encoding="utf-8"))


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="pulse_api/generated_outputs")
    parser.add_argument("--last", type=int, default=6)
    return parser.parse_args()


if __name__ == "__main__":
    main()
