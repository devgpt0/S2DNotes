# Design a Personalized News Feed

> **Difficulty:** Hard  
> **Main focus:** fan-out, ranking, pagination

## Interview prompt

Design a home feed that combines posts from followed accounts and ranks them.

## 1. Clarify the scope

**What I would say first:** I will separate candidate generation from ranking and use stable cursor pagination. The main trade-off is fan-out on write versus fan-out on read.

### Functional requirements

- Create posts and show a personalized ranked feed.
- Support follows, deletes, privacy, and pagination.
- Keep new posts visible quickly without duplicating items.
- Measure engagement while avoiding unsafe or blocked content.

### Out of scope for the first version

- The media transcoding pipeline is reused from the video or media-storage design.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 500 million users, 50 million daily posts, and read traffic far above writes.
- Follower counts are highly skewed, so celebrity accounts require special handling.
- Store only bounded recent feed candidates per user.

## 3. API and data model

### Main contracts

- POST /v1/posts {text, mediaIds, visibility}
- GET /v1/feed?cursor=...&limit=30
- PUT /v1/follows/{creatorId}

### Important data

- Post(post_id, author_id, content_ref, visibility, created_at, status)
- Follow(follower_id, followee_id, created_at)
- FeedEntry(user_id, score_time, post_id, source, inserted_at)

## 4. High-level design

```text
creator -> post service -> post store -> event stream
                                      |
                         +------------+-------------+
                         |                          |
                  normal fan-out workers      celebrity index
                         |                          |
                         +-> candidate inboxes <----+
                                      |
viewer -> feed API -> candidate fetch -> policy filter -> ranker -> hydrate/cache
```

## 5. Critical request flow

1. Persist the post, then publish it with an outbox.
2. Fan out normal-author posts to follower candidate inboxes.
3. Keep celebrity posts in author timelines and merge them during reads.
4. Fetch candidates, remove blocked/deleted/private content, rank, then hydrate.
5. Return an opaque cursor containing stable score and tie-breaker information.

## 6. Deep dive

- Hybrid fan-out prevents one celebrity post from creating hundreds of millions of synchronous writes.
- Ranking features must be point-in-time correct and the system needs a chronological fallback.
- Feed entries reference posts; deletion or privacy changes are enforced again at read time.
- Cursor pagination avoids duplicates caused by insertions above the current page.

## 7. Scaling, failures, and observability

- If ranking is unavailable, serve a filtered reverse-chronological feed.
- If fan-out lags, merge recent author timelines so fresh posts still appear.
- Rebuild candidate inboxes from the post stream when corruption is detected.
- Monitor freshness, candidate recall, ranking latency, duplicate rate, and policy-filter failures.

## 8. Security and privacy

- Enforce visibility and block relationships during both fan-out and reads.
- Apply moderation before broad distribution and support rapid takedown.
- Limit sensitive feature access and audit ranking policy changes.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Fan-out on write | Fast feed reads but expensive for high-follower authors. |
| Fan-out on read | Cheap writes but heavy read-time merging. |
| Ranked feed | More relevance but requires evaluation and transparency controls. |
| Chronological feed | Simple and reliable but less personalized. |

## 10. 60-second interview summary

I use hybrid fan-out: materialize candidates for ordinary authors and merge celebrity timelines at read time. A separate policy and ranking stage produces stable cursor pages, with chronological fallback and read-time privacy enforcement.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

