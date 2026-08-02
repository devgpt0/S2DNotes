# LLM Serving

## Idea

LLM serving schedules memory-heavy autoregressive workloads across accelerators.
Prefill processes the prompt; decode generates tokens one step at a time. Tail
latency, KV-cache memory, batching, and overload control drive the design.

## Visual model

```text
client -> auth/quota -> model router -> request scheduler
       -> GPU workers: prefill -> KV cache -> continuous decode -> token stream
```

## Design steps

1. Define models, context/output limits, TTFT, inter-token latency, throughput, and cost.
2. Route by model/version/adapter/capability and warm availability.
3. Use continuous/dynamic batching while protecting latency classes.
4. Budget KV-cache memory and reject/truncate before OOM.
5. Stream tokens with cancellation and stop generation promptly on disconnect.
6. Autoscale from queue delay, tokens/sec, memory, and warm-up time.
7. Apply admission control before saturation.

## When to use it

Self-host when data control, customization, predictable volume, or unit economics
justify GPU operations. Managed APIs are simpler for variable or early workloads.

## Trade-offs

Larger batches increase throughput but delay individual requests. Quantization
reduces memory/cost but may affect quality. More model replicas reduce queueing
but consume expensive idle capacity.

## Failure modes

- OOM: context limits, memory-aware scheduler, graceful rejection.
- Hot model/adapter: weighted routing and reserved capacity.
- Worker death: fail in-flight streams explicitly; retry only safe requests.
- Overload: priority queues, token quotas, maximum queue age, load shedding.

## Common mistakes

- Autoscaling on GPU utilization alone.
- Mixing interactive and batch jobs without priority isolation.
- Ignoring tokenizer/model-version compatibility.
- Continuing expensive generation after the client cancels.
