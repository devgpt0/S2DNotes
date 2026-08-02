# Design an Offline-First Task Application

> **Difficulty:** Medium  
> **Main focus:** local database, outbox, conflict policy

## Interview prompt

Design a task application that remains fully usable without a network and syncs later.

## 1. Clarify the experience

**What I would say first:** The local database is the immediate UI source; the server remains the shared durable authority. Every local mutation gets an operation ID and enters a persistent outbox.

### Functional requirements

- Create, edit, complete, and delete tasks offline.
- Sync across devices after reconnect.
- Show sync and conflict status without blocking normal use.
- Protect data on shared or lost devices.

### Browser and product constraints

- The browser may close at any point during a mutation.
- Network transitions are frequent and requests may complete after timeout.
- Different devices may edit the same task concurrently.

## 2. State and API contracts

- POST /v1/sync {deviceId, lastCursor, operations[]} -> acknowledgements, remoteChanges, nextCursor
- Operation {operationId, entityId, baseVersion, type, patch, clientTime}
- Task {id, listId, title, completed, version, updatedAt, deletedAt?}

## 3. Frontend architecture

```text
UI <-> local repository <-> IndexedDB
          |                    |
          |                    +-> durable outbox
          |
       sync engine <-> network API <-> server change log
          |
 conflict resolver + visible sync status
```

## 4. Critical user flow

1. Write the task change and outbox operation in one IndexedDB transaction.
2. Render immediately from local data.
3. When online, send ordered operations with stable operation IDs.
4. Server deduplicates, applies allowed changes, and returns remote changes after the cursor.
5. Apply acknowledgements and remote changes atomically, then remove acknowledged outbox entries.

## 5. Deep dive

- Simple fields can use last-writer-wins with server version; destructive or text conflicts may require explicit user resolution.
- Tombstones prevent a deleted task from reappearing when an old device reconnects.
- Do not use online/offline events as truth; attempt sync and classify actual failures.
- Background sync is an optimization because browsers may suspend it.

## 6. Performance, resilience, and observability

- Batch operations and compact multiple unsent edits to the same field when semantics allow.
- Paginate and index local queries; do not load an entire account into memory.
- Use exponential backoff with user-triggered retry.
- Track outbox age, conflict rate, sync duration, cursor resets, and local database failures.

## 7. Security and accessibility

- Use XSS defenses because browser storage is accessible to compromised same-origin code.
- Encrypt especially sensitive local data only with a usable key and logout/deletion story.
- Provide keyboard access, clear sync labels, and error text not conveyed by color alone.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Network-first UI | Simpler consistency but unusable offline and high latency. |
| Local-first UI | Fast and resilient with explicit sync semantics. |
| Last-writer-wins | Simple but may silently discard meaningful edits. |
| User-visible conflicts | Safer for important data with more product complexity. |

## 9. 60-second interview summary

UI state comes from IndexedDB, and every local mutation atomically enters a persistent outbox. A cursor-based idempotent sync exchanges operations and remote changes, while tombstones and field-specific conflict rules prevent silent data resurrection or loss.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

