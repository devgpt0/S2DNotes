# Frontend State, Server State, and Offline Sync

## Idea

State should have one clear owner. UI state is local and temporary; server
state is remote, cached, shared, and can become stale. Offline state adds a
durable operation log and conflict policy.

## Visual model

```text
UI state -> component/route
server state -> query cache <-> API
offline writes -> local durable queue -> sync -> conflict resolution
```

## Design steps

1. Classify each value: URL, local UI, shared client, server cache, or durable offline.
2. Give server data stable query keys, freshness, invalidation, and deduplication.
3. Normalize shared entities only when multiple views edit the same records.
4. Model mutations with pending/success/failure and idempotency keys.
5. For offline use, persist operations plus base versions—not only final snapshots.
6. Define conflict policy: server wins, client wins, field merge, or CRDT/domain merge.

## When to use it

Offline-first is justified for unreliable networks or core field/mobile workflows.
Do not add it to a simple online application without a product requirement.

## Trade-offs

Optimistic UI feels fast but needs rollback/reconciliation. Long cache freshness
reduces requests but increases stale views. General conflict resolution is
complex; domain-specific rules are often clearer.

## Common mistakes

- Copying server responses into several unrelated stores.
- Global state for values used by one component.
- Retrying a mutation without idempotency.
- Saying “last write wins” without a trustworthy clock/version and acceptable loss.
