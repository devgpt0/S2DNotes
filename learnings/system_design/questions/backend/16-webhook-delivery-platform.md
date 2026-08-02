# Design a Webhook Delivery Platform

> **Difficulty:** Medium  
> **Main focus:** at-least-once delivery, signing, retries

## Interview prompt

Design a platform that reliably delivers product events to customer HTTP endpoints.

## 1. Clarify the scope

**What I would say first:** Internet delivery cannot be exactly once. I will provide at-least-once attempts, stable event IDs, signatures, ordering boundaries, and a replay UI.

### Functional requirements

- Register endpoints and event subscriptions.
- Deliver signed HTTP requests with retries.
- Expose attempt history, endpoint health, and manual replay.
- Isolate tenants and prevent one slow endpoint from blocking others.

### Out of scope for the first version

- Transforming events with arbitrary customer code is out of scope.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume billions of deliveries per day with highly variable endpoint quality.
- Queueing, retry amplification, and slow connections dominate resources.
- Per-endpoint ordering may be optional because it reduces throughput.

## 3. API and data model

### Main contracts

- POST /v1/endpoints {url, eventTypes}
- GET /v1/events/{eventId}/attempts
- POST /v1/events/{eventId}/replay

### Important data

- Endpoint(endpoint_id, tenant_id, url, encrypted_secret, status, version)
- WebhookEvent(event_id, tenant_id, type, payload_ref, created_at)
- Delivery(event_id, endpoint_id, attempt, next_attempt_at, state, response_code)

## 4. High-level design

```text
product services -> event bus -> subscription router -> endpoint queues
                                                        |
delivery workers -> DNS/egress policy -> customer endpoints
        |
        +-> attempt store -> dashboard/replay
        +-> retry scheduler / dead letter
```

## 5. Critical request flow

1. Persist or consume a product event with a globally stable event ID.
2. Resolve active subscriptions and enqueue one delivery per endpoint.
3. Sign timestamp plus raw body using the endpoint secret.
4. Send with strict connect and response timeouts; record the bounded response metadata.
5. Retry transient outcomes with jitter, then disable or dead-letter persistently failing endpoints.

## 6. Deep dive

- Partition queues by endpoint hash and cap concurrent requests per endpoint.
- Use an outbound proxy that re-resolves DNS and blocks private or metadata networks.
- Provide event ID and attempt number so consumers can deduplicate.
- Preserve per-endpoint order only for event types that require it; later events otherwise need not wait.

## 7. Scaling, failures, and observability

- Circuit-break unhealthy endpoints and run occasional probes.
- Retry schedules have maximum age and attempts to prevent infinite backlog.
- Replay creates a new delivery attempt but keeps the original event ID.
- Monitor success latency, endpoint queue age, retries, disabled endpoints, and egress saturation.

## 8. Security and privacy

- Verify endpoint ownership, encrypt secrets, rotate them, and sign raw bytes.
- Defend against SSRF, DNS rebinding, oversized responses, and redirect abuse.
- Redact response bodies and customer payloads from general logs.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| At-least-once | Practical reliability with consumer deduplication. |
| Per-endpoint strict order | Simpler consumer state but head-of-line blocking. |
| Concurrent delivery | Higher throughput but possible reordering. |
| Store full responses | Useful debugging but privacy and storage risk. |

## 10. 60-second interview summary

Product events fan out into isolated endpoint queues. Workers sign each attempt, enforce egress security and timeouts, then retry with bounded backoff. Stable event IDs provide deduplication, and operators can inspect and replay deliveries safely.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

