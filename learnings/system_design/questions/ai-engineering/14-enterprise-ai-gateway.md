# Design an Enterprise AI Gateway and Model Router

> **Difficulty:** Hard  
> **Main focus:** provider routing, policy, budgets, reliability

## Interview prompt

Design one enterprise API that safely routes AI requests across internal and external models.

## 1. Clarify the product and success criteria

**What I would say first:** The gateway provides stable contracts, policy, observability, and routing; it must not pretend different models have identical behavior. Data policy constrains eligible routes before cost optimization.

### Functional requirements

- Expose stable chat, embedding, and multimodal APIs.
- Route by capability, residency, quality, latency, availability, and cost.
- Enforce tenant budgets, content policy, and provider permissions.
- Support fallback, canary, audit, and usage attribution.

### AI and product constraints

- Providers have different schemas, limits, safety behavior, and streaming semantics.
- Retrying after partial output can duplicate or contradict content.
- Sensitive prompts may be forbidden from external providers.

## 2. Contracts and data

- POST /v1/ai/generate {capability, messages, constraints, maxCost, requestId}
- RoutePolicy {tenant, dataClass, allowedModels, residency, qualityTier, fallback}
- Trace records normalized request metadata, selected route, versions, usage, latency, and policy decision

## 3. High-level design

```text
applications -> auth/schema -> data classification/policy
                                      |
                               capability router
                         / internal models / providers
                         |        |             |
                    adapters  circuit health  quotas
                         \        |             /
                         normalized stream/usage
                                      |
                         traces, budgets, evaluation
```

## 4. Critical request flow

1. Authenticate tenant, validate exact typed input, and classify data sensitivity.
2. Filter routes by policy, residency, modality, context size, and required quality.
3. Choose among eligible routes using health, latency, cost, and experiment policy.
4. Normalize provider streaming and finish reasons without hiding unsupported semantics.
5. Record usage and outcome; fallback only when the operation can safely restart.

## 5. Quality and evaluation

- Maintain task-specific routing evaluations rather than one model leaderboard.
- Shadow candidates on consented traffic and compare quality, safety, latency, and cost.
- Continuously detect provider behavior or version drift.
- Expose selected model/version when product or compliance requires transparency.

## 6. Reliability, scale, observability, and cost

- Use circuit breakers, provider-specific concurrency limits, and bounded admission queues.
- Cache embeddings or deterministic results only with strict tenant and version keys.
- Set per-request and per-tenant token, tool, and monetary budgets.
- Track route share, fallback, policy denies, provider errors, latency, quality proxy, and cost/success.

## 7. Safety, security, and privacy

- Do not send restricted data to ineligible providers; redact only when business semantics permit.
- Keep provider keys in the gateway, not applications, and isolate tenant logs.
- Normalize output safely but preserve provider safety signals and audit decisions.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| One forced model | Simple but creates lock-in and weak task fit. |
| Policy-aware routing | Resilient and cost-aware with evaluation complexity. |
| Transparent provider quirks | More application work but honest semantics. |
| Lowest-common-denominator API | Simple contract that hides useful capabilities. |

## 9. 60-second interview summary

A policy layer first removes models that violate data, residency, or capability constraints. A health- and evaluation-aware router chooses among eligible providers, adapters preserve explicit semantics, and budgets, traces, canaries, and safe fallback centralize enterprise control.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

