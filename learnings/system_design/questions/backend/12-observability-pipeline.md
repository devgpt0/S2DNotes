# Design a Metrics and Log Ingestion Platform

> **Difficulty:** Hard  
> **Main focus:** high-volume ingestion, cardinality, retention

## Interview prompt

Design a platform that ingests, stores, searches, and alerts on application metrics and logs.

## 1. Clarify the scope

**What I would say first:** I will separate a durable ingestion path from storage-specific indexing. Cardinality and retention are product constraints, not afterthoughts.

### Functional requirements

- Accept batched metrics and structured logs.
- Support recent queries, dashboards, and alert evaluation.
- Handle tenant quotas, retention tiers, and backpressure.
- Preserve enough data during partial storage outages.

### Out of scope for the first version

- Distributed tracing can reuse the ingestion pattern but has a distinct query model.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume tens of millions of events per second and petabytes of daily raw data.
- Writes dominate; compression, batching, and sampling materially affect cost.
- Unbounded metric labels or log fields can create operational collapse.

## 3. API and data model

### Main contracts

- POST /v1/metrics:write batched time series
- POST /v1/logs:write compressed structured events
- POST /v1/query {tenant, expression, start, end, limit}

### Important data

- Metric sample: tenant, metric, sorted label set, timestamp, value
- Log event: tenant, timestamp, service, severity, indexed fields, body
- RetentionPolicy(tenant, dataset, hot_days, archive_days, quota)

## 4. High-level design

```text
agents -> regional collectors -> durable partitioned log
                  |                       |
                  +-> admission/quota     +-> metric compactors -> time-series store
                                          +-> log indexers -> hot search store
                                          +-> archive writers -> object storage
query API -> planner -> hot stores + archive -> merge
alert engine -> query/cache -> notification
```

## 5. Critical request flow

1. Agents batch, compress, and retry with bounded local buffers.
2. Collectors authenticate the tenant, validate schemas, and enforce quotas.
3. Partition the durable log by tenant and series or time key.
4. Independent consumers write time-series blocks, log indexes, and archive files.
5. The query planner selects hot or archived sources and enforces scanned-data limits.

## 6. Deep dive

- Canonicalize metric labels and reject or aggregate high-cardinality dimensions.
- Store compressed immutable time blocks; compact small blocks later.
- Index selected log fields and keep full bodies in cheaper columnar or object storage.
- Alert rules need evaluation timestamps, late-data policy, and deduplicated notifications.

## 7. Scaling, failures, and observability

- Collectors shed low-priority data before durable queues exhaust disk.
- Consumers checkpoint offsets only after idempotent storage writes.
- Rebuild indexes from the durable log or object archive.
- Monitor ingest loss, queue age, cardinality, query scanned bytes, alert delay, and tenant cost.

## 8. Security and privacy

- Use tenant-scoped credentials, encryption, strict query isolation, and field redaction.
- Prevent log injection and never encourage secrets or personal data in telemetry.
- Audit cross-tenant support access and enforce retention deletion.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Index every field | Flexible queries but unacceptable storage and write cost. |
| Selected indexes | Cheaper with less ad hoc search. |
| Drop on overload | Protects platform but loses evidence. |
| Durable buffering | Improves recovery until finite storage fills. |

## 10. 60-second interview summary

Regional collectors validate and admit compressed batches into a durable log. Independent pipelines build metrics blocks, log indexes, and object archives. Cardinality, quota, retention, backpressure, and rebuildability are first-class design decisions.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

