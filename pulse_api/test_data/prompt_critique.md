# Master Prompt Critique

## Event Understanding Prompt

Strengths:

- Clear separation between taxonomy classification and runtime reasoning.
- Explicitly says not to recommend actions.
- Good cost-control framing: runtime LLM only for ambiguous cases.

Gaps:

- Does not ask the model to identify signal conflicts explicitly.
- Does not request evidence spans or event examples behind scores.
- Does not distinguish recent high-value events from older repeated events.
- Does not ask for abstention/low-confidence behavior when event taxonomy has
  unknowns or missing recency.

Recommended additions:

- Add `conflict_summary`.
- Add `evidence_events`.
- Add `recency_weighting_notes`.
- Add `data_quality_flags`.

## Voice of Customer Prompt

Strengths:

- Strong role boundary: extraction only, not support response.
- Good signal contract.
- Handles sparse/mixed communication with lower confidence.

Gaps:

- Does not explicitly cover multilingual or code-mixed communication.
- Does not ask for transcript-quality or noise-quality flags.
- Does not separate transcription confidence from semantic confidence.
- Does not require evidence snippets for frustration, urgency, trust erosion,
  or retention risk.

Recommended additions:

- Add language detection and code-mixing handling.
- Add `transcription_quality_flags`.
- Add `semantic_adequacy_confidence`.
- Add `evidence_spans`.
- Add instruction: if transcript has non-English text, translate internally but
  preserve original meaning and do not over-penalize confidence solely for
  language.

## NBA Explanation Prompt

Strengths:

- Correctly prevents recomputation.
- Good for auditable marketer-facing explanation.
- Uses counterfactuals directly.

Gaps:

- Does not mention auto-approve / observe / reject confidence bands.
- Does not require explanation of channel, time, content, and constraint
  overrides.
- Does not ask for alternatives ruled out in the exact UI-friendly structure.
- Does not explain expected value per communication.

Recommended additions:

- Add confidence band explanation.
- Add delivery-plan explanation.
- Add constraint override explanation.
- Add expected-value-per-comms explanation.
- Add concise UI sections: `why_this_action`, `alternatives_ruled_out`,
  `constraint_resolution`, `risk_note`.

## Overall Prompt Governance

Recommended shared requirements:

- Always separate model inference from deterministic facts.
- Always output data-quality flags.
- Always identify whether the model is confident enough for automation.
- Always include short evidence references, not chain-of-thought.
- For multilingual VoC, include original-language evidence and English
  interpretation.
