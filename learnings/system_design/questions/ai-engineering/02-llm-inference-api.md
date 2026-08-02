# Design a Multi-Tenant LLM Inference API

> **Difficulty:** Hard  
> **Main focus:** GPU serving, batching, quotas, isolation

## Interview prompt

Design an API that serves multiple language models to many tenants with streaming responses.

## 1. Clarify the product and success criteria

**What I would say first:** The scheduler must balance time to first token, throughput, GPU memory, tenant fairness, and cost. Admission control is necessary because queues are finite.

### Functional requirements

- Serve synchronous and streaming generation.
- Support several models, adapters, priorities, and tenant quotas.
- Meet latency targets while maximizing accelerator use.
- Cancel work, report usage, and survive worker failure.

### AI and product constraints

- Model weights and KV cache consume scarce GPU memory.
- Input and output lengths are unpredictable.
- One tenant or long request must not starve others.

## 2. Contracts and data

- POST /v1/generate {model, messages, maxTokens, temperature, stream, requestId}
- DELETE /v1/requests/{id} cancels queued or active work
- Usage record includes model version, input tokens, output tokens, queue time, GPU time, tenant

## 3. High-level design

```text
clients -> auth/quota -> tokenizer/validator -> admission queues
                                                |
                                         fair scheduler
                                      /         |        \
                              model pool A  model pool B  batch pool
                                  |             |
                         continuous batching + KV cache
                                  |
                           streamed token gateway
control plane -> registry, rollout, capacity, adapters
```

## 4. Critical request flow

1. Authenticate tenant, validate exact model contract, count tokens, and reserve quota.
2. Route to a compatible model pool and priority queue.
3. Scheduler forms continuous batches without violating fairness or deadlines.
4. Worker allocates KV cache, generates tokens, and streams sequenced deltas.
5. Cancellation frees queue and cache state; completion records final usage.

## 5. Quality and evaluation

- Model versions have offline quality, safety, latency, and cost gates before registry promotion.
- Canaries compare request classes and preserve a stable control population.
- Tokenization, chat template, sampling, and stop rules are versioned with the weights.
- Detect output truncation and finish reason rather than treating every stream close as success.

## 6. Reliability, scale, observability, and cost

- Use bounded queues and return explicit overload instead of allowing unlimited latency.
- Warm common models; rarer models may accept cold starts or run on shared pools.
- Retry only before visible output unless the protocol can clearly start a replacement turn.
- Track queue time, time to first token, inter-token latency, throughput, cache utilization, OOM, cancellation, and cost.

## 7. Safety, security, and privacy

- Isolate tenant adapters and KV/prefix caches; never reuse private prefixes across tenants.
- Validate model artifacts, restrict control-plane access, and encrypt prompts according to policy.
- Rate-limit token budgets and expensive parameter combinations.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Large batches | High throughput but greater queue and first-token latency. |
| Dedicated tenant pools | Strong isolation with lower utilization. |
| Shared fair pools | Efficient but require rigorous cache and quota isolation. |
| Many resident models | Few cold starts but expensive reserved memory. |

## 9. 60-second interview summary

A quota-aware admission layer feeds fair bounded queues, and compatible requests use continuous batching on versioned model pools. Cancellation, cache isolation, rollout gates, and overload responses keep GPU use high without sacrificing tenant fairness or correctness.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

