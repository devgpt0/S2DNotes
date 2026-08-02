# Design a Multi-Region Active-Active Service

> **Difficulty:** Hard  
> **Main focus:** data ownership, conflict handling, regional failure

## Interview prompt

Evolve a stateful SaaS product so users can read and write through multiple regions.

## 1. Clarify the scope

**What I would say first:** Active-active is a data-consistency decision, not only traffic routing. I will classify data by conflict tolerance and assign ownership where strong ordering is required.

### Functional requirements

- Route users to a healthy nearby region.
- Continue defined operations during a regional outage.
- Replicate durable data and prevent silent conflict loss.
- Meet explicit recovery time and recovery point objectives.

### Out of scope for the first version

- Zero data loss and zero downtime for every operation are not assumed without cost discussion.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume three regions and millions of tenants.
- Cross-region round trips are much slower than in-region database calls.
- Region evacuation can double surviving-region traffic.

## 3. API and data model

### Main contracts

- Existing product APIs include operation IDs and entity versions.
- GET /health/region returns dependency readiness, not only process liveness.
- Administrative failover actions require audited control-plane commands.

### Important data

- TenantHome(tenant_id, home_region, epoch)
- Operation(operation_id, entity_id, region, logical_time, idempotency_key)
- ReplicationCheckpoint(stream, source_region, destination_region, offset)

## 4. High-level design

```text
global traffic manager
      |------------------|------------------|
   region A           region B           region C
 gateway/service     gateway/service     gateway/service
      |                  |                  |
 regional data <-> async replication <-> regional data
      |
global control plane: tenant ownership, epochs, failover, config
```

## 5. Critical request flow

1. Route a tenant to its current home region for ordered writes.
2. Commit locally, publish an operation log, and replicate asynchronously.
3. Serve safe reads locally with visible staleness rules.
4. On region failure, fence the old ownership epoch before promoting a new home.
5. Reconcile replayed idempotent operations and rebuild replicas after recovery.

## 6. Deep dive

- Classify data: immutable events replicate easily; counters may use CRDTs; payments need one writer or consensus.
- Epoch fencing prevents an isolated old region from accepting valid-looking writes after failover.
- Do not claim active-active if all writes synchronously depend on one distant primary.
- Capacity must reserve for evacuation, and failover must be exercised regularly.

## 7. Scaling, failures, and observability

- Define behavior for network partition separately from complete region loss.
- Use bounded-staleness indicators and disable unsafe writes when ownership is uncertain.
- Restore traffic gradually and compare data checksums before full rejoin.
- Monitor replication lag, conflict count, regional saturation, failover time, and lost-operation estimate.

## 8. Security and privacy

- Keep data residency rules in routing and replication policy.
- Use region-scoped credentials, encrypted replication, and audited failover authority.
- Test key availability and identity dependencies during isolation.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Single home-region writer | Clear ordering with remote-write latency for traveling users. |
| Multi-writer conflict resolution | Low local latency but complex business semantics. |
| Synchronous replication | Lower data loss with higher latency and partition unavailability. |
| Asynchronous replication | Fast local writes with a nonzero recovery point. |

## 10. 60-second interview summary

I route ordered writes to a fenced tenant home region and asynchronously replicate an operation log. Data types with safe merge rules can be multi-writer, while financial or invariant-heavy data remains single-owner. Failover changes epochs and is capacity-tested.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

