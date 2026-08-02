# Design a GPU Scheduling Platform

> **Difficulty:** Hard  
> **Main focus:** accelerator allocation, topology, fairness

## Interview prompt

Design a shared platform that schedules training, batch inference, and online inference across GPU clusters.

## 1. Clarify the product and success criteria

**What I would say first:** GPU count is not enough; memory, model size, topology, locality, duration, and service priority determine whether a placement is useful.

### Functional requirements

- Schedule single- and multi-GPU jobs across heterogeneous accelerators.
- Support online services, training, batch jobs, reservations, and quotas.
- Use topology-aware placement and recover from node failure.
- Measure utilization, queue delay, fragmentation, and cost.

### AI and product constraints

- Multi-node jobs may require gang scheduling.
- Idle fragments of GPU memory or topology can leave capacity unusable.
- Preempting training is possible with checkpoints; preempting online requests is disruptive.

## 2. Contracts and data

- JobSpec {workloadType, image, GPUType, GPUCount, memory, topology, priority, checkpointPolicy}
- Allocation {jobId, nodes, devices, lease, placementEpoch}
- Node heartbeat reports device health, free memory, topology, and active allocations

## 3. High-level design

```text
users/services -> admission/quota -> priority queues
                                      |
                             topology-aware scheduler
                          / placement / reservation / preemption
                                      |
                  cluster agents -> GPU nodes / fabric / storage
                       |                  |
                    health             checkpoints
control plane -> inventory, quotas, capacity forecast, cost
```

## 4. Critical request flow

1. Validate image, identity, quota, resource shape, and workload priority.
2. Queue by service class with fairness and reserved emergency capacity.
3. Filter nodes by GPU type, memory, locality, and health; score topology and fragmentation.
4. Atomically lease the complete placement, then launch through node agents.
5. Renew leases, collect health, and checkpoint or reschedule on failure.

## 5. Quality and evaluation

- Benchmark model quality and performance by GPU type and optimization profile.
- Validate that preemption/resume does not change expected training behavior beyond known nondeterminism.
- Use workload traces to test scheduler policies before production.
- Report successful work per GPU-hour, not utilization alone.

## 6. Reliability, scale, observability, and cost

- Gang-schedule distributed jobs so workers do not reserve partial capacity indefinitely.
- Backfill short batch jobs into reservation gaps without threatening online SLOs.
- Defragment by controlled draining and model-aware consolidation.
- Track pending GPU-hours, placement time, topology penalties, OOM, utilization, power, checkpoint recovery, and cost.

## 7. Safety, security, and privacy

- Run signed images with least-privilege identities and isolated tenant storage/network access.
- Protect model artifacts and checkpoint data; audit quota and priority changes.
- Prevent untrusted jobs from accessing host drivers or neighboring device memory.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Strict reservations | Predictable online capacity with lower average utilization. |
| Aggressive sharing | High utilization with noisy-neighbor risk. |
| FIFO | Simple but allows large jobs to block small urgent work. |
| Priority/fair scheduling | Better product outcomes with policy complexity. |

## 9. 60-second interview summary

Admission creates fair priority queues, a topology-aware scheduler atomically leases complete GPU placements, and node agents enforce health and isolation. Gang scheduling, checkpoint-aware preemption, backfill, and fragmentation metrics optimize successful work per GPU-hour.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

