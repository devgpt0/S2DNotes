# Functional and Non-Functional Requirements

## Idea

Functional requirements say what users can do. Non-functional requirements say
how well and under which failures the system must do it.

## Visual model

```text
functional: create message, read history
quality:    deliver quickly, never lose acknowledged messages, preserve order per chat
```

## Design steps

1. Identify actors and their top three actions.
2. Define inputs, outputs, permissions, and lifecycle.
3. Ask about scale, regions, latency, availability, durability, and consistency.
4. Choose explicit non-goals.
5. Turn vague words into targets: “fast” becomes p95/p99 latency.

## When to use it

Always. Requirements determine whether you need a transaction, queue, cache,
WebSocket, strong read, or asynchronous result.

## Trade-offs

Strong consistency may increase latency or reduce availability during a
partition. Durability adds synchronous work. Rich scope reduces design depth.

## Common mistakes

- Treating every feature as equally important.
- Omitting authorization and data deletion.
- Confusing durability with availability.
- Designing an unstated global ordering guarantee.
