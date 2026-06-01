# Voice of Customer Agent

## Purpose

Extract universal behavioral communication signals from:

- call recordings
- chat logs
- emails
- messages

The Voice of Customer Agent converts unstructured customer communication into
structured behavioral intelligence for Pulse. It is an intelligence extraction
system, not a response-generation system.

## Architecture

```text
Raw customer communication
        |
Speech / text normalization
        |
Embedding similarity against canonical behavior patterns
        |
LLM-style semantic reasoning
        |
Policy and safety rules
        |
VOCOutput
```

## Outputs

- frustration signal
- urgency signal
- trust signal
- retention risk
- escalation risk
- engagement signal

## Run Example

From the repository root:

```bash
python -m voice_of_customer_agent.examples.run_example
```

From inside `voice_of_customer_agent/`, use:

```bash
python examples/run_example.py
```

## Local Secrets

Create a local `.env` file in the repository root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

The `.env` file is ignored by Git.

## Replacement Points

- Replace `SpeechProcessor.process_audio` with Gemini 2.5 speech/audio analysis.
- Replace `VOCEmbeddingEngine` with real text embeddings.
- Replace `VOCLLMReasoner` with a model call using `VOC_SYSTEM_PROMPT`.
- Extend `PolicyEngine` and `default_rules.json` with business guardrails.
