# Client State, Server State, and Offline Sync

## Idea

Separate ephemeral UI state from server-owned cached data. Offline writes need
a durable local log and a conflict policy.

## Classroom board

```text
server data -> query cache -> components
offline mutation -> local outbox -> optimistic UI
reconnect -> replay idempotently -> accept/reject/merge -> reconcile
```

## Design steps

1. Keep local state near its owner; cache server state by stable query key.
2. Define freshness, invalidation, pagination, and optimistic rollback.
3. Persist offline commands with IDs/base versions.
4. Reconnect, replay, resolve conflicts, and show unresolved user choices.

## When to use it

Offline-first matters for unreliable networks and field/mobile tools; ordinary
web apps may only need cached reads and retryable drafts.

## Trade-offs and mistakes

Last-write-wins is simple but can lose intent. Avoid copying server data into
multiple stores, optimistic success for irreversible actions, or silent merge
conflicts.
