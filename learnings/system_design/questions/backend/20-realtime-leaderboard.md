# Design a Real-Time Leaderboard

> **Difficulty:** Medium  
> **Main focus:** rank updates, top-k, anti-cheat

## Interview prompt

Design global and friend leaderboards that update quickly during a game or event.

## 1. Clarify the scope

**What I would say first:** Scores need an authoritative event path; ranking is derived state that can be rebuilt. I will clarify whether scores only increase and how ties are ordered.

### Functional requirements

- Submit validated score events.
- Read global top-k, a user's rank, and nearby ranks.
- Support friend or regional boards and season resets.
- Remove fraudulent scores and rebuild rankings.

### Out of scope for the first version

- Game simulation and detailed anti-cheat models are upstream.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume millions of score updates per second during events.
- Top-k reads are hot and cacheable; exact rank for every user is more expensive.
- Season partitions bound data and simplify reset.

## 3. API and data model

### Main contracts

- POST /v1/scores {eventId, userId, delta|absolute, gameProof, operationId}
- GET /v1/leaderboards/{season}/top?limit=100
- GET /v1/leaderboards/{season}/users/{id}/window?radius=5

### Important data

- ScoreEvent(operation_id, season, user_id, value, verified_at)
- CurrentScore(season, board, user_id, score, tie_break_time)
- LeaderboardSnapshot(season, board, generated_at, top_entries)

## 4. High-level design

```text
game servers -> score validation -> immutable score stream
                                      |
                                  rank workers
                                      |
                         partitioned ordered-set shards
                           |                    |
                      top-k cache          rank query service
                           |
                    snapshot/archive/rebuild
```

## 5. Critical request flow

1. Authenticate a trusted game server and deduplicate operation ID.
2. Validate the score transition and append an immutable event.
3. Update the user's ordered-set entry atomically.
4. Update cached top-k only when the changed score can affect it.
5. For friend boards, fetch friend IDs then rank their current scores.

## 6. Deep dive

- Shard ordinary ranking by score range or user hash; exact global rank needs shard counts plus local rank.
- Tie-break with earliest achievement time or another documented stable key.
- For massive boards, approximate rank may be acceptable outside the top region.
- Immutable events allow removal and deterministic rebuild after anti-cheat decisions.

## 7. Scaling, failures, and observability

- If ranking workers lag, accept score events and display a freshness timestamp.
- Reprocess from checkpoints idempotently and compare snapshots.
- Season rollover creates a new namespace rather than clearing a live structure.
- Monitor event lag, rejected updates, top-k freshness, rebuild time, and hot-shard skew.

## 8. Security and privacy

- Accept authoritative scores from trusted servers, not client claims alone.
- Rate-limit and sign submissions, detect impossible changes, and audit removals.
- Avoid exposing hidden user identifiers on public boards.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Exact global rank | More coordination and query cost. |
| Approximate rank | Scales better with small accuracy loss. |
| Synchronous rank update | Fresh reads but score submission depends on ranking. |
| Eventual rank update | Reliable ingestion with visible short lag. |

## 10. 60-second interview summary

Validated immutable score events are the source of truth, while ordered-set shards and top-k caches are rebuildable derived state. Stable tie rules, seasonal namespaces, anti-cheat correction, and explicit freshness make the system predictable.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

