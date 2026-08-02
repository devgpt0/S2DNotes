# Design a Tamper-Evident Audit Log

> **Difficulty:** Hard  
> **Main focus:** immutability, integrity, compliance search

## Interview prompt

Design an audit platform for security-sensitive user and administrator actions.

## 1. Clarify the scope

**What I would say first:** An audit log must be complete, append-only, attributable, searchable, and independently verifiable. It is different from debug logging.

### Functional requirements

- Capture who did what, to which resource, when, and with what result.
- Prevent silent modification or deletion.
- Search by tenant, actor, resource, action, and time.
- Export evidence with retention and legal-hold controls.

### Out of scope for the first version

- General application logs and high-volume metrics are separate pipelines.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume billions of events per day but far fewer searches.
- Events are small and append-only; long retention dominates storage.
- Tenant isolation and time-bounded queries are mandatory.

## 3. API and data model

### Main contracts

- appendAuditEvent(event) from authenticated internal producers
- GET /v1/audit-events?actor=...&resource=...&start=...&end=...&cursor=...
- POST /v1/audit-exports {filters, destination}

### Important data

- AuditEvent(event_id, tenant_id, event_time, ingest_time, actor, action, resource, outcome, request_id, previous_hash, hash)
- SignedCheckpoint(partition, sequence, root_hash, signed_at)
- RetentionRule(tenant, event_class, duration, legal_hold)

## 4. High-level design

```text
services -> authenticated collectors -> durable append log
                                             |
                            +----------------+----------------+
                            |                                 |
                    immutable archive                    search index
                            |                                 |
                      signed checkpoints <- verifier      query/export API
```

## 5. Critical request flow

1. Producer emits a canonical structured event after an attempted action.
2. Collector authenticates the producer, validates required fields, and assigns ingest sequence.
3. Chain or tree-hash records and publish signed checkpoints to independent storage.
4. Write immutable archive first, then build a replaceable search index.
5. Queries authorize tenant scope and return evidence with integrity verification metadata.

## 6. Deep dive

- Hash chaining detects removal or modification but partitions need signed boundary checkpoints.
- The archive is the source of truth; search indexes may be rebuilt.
- Record both event time and trusted ingest time to expose clock skew.
- Redact sensitive values at production because append-only storage is difficult to correct.

## 7. Scaling, failures, and observability

- Producers buffer briefly, but security-critical actions may fail closed if auditing cannot be accepted.
- Reconcile producer sequence gaps and alert on missing expected events.
- Verify random archived segments continuously and practice full index rebuilds.
- Monitor ingest gaps, verification failures, index lag, export age, and unauthorized query attempts.

## 8. Security and privacy

- Separate write, query, export, and retention permissions.
- Encrypt per tenant, protect signing keys, and require dual control for legal-hold changes.
- Never record secrets, tokens, or unnecessary content in an immutable event.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Database update history | Queryable but administrators may modify the same system. |
| Independent immutable archive | Stronger evidence with more pipeline complexity. |
| Hash chain | Simple sequential verification but partition boundaries need care. |
| Merkle batches | Efficient proofs with batch latency. |

## 10. 60-second interview summary

Authenticated producers append canonical events to a durable log and immutable archive. Hash chains or Merkle checkpoints make tampering detectable, while a rebuildable tenant-isolated index supports search. Retention and export are audited privileged operations.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

