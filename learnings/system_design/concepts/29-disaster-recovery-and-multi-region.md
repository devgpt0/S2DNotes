# Disaster Recovery and Multi-Region Design

## Idea

Disaster recovery (DR) restores service and data after a large failure. Define
recovery point objective (RPO: acceptable data loss) and recovery time objective
(RTO: acceptable downtime) before choosing architecture.

## Visual model

```text
active region -> replicated data -> standby region
       |             |
       +-> backups in separate account/region -> tested restore
```

## Design steps

1. Classify services and data by RPO/RTO and business impact.
2. Choose backup/restore, pilot light, warm standby, or active-active.
3. Replicate dependencies, configuration, secrets, DNS/routing, and artifacts.
4. Prevent split brain with ownership epochs and explicit failover authority.
5. Automate recovery, reconciliation, and controlled failback.
6. Run game days and restore drills with measured RPO/RTO.

## When to use each mode

- Backup/restore: low cost, long RTO.
- Warm standby: reduced RTO with partial idle capacity.
- Active-passive: simpler writes and failover.
- Active-active: lowest regional outage impact; hardest data conflicts.

## Trade-offs

Lower RPO/RTO costs more and increases operational complexity. Active-active
does not remove consistency decisions; it makes them unavoidable.

## Critical controls

- Immutable/versioned backups with separate credentials.
- Restore verification, not only backup-success metrics.
- Capacity reserved in the recovery region.
- Data reconciliation after failover and failback.

## Common mistakes

- Equating asynchronous replicas with backups.
- Designing failover but not failback.
- Depending on the failed region for DNS, secrets, or deployment control.
- Claiming zero RPO across distant regions without paying synchronous latency.
