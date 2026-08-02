# A First-Principles System Design Interview Framework

## The goal

A strong interview answer is a clear engineering conversation. The goal is not
to draw the largest diagram or name the most technologies. The goal is to find
the simplest design that meets the agreed requirements and explain when it
must evolve.

## The 40-minute structure

| Time | Work |
|---:|---|
| 0-5 min | Clarify users, operations, consistency, latency, and scope |
| 5-8 min | Estimate traffic, storage, bandwidth, and hot-key risk |
| 8-12 min | Define API contracts and the data model |
| 12-20 min | Draw the high-level design and one critical request flow |
| 20-32 min | Deep-dive into the hardest requirement |
| 32-37 min | Cover failures, security, observability, and cost |
| 37-40 min | State trade-offs, evolution, and a concise summary |

## 1. Clarify before drawing

Ask only questions that can change the architecture:

- Who uses the system and what are the top two actions?
- What is explicitly out of scope?
- What are peak reads, writes, payload sizes, and retention?
- Which results require strong consistency?
- What latency and availability targets matter?
- Is the system single-region, multi-region, offline, or real-time?
- What privacy, abuse, accessibility, or regulatory constraints apply?

> [!TIP]
> If the interviewer provides no number, state one reasonable assumption and
> continue. The calculation matters more than guessing the real company scale.

## 2. Estimate only architecture-changing numbers

```text
average requests/second = daily operations / 86,400
peak requests/second    = average * peak factor
storage/year            = writes/day * bytes/write * 365
bandwidth                = requests/second * bytes/response
```

Estimate enough to decide between one database and sharding, synchronous and
asynchronous work, client and CDN delivery, or one model worker and a GPU pool.

## 3. Define contracts before boxes

Write the main API and important data entities. This exposes ownership,
idempotency, pagination, authorization, and consistency requirements.

```text
POST /resources        Idempotency-Key: <client-generated key>
GET  /resources/{id}
GET  /resources?cursor=<opaque cursor>&limit=50
```

For events, define the producer, key, payload, ordering boundary, and duplicate
handling.

## 4. Draw one readable high-level diagram

```text
clients -> edge / gateway -> stateless service -> source-of-truth database
                              |        |
                              |        +-> cache / search / object storage
                              |
                              +-> durable queue -> idempotent workers
```

Label protocols and storage purpose. Do not draw components that have no job.

## 5. Walk one critical flow

Number the steps from user action to durable result. Say where validation,
authorization, deduplication, persistence, retries, and user feedback occur.

## 6. Deep-dive into the reason the question exists

Examples:

- feed: fan-out and ranking;
- booking: contention and overselling;
- collaboration: conflict resolution and reconnection;
- RAG: retrieval quality and grounding;
- LLM serving: batching, queueing, and GPU memory;
- frontend platform: ownership, isolation, and safe releases.

## 7. Design the unhappy path

Cover timeouts, retry limits, idempotency, backpressure, partial dependency
failure, stale caches, region loss, poison messages, and recovery objectives.

```text
dependency slow -> timeout -> bounded retry with jitter
                -> circuit opens -> fallback or explicit failure
                -> alert on SLO burn rate
```

## 8. Finish with cross-cutting concerns

- **Security:** authentication, authorization, least privilege, encryption,
  validation, abuse controls, secrets, and audit trails.
- **Observability:** request IDs, structured logs, metrics, traces, business
  outcomes, SLOs, and actionable alerts.
- **Cost:** dominant storage, bandwidth, database, search, or model costs.
- **Evolution:** the first bottleneck and the smallest justified next step.

## A strong final summary

```text
I chose <source of truth> because <consistency need>.
The read path meets <latency target> using <cache/index/edge strategy>.
Slow or retryable work moves through <durable async mechanism>.
The hardest trade-off is <A versus B>; I chose A because <requirement>.
At the next scale boundary, I would <specific evolution>.
```

## Common interview mistakes

- Drawing before agreeing on scope.
- Using exact company traffic numbers without stating they are assumptions.
- Naming products instead of explaining required capabilities.
- Ignoring data ownership, retries, duplicates, and deletion.
- Saying “eventual consistency” without describing the user-visible effect.
- Omitting client behavior in frontend design or evaluation in AI design.
- Ending without trade-offs and a summary.
