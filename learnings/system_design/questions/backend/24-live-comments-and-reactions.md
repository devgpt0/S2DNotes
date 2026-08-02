# Design Live Comments and Reactions

> **Difficulty:** Medium  
> **Main focus:** realtime fan-out, hot content, counters

## Interview prompt

Design comments, reactions, and live updates for a video, stream, or post.

## 1. Clarify the scope

**What I would say first:** Durable comments and ephemeral realtime delivery have different guarantees. Reaction counts may be eventually consistent, while moderation and comment order must be explicit.

### Functional requirements

- Post and paginate comments or replies.
- Add or remove one reaction per user and type.
- Push new comments and count changes to active viewers.
- Moderate, delete, rate-limit, and handle extremely hot content.

### Out of scope for the first version

- Video delivery and recommendation ranking are separate.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Most content is cold; a live event can have millions of concurrent viewers.
- Individual reaction events are much hotter than durable comment writes.
- Broadcasting every reaction to every viewer is unnecessary.

## 3. API and data model

### Main contracts

- POST /v1/content/{id}/comments {clientCommentId, body, parentId?}
- GET /v1/content/{id}/comments?cursor=...&sort=top|new
- PUT /v1/content/{id}/reactions/{type}
- WebSocket/SSE: comment.created, reaction.counts

### Important data

- Comment(content_id, comment_id, parent_id, author_id, body, created_at, moderation_state)
- Reaction(content_id, user_id, type, created_at)
- ReactionCount(content_id, type, count, version)

## 4. High-level design

```text
clients -> API -> comment store -> moderation/events -> realtime fan-out
           -> reaction service -> dedupe store -> counter stream -> aggregates
active clients <- regional channel gateways <- sampled/batched updates
```

## 5. Critical request flow

1. Authenticate and rate-limit, then persist a comment with idempotent client ID.
2. Run synchronous basic safety checks and asynchronous deeper moderation.
3. Publish allowed comment events to regional channel gateways.
4. Reaction upsert enforces one active value per user and emits a delta.
5. Aggregate deltas and broadcast count snapshots at a bounded frequency.

## 6. Deep dive

- Shard by content ID, but split exceptionally hot channels into fan-out subchannels.
- Do not send every heart or like event; send count updates several times per second.
- Ranked comments need stable cursors and a score snapshot; newest comments can use sequence order.
- Deletion uses tombstones so clients and indexes converge.

## 7. Scaling, failures, and observability

- Reconnect fetches comments after the last sequence and refreshes count snapshots.
- Counter aggregates rebuild from deduplicated reaction state or event logs.
- Slow clients receive coalesced state, not an unbounded event backlog.
- Monitor fan-out lag, dropped/coalesced updates, moderation latency, and hot-channel saturation.

## 8. Security and privacy

- Sanitize rendered text, prevent XSS, enforce block lists, and protect minors or private rooms.
- Rate-limit spam and coordinated abuse; keep moderation actions auditable.
- Do not expose viewer membership or raw user reaction lists without authorization.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Per-event broadcast | Exact animation but impossible at huge scale. |
| Batched count snapshots | Scalable with small visible lag. |
| Synchronous deep moderation | Safer before publish but high latency. |
| Layered moderation | Fast basic checks plus later correction. |

## 10. 60-second interview summary

Comments are durable ordered records with layered moderation, while reactions are deduplicated state feeding asynchronous aggregates. Regional gateways push comments and coalesced count snapshots, and reconnecting clients recover from durable sequence cursors.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

