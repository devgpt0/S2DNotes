# Design a Distributed Job Scheduler

> **Difficulty:** Hard  
> **Main focus:** leases, retries, recurring work

## Interview prompt

Design a service for one-time, delayed, recurring, and long-running jobs.

## 1. Clarify the scope

**What I would say first:** The durable job record is the source of truth. Execution is at least once, so job handlers must be idempotent.

### Functional requirements

- Schedule one-time and recurring jobs.
- Dispatch near the requested time across many workers.
- Retry transient failures, cancel jobs, and expose status.
- Recover jobs from crashed workers without double-completing effects.

### Out of scope for the first version

- Arbitrary untrusted code execution requires a separate sandbox design.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume hundreds of millions of scheduled jobs and one million executions per minute.
- Most jobs are far in the future; only a small near-term window needs active scanning.
- Recurring jobs create executions rather than mutating one ambiguous run record.

## 3. API and data model

### Main contracts

- POST /v1/jobs {type, payloadRef, runAt|schedule, retryPolicy}
- POST /v1/jobs/{id}/cancel
- GET /v1/jobs/{id}

### Important data

- Job(job_id, type, schedule, next_run_at, state, version)
- Execution(execution_id, job_id, scheduled_for, state, attempt, lease_until, worker_id)

## 4. High-level design

```text
client -> scheduler API -> job database
                                  |
                                  +-> time buckets / near-term index
                                              |
                                      dispatchers -> durable ready queue
                                                         |
                                                      workers
                                                         |
                                            heartbeat/result/lease expiry
```

## 5. Critical request flow

1. Persist the job and compute its next occurrence.
2. Dispatchers claim due jobs from time buckets with an atomic state change.
3. Create a unique execution and publish it to the ready queue.
4. A worker obtains a lease, heartbeats, executes idempotently, and records the result.
5. Lease expiry makes unfinished work eligible for another attempt.

## 6. Deep dive

- Use coarse buckets for far-future jobs and a precise near-term priority structure.
- Uniqueness on job ID plus scheduled time prevents duplicate recurring executions.
- Separate queue delivery from business-effect idempotency; a worker crash can occur after the effect.
- Define whether missed recurring occurrences are skipped, coalesced, or replayed.

## 7. Scaling, failures, and observability

- Clock skew is bounded by using server time and due-time tolerance.
- Poison jobs stop after a maximum attempt count and move to a dead-letter state.
- Backpressure and tenant quotas prevent one producer from exhausting workers.
- Monitor scheduling delay, queue age, lease expiries, success rate, and retry amplification.

## 8. Security and privacy

- Authorize job types and payload references; do not deserialize arbitrary objects.
- Run high-risk jobs with least-privilege identities and resource limits.
- Audit creation, cancellation, and manual replay.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Database polling | Simple and durable, but inefficient at extreme scale. |
| Hierarchical time buckets | Scalable with more dispatch complexity. |
| Long leases | Fewer duplicates but slower crash recovery. |
| Short leases | Faster recovery with more heartbeat traffic. |

## 10. 60-second interview summary

Jobs and executions are durable, dispatch uses time buckets into a ready queue, and workers run with renewable leases. Delivery is at least once, so execution IDs and business handlers are idempotent, with bounded retries and explicit missed-schedule policy.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

