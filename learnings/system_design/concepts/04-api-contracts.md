# API Contracts

## Idea

An API is a long-lived contract between independently changing components. It
defines behavior, not only paths.

## Visual model

```text
client -> authenticated request + idempotency key -> service
client <- status + typed body + retry guidance ----- service
```

## Design steps

1. Model resources/actions and choose HTTP, RPC, events, or streaming.
2. Define request/response fields, validation, errors, and authorization.
3. Use cursor pagination for changing large collections.
4. Add idempotency to retried mutations.
5. Version compatibly: add optional fields before breaking shapes.

## When to use each style

- REST/HTTP: public resource APIs and broad interoperability.
- RPC: typed internal calls and action-oriented operations.
- Events: decoupled facts and asynchronous workflows.
- WebSocket/SSE: server-driven updates.

## Trade-offs

Fine-grained APIs are reusable but chatty. Coarse APIs reduce round trips but
couple clients to use cases. Events decouple time but add eventual consistency.

## Common mistakes

- Returning internal database models directly.
- Offset pagination on a rapidly changing feed.
- Retrying non-idempotent creates without a key.
- Putting secrets or sensitive data in URLs/logs.
