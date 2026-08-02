# System Design: Beginner to Expert

This course teaches system design as a repeatable engineering process. It
covers shared foundations first, then backend, frontend, and AI-engineering
systems.

The [progressive concept path](concepts/README.md) contains 59 focused notes.
Each new concept has its own file so it can be learned and revised independently.

## Important date note

No reliable list of "most asked 2027 questions" exists yet because the current
date is August 2026. The question set therefore combines widely recurring
2024-2026 interview prompts with forward-looking topics such as AI agents, RAG,
LLM serving, real-time collaboration, privacy, reliability, and cost control.
Companies vary, so treat the set as a high-value curriculum, not a universal
ranking.

## How to use the course

1. Read the [concepts](concepts/README.md) in order.
2. After each note, explain the visual model without looking at it.
3. For each solved design, hide the solution and work for 35-45 minutes.
4. Start with requirements and scale; do not draw boxes immediately.
5. Defend every storage, protocol, consistency, and deployment choice.
6. End with failures, security, observability, cost, and trade-offs.

```text
requirements -> estimates -> API and data -> high-level design
       -> deep dive -> failures and security -> trade-offs -> evolution
```

## Coverage

- **Backend:** distributed foundations, data systems, messaging, resilience,
  real-time systems, operations, multi-region design, migrations, and cost.
- **Frontend:** rendering, state, offline sync, browser networking, performance,
  safe releases, accessibility, security, and real-time collaboration.
- **AI engineering:** data and features, RAG, serving, evaluation, agents,
  training, GPU scheduling, multimodal systems, security, human review, and cost.

## Solved interview designs

- [Complete interview question bank](questions/README.md) - 60 fully solved
  backend, frontend, and AI-engineering designs
- [Backend systems](questions/backend/README.md)
- [Frontend systems](questions/frontend/README.md)
- [AI-engineering systems](questions/ai-engineering/README.md)

## Standard used in every solved design

```text
scope and requirements
    -> scale assumptions
    -> API and data model
    -> visual architecture
    -> critical request flow
    -> scaling and failure handling
    -> security and observability
    -> trade-offs and interview follow-ups
```

## What expert means here

An expert does not name the most technologies. An expert makes requirements
explicit, chooses the simplest design that meets them, predicts failure modes,
and explains what must change at the next scale boundary.

Existing deeper distributed-systems notes are linked where useful:
[distributed-systems roadmap](../computer_fundamentals/distributed_systems/00-distributed-systems-roadmap.md).
