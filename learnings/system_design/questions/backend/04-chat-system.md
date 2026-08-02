# Design a Chat and Messaging System

> **Difficulty:** Hard  
> **Main focus:** realtime delivery, ordering, offline sync

## Interview prompt

Design one-to-one and group chat with history, presence, and multi-device delivery.

## 1. Clarify the scope

**What I would say first:** I will guarantee durable messages and per-conversation order, not a single global order. Presence may be eventually consistent.

### Functional requirements

- Send one-to-one and group messages.
- Deliver in real time when connected and sync missed messages later.
- Support multiple devices, read receipts, typing, and attachments.
- Allow pagination, deletion policy, and abuse reporting.

### Out of scope for the first version

- End-to-end encryption can be a dedicated deep dive because it changes server capabilities.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 100 million daily users and 10 billion messages per day.
- Connections are long-lived; message writes and fan-out dominate.
- Large groups require server-side fan-out strategy changes.

## 3. API and data model

### Main contracts

- POST /v1/conversations/{id}/messages {clientMessageId, body, attachmentIds}
- GET /v1/conversations/{id}/messages?beforeSequence=...&limit=50
- WebSocket events: message.created, receipt.updated, typing.changed

### Important data

- Conversation(id, type, membership_version, last_sequence)
- Message(conversation_id, sequence, message_id, sender_id, body_ref, created_at)
- DeviceCursor(user_id, device_id, conversation_id, last_delivered_sequence)

## 4. High-level design

```text
mobile/web -> connection gateway -> session directory
                    |                    |
                    v                    v
              message service -> conversation-partitioned log -> message store
                    |                    |
                    +-> fan-out service -+-> online gateways
                                         +-> offline inbox/cursors
attachments -> signed upload -> object storage -> scanning
```

## 5. Critical request flow

1. Client sends a stable clientMessageId so retries are safe.
2. The conversation owner assigns the next sequence and durably appends the message.
3. Fan-out publishes to online device gateways and records offline progress.
4. Recipients acknowledge delivery or read state with monotonic sequence numbers.
5. Reconnect uses the stored cursor to fetch every missing sequence.

## 6. Deep dive

- Partition by conversation ID to serialize writes and preserve per-conversation order.
- Small groups can fan out on write; huge groups may fan out on read or use hybrid membership segments.
- Presence uses expiring heartbeats and should not share the durable message path.
- Attachments are uploaded directly to object storage and referenced only after malware scanning.

## 7. Scaling, failures, and observability

- Clients deduplicate by message ID and reorder briefly by sequence.
- If a gateway dies, clients reconnect with jitter and resume from a durable cursor.
- A poison event is quarantined; it must not block an entire conversation partition.
- Monitor send-to-persist latency, delivery lag, reconnect rate, and missing-sequence alarms.

## 8. Security and privacy

- Authorize membership on every send and history read.
- Rate-limit spam, scan attachments, support block lists, and retain audit evidence carefully.
- Encrypt transport and storage; minimize message content in logs.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Fan-out on write | Fast reads for normal groups, expensive for celebrity-size groups. |
| Fan-out on read | Cheaper writes, more complex and slower reads. |
| Per-conversation order | Useful and scalable. |
| Global order | Unnecessary coordination with little user value. |

## 10. 60-second interview summary

Messages are appended durably to a log partitioned by conversation, which gives per-conversation sequence numbers. Gateways handle live sockets, cursors recover offline gaps, and fan-out changes from write to hybrid behavior for very large groups.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

