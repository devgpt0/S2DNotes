# Inference Optimization and GPU Scheduling

## Idea

Inference optimization serves the required model quality within latency, throughput, memory, and cost limits.

GPU scheduling decides which work runs on scarce accelerators and prevents one workload from harming every other workload.

## Visual model

```text
requests
   |
admission + priority queue
   |
dynamic batcher
   |
GPU scheduler -> model workers -> streamed response
   |                 |
quota / fairness   metrics
```

## Design steps

1. Define separate targets for time to first token, total latency, throughput, quality, and cost.
2. Measure a correct baseline before applying optimizations.
3. Batch compatible requests without violating latency targets.
4. Reuse prefix and key-value caches only across requests with safe isolation.
5. Test quantization, compilation, speculative decoding, or smaller models against quality gates.
6. Use tensor or pipeline parallelism only when the model cannot fit or meet throughput on one device.
7. Schedule by priority, deadline, model, and memory requirement.
8. Enforce queue limits, quotas, cancellation, and overload responses.

## Pattern clues

Consider these techniques when:

- GPU memory limits model size or batch size;
- latency rises sharply during traffic bursts;
- accelerators are idle while requests are queued;
- many adapters or models compete for the same devices;
- repeated prefixes consume most computation.

## Failure handling

- Reject excess work before queues grow without bound.
- Remove cancelled requests from batches quickly.
- Replace unhealthy workers and reload models from verified artifacts.
- Keep fallback capacity for critical traffic.
- Monitor out-of-memory errors, fragmentation, cache use, and queue time.

## Trade-offs

- Larger batches improve throughput but can increase latency.
- Quantization reduces memory and cost but may reduce quality.
- Model parallelism enables larger models but adds communication overhead.
- More resident models reduce cold starts but reserve expensive memory.

## Common mistakes

- Measuring average latency without tail latency.
- Treating all requests as equal during overload.
- Optimizing tokens per second while quality quietly falls.
- Ignoring GPU memory fragmentation and model load time.
- Sharing caches across tenants without strict isolation.
