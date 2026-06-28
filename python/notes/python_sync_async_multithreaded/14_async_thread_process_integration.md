# Async + Thread + Process Integration Playbook

## 1) Why Hybrid Systems Exist

Real systems often combine:
- async for network I/O
- thread pool for blocking SDKs
- process pool for CPU-heavy transformations

## 2) Stage-Based Model Selection

Example:
1. async fetch stage (network bound)
2. thread-offloaded parse stage (blocking library)
3. process pool transform stage (CPU bound)
4. async persist stage (DB/network)

## 3) Integration Boundaries

Key rules:
- keep payloads compact across boundaries
- avoid sharing mutable state across threads/processes
- define explicit timeout and cancellation policy per stage

## 4) Async with Thread Pool

Use:
- `asyncio.to_thread`
- `loop.run_in_executor`

for blocking calls inside async services.

## 5) Async with Process Pool

Use process pool for CPU-heavy chunks.
Ensure worker functions are pickle-safe and top-level.

## 6) Error Propagation Strategy

Define:
- fail-fast vs partial-success behavior
- retry policy per stage
- fallback behavior when one stage degrades

## 7) Shutdown Coordination

1. stop ingress
2. cancel async producers
3. drain worker queues
4. close thread/process pools
5. wait bounded time and report leftovers

## 8) Capacity Planning Basics

Track:
- per-stage throughput
- queue pressure by stage
- end-to-end latency

Scale the bottleneck stage, not all stages equally.

## 9) Interview Answer Structure for Hybrid Architecture

1. classify each stage by bottleneck type
2. select concurrency model per stage
3. define reliability controls (timeouts, retries, backpressure)
4. define observability metrics
5. define shutdown strategy
