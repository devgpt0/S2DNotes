# 08 - Microservices and System Design

## Design Interview Flow

1. Clarify functional and non-functional requirements.
2. Estimate scale and identify dominant operations.
3. Define API/events and data model.
4. Draw components and ownership boundaries.
5. Deep-dive critical read/write flows.
6. Handle failure, consistency, security, and overload.
7. Add observability, deployment, migration, and cost.
8. State tradeoffs and remaining risks.

## Capacity Example

```text
10,000 requests/second * 2 KB average payload = 20 MB/second before protocol/replication overhead
# Result: approximately 1.728 TB/day of raw payload if every request were retained.
```

State assumptions; interviewers care about reasoning more than false precision.

## Common Designs

- URL shortener: key generation, redirect cache, abuse controls
- rate limiter: token bucket, distributed counters, consistency
- notification service: preferences, queues, provider failure, deduplication
- order/payment: idempotency, saga, ledger, reconciliation
- file storage: multipart upload, metadata, object store, scanning
- search: ingestion, indexing, relevance, reindexing
- chat: connection management, ordering, presence, offline delivery
- RAG assistant: ingestion, authorization filters, retrieval quality, tool security, evaluation

## Distributed-System Fundamentals

- network calls can time out after success
- clocks are not perfectly synchronized
- duplicate/out-of-order delivery is normal in many systems
- replication creates lag and conflict choices
- partitions require availability/consistency tradeoffs per operation
- exactly-once business effect normally comes from idempotency and atomic local state

## Senior Tradeoff

Do not jump to Kafka, Kubernetes, Redis, NoSQL, or microservices. Introduce each component only after naming the requirement it satisfies and its new failure modes.
