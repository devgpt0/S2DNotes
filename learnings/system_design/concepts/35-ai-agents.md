# Agent and Tool Orchestration

## Idea

An agent chooses model/tool steps toward a goal. Production agents need a
bounded state machine, durable checkpoints, typed tools, and approval gates.

## Classroom board

```text
goal -> plan/next step -> validate tool call -> execute -> record observation
     -> stop success | retry bounded | request approval | fail safely
```

## Design steps

1. Give every tool a strict schema, least privilege, timeout, and idempotency.
2. Store run/step state and immutable audit events.
3. Bound steps, tokens, cost, retries, and wall time.
4. Require approval for destructive/external actions and verify completion.

## Trade-offs and mistakes

Autonomy improves flexibility but expands risk and nondeterminism. Do not let
model text bypass authorization, trust tool output blindly, retry side effects
without keys, or call “no exception” success.
