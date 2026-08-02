# Real-Time Collaboration and Conflict Resolution

## Idea

Collaborative frontends apply local edits immediately, exchange operations, and
converge after delay, duplication, reordering, reconnects, and concurrent edits.
Presence is ephemeral; document edits are durable.

## Visual model

```text
local edit -> optimistic document + durable local operation
          -> collaboration service -> ordered/causal operations -> peers
reconnect -> snapshot + operations after version -> converge
```

## Design steps

1. Define the shared model and conflict semantics at field/operation level.
2. Choose server sequencing, operational transformation (OT), or CRDTs.
3. Give operations stable client IDs, sequence IDs, and idempotency.
4. Separate durable document operations from cursor/presence updates.
5. Persist snapshots plus operation history and define compaction.
6. Handle reconnect, offline edits, permission changes, and deleted documents.

## When to use each model

- Server-ordered operations: simplest when always-online and centralized.
- OT: established for text editing with a transformation server.
- CRDT: useful for offline/peer concurrency; metadata and implementation cost.

## Trade-offs

Immediate local edits improve experience but require reconciliation. Stronger
offline convergence adds metadata and can make product-specific conflict rules
harder to express.

## Common mistakes

- Treating WebSocket delivery as a conflict-resolution algorithm.
- Using timestamps alone to merge rich document edits.
- Persisting high-frequency presence like durable content.
- Reconnecting without a version/resume protocol and silently losing edits.
