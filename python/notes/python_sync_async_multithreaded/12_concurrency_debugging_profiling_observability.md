# Concurrency Debugging, Profiling, and Observability

## 1) Observability Requirements

Track at minimum:
- request/job id
- task/thread/process id
- queue depth
- retries/timeouts/failures
- latency percentiles

## 2) Structured Logging

Use structured logs with correlation ids so cross-task flow is traceable.

## 3) Debugging Stuck Systems

Checklist:
1. inspect queue growth and worker states
2. inspect lock contention and waiting points
3. dump thread stacks (`faulthandler`)
4. inspect pending asyncio tasks on shutdown
5. detect pool starvation/deadlock patterns

## 4) Async Debugging Tools

- enable asyncio debug mode when needed
- name tasks
- detect forgotten awaits and long blocking calls in event loop

## 5) Thread/Lock Debugging

- log lock acquisition/release boundaries in suspicious zones
- keep critical sections short
- enforce lock ordering

## 6) Process Pool Diagnostics

- measure serialization overhead
- monitor worker crash/restart patterns
- monitor task runtime skew (stragglers)

## 7) Profiling Concurrency Workloads

Measure:
- throughput
- p50/p95/p99 latency
- CPU utilization
- context switches
- memory per worker

Do baseline before and after architecture changes.

## 8) Key Metrics Dashboard

1. queue length by stage
2. in-flight tasks
3. timeout count
4. retry count
5. success/failure rate
6. shutdown drain duration

## 9) Interview Questions

1. How do you diagnose an async app that "hangs"?
2. How do you prove concurrency change improved performance?
3. Which metrics indicate missing backpressure?
4. How do you identify deadlocks in threaded code?
