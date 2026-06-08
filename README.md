# Pulse AI

AI-powered decisioning layer for customer engagement platforms.
Pulse AI helps Lifecycle PMs, CRM managers, and Growth PMs decide the next best action for every customer by combining behavioral signals, customer communication intelligence, CRM context, predicted outcomes, and business constraints.

## Problem
Customer engagement platforms like Braze, MoEngage, and WebEngage help teams send campaigns, but they do not reliably answer:
- Which users should not be messaged?
- Will suppressing a message reduce revenue?
- Which intervention is best for this user right now?
- What business impact did the decision actually create?

Pulse AI is designed to answer these questions.

## Core Architecture
Event Understanding Agent
        +
Voice of Customer Agent
        +
CRM Context
        ↓
Behavioral State Engine
        ↓
Behavioral Memory + Similarity Retrieval
        ↓
Outcome Estimator
        ↓
NBA Decision Engine
        ↓
Recommendation API
        ↓
Enterprise Engagement Platform
        ↓
Intervention Outcome Tracker
        ↓
Decision Evidence Dashboard

Key Modules
1. Event Understanding Agent
Maps raw event streams into behavioral intent signals.

2. Voice of Customer Agent
Analyzes customer calls, chats, emails, tickets, and messages for sentiment, urgency, trust, retention risk, and escalation risk.

3. Behavioral State Engine
Fuses Event Understanding, VoC, and CRM context into a unified customer behavioral state vector.

4. Behavioral Memory + Outcome Estimator
Retrieves similar historical users and estimates predicted outcomes for possible interventions.

5. NBA Decision Engine
Chooses the best action using predicted outcomes, business goals, and constraints.

6. Intervention Outcome Tracker
Measures what happened because of Pulse decisions, including incrementality, suppression impact, and decision evidence.

7. Pulse API
FastAPI backend for frontend and Lovable integration.

8. Model Routing
Pulse centralizes model selection in model_router.

Default routing:
event_taxonomy_classification -> gpt-5.1
event_runtime_fallback        -> gpt-5-mini
voc_reasoning                 -> gpt-5.1
nba_explanation               -> gpt-5-mini
audio_transcription           -> gpt-4o-transcribe

9. Cost-Aware Design
Pulse avoids running LLMs per user.

Instead:
- LLMs classify enterprise event taxonomy periodically.
- Runtime event understanding uses lookup tables, embeddings, and rules.
- VoC runs only when new communication arrives.
- Behavioral state refresh is hybrid: real-time for critical events, batch for normal updates.
- NBA explanations use smaller models because decisions are already computed.

9. pgvector
Pulse uses pgvector for production vector retrieval.

Pulse helps them improve revenue, reduce fatigue, protect retention, and prove the incremental impact of communication decisions.

ICP: 
Lifecycle PMs
CRM managers
Growth PMs
teams managing customer engagement P&L
