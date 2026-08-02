# Design a Collaborative Document Editor Frontend

> **Difficulty:** Hard  
> **Main focus:** local-first edits, conflict resolution, presence

## Interview prompt

Design the browser architecture for real-time multi-user document editing with offline recovery.

## 1. Clarify the experience

**What I would say first:** Keystrokes must apply locally without waiting for the network. I will represent edits as operations, persist an outbox, and merge concurrent changes using OT or a CRDT selected with the backend.

### Functional requirements

- Edit immediately, see remote changes, and show collaborator presence.
- Reconnect after network loss without losing local edits.
- Support undo/redo, selections, comments, and large documents.
- Display sync state and resolve rejected permissions.

### Browser and product constraints

- Typing latency must stay below a frame.
- Operations can arrive duplicated, late, or out of order.
- Presence is ephemeral; document content is durable.

## 2. State and API contracts

- WebSocket: join(documentId, lastServerVersion), operation, ack, presence
- GET /v1/documents/{id}/snapshot?version=...
- Operation contains operationId, clientId, baseVersion or CRDT clock, and payload

## 3. Frontend architecture

```text
editor view <-> local document model <-> undo manager
                     |                |
                     |                +-> durable local outbox (IndexedDB)
                     |
              merge engine (OT/CRDT)
                     |
              sync client <-> WebSocket gateway
                     |
             snapshot/checkpoint API
presence layer is separate and lossy
```

## 4. Critical user flow

1. Apply each keystroke to the local model and append an operation to the local outbox.
2. Send operations in protocol order and keep them until acknowledged.
3. Transform or merge remote operations against unacknowledged local work.
4. Update the rendered affected block, not the entire document.
5. On reconnect, exchange clocks or versions, replay missing remote work, then resend unacknowledged operations.

## 5. Deep dive

- OT needs a central version order and transformation rules; CRDTs carry merge metadata and can support peer-like offline work.
- Undo must invert the user's logical operation in the current merged document, not restore an old full snapshot.
- Partition large documents into blocks and virtualize blocks outside the viewport.
- Presence uses throttled cursor updates and expires; it never blocks document synchronization.

## 6. Performance, resilience, and observability

- Batch remote rendering within animation frames while preserving operation order.
- Checkpoint to bound startup replay and compact local operation history after acknowledgement.
- Use backpressure and a visible offline state when the outbox grows.
- Track local input latency, merge time, reconnect duration, lost-op incidents, and outbox size.

## 7. Security and accessibility

- Authorize the document on join and every reconnect; handle permission revocation immediately.
- Sanitize pasted or rendered rich content and restrict embedded resources.
- Provide keyboard editing, screen-reader labels, collaborator color alternatives, and non-color presence cues.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| OT | Smaller operation metadata with a central sequencing dependency. |
| CRDT | Flexible offline merge with more metadata and implementation complexity. |
| Whole-document render | Simple but slow for large documents. |
| Block model | Efficient updates with cross-block editing complexity. |

## 9. 60-second interview summary

The editor is local-first: operations update the model immediately, enter an IndexedDB outbox, and merge through OT or CRDT semantics. Durable document sync, ephemeral presence, block virtualization, checkpoint recovery, and explicit permission changes keep it usable under failure.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

