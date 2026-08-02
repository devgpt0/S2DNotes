# LLM Serving

## Idea

LLM serving schedules expensive accelerator work while meeting time-to-first-
token, token throughput, availability, and cost goals.

## Classroom board

```text
API -> auth/quota -> scheduler -> model replicas -> streamed tokens
                    batching       KV cache
fallback/router <- overload/health/cost policy
```

## Design steps

1. Validate model, token limits, tenant quota, and safety policy.
2. Route by capability/region and batch compatible work continuously.
3. Stream output, support cancellation, and bound queues.
4. Autoscale from queue delay and accelerator saturation; canary model versions.

## Trade-offs and mistakes

Larger batches improve throughput but delay first token. Avoid CPU-only scaling
signals, unbounded prompts/outputs, caching private prompts under shared keys,
and retries after partial streamed output without semantics.
