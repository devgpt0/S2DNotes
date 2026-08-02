# Design a Real-Time Chat Frontend

> **Difficulty:** Medium  
> **Main focus:** optimistic messages, reconnect, long history

## Interview prompt

Design the web or mobile-web client for conversations, attachments, receipts, and unreliable connections.

## 1. Clarify the experience

**What I would say first:** The UI needs a local message state machine and durable client IDs so optimistic sends reconcile with server acknowledgements instead of duplicating.

### Functional requirements

- Show conversation list, paginated history, live messages, typing, and receipts.
- Send text and attachments optimistically.
- Reconnect and fill missed-message gaps.
- Handle edits, deletes, block states, and long histories.

### Browser and product constraints

- Events may be duplicated, reordered, or missed during disconnect.
- Uploads can finish after the user leaves the conversation.
- Prepending old messages must not move the visible scroll anchor.

## 2. State and API contracts

- GET /v1/conversations/{id}/messages?beforeSequence=...&limit=50
- POST /v1/conversations/{id}/messages {clientMessageId, body, attachmentIds}
- WebSocket events include conversationId, sequence, eventId, and entity version

## 3. Frontend architecture

```text
conversation UI -> normalized message store -> paginated history cache
       |                    |
       |                    +-> optimistic mutation/outbox
       |
socket manager -> sequencer/gap detector -> event reducer
       |
upload manager -> signed multipart uploads
typing/presence state is ephemeral and separate
```

## 4. Critical user flow

1. Create a local pending message with clientMessageId and render immediately.
2. Upload attachments, then send the message using the same stable ID on retries.
3. Server acknowledgement replaces pending metadata without changing UI identity.
4. Socket events deduplicate by event ID and apply in per-conversation sequence.
5. On a gap or reconnect, fetch messages after the last durable sequence.

## 5. Deep dive

- Use inverted or anchor-preserving virtualization so loading older history does not jump the viewport.
- A failed message remains visible with retry and remove actions.
- Read receipts advance monotonically by sequence instead of one event per message.
- Typing is throttled, expires quickly, and never enters durable message state.

## 6. Performance, resilience, and observability

- Virtualize history, lazy-load media, and keep normalized entities outside individual bubbles.
- Use one socket manager and multiplex conversations.
- Back off reconnect with jitter while keeping explicit offline status.
- Track send-to-ack, gap recovery, duplicate events, socket reconnects, scroll jumps, and message render cost.

## 7. Security and accessibility

- Sanitize rich text and links, isolate previews, and never trust attachment MIME alone.
- Clear sensitive cached data on logout according to product policy.
- Support keyboard navigation, message grouping semantics, screen-reader announcements, and reduced motion.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Wait for send acknowledgement | Simple but feels slow. |
| Optimistic pending message | Responsive with reconciliation states. |
| One socket per conversation | Simple handlers but wasteful. |
| Multiplexed socket | Efficient with routing complexity. |

## 9. 60-second interview summary

A normalized message store and explicit pending/sent/failed states reconcile optimistic client IDs with sequenced server events. One multiplexed socket detects gaps, history virtualization preserves anchors, and attachment, typing, and durable message concerns stay separate.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

