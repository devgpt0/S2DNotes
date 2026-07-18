# 20 - Microservices and Distributed Systems

## Start with the Problem

A method call inside one process either returns or throws directly. A network call is harder: the request, response, caller, or server can fail independently. A timeout does not tell you whether the server completed the work.

Microservices add independent deployment and ownership, but also add network failure, delayed data, duplicate messages, and operational cost. A modular monolith is the better starting point for many systems.

## Service Boundary

A service should own a cohesive business capability and its data. Splitting by technical layer creates chatty distributed coupling.

## Essential Patterns

- API Gateway: routing, edge authentication, rate limits; not core business logic
- Service Discovery: map logical service names to healthy instances
- Central Configuration and Secrets: externalized, versioned, access-controlled
- Circuit Breaker: stop calls to a persistently failing dependency
- Bulkhead: isolate pools/concurrency by dependency
- Saga: distributed workflow through local transactions and compensation
- Outbox: reliable database-to-broker publication
- Idempotency Key: make retried commands produce one logical effect
- Distributed Tracing: correlate work across boundaries

## Idempotent Command

```java
@PostMapping("/payments")
ResponseEntity<PaymentResponse> create(
        @RequestHeader("Idempotency-Key") UUID key,
        @Valid @RequestBody PaymentRequest request) {
    PaymentResponse response = service.createOnce(key, request);
    return ResponseEntity.ok(response);
    // HTTP 200 returns the same logical result when the same key and request are retried.
}
```

Persist the key, request fingerprint, state, and result atomically. Reject reuse with a different request.

## Consistency

Distributed systems cannot use one local ACID transaction across autonomous stores without major coupling. Define which reads are strongly consistent, eventually consistent, monotonic, or stale-tolerant.

## Failure Questions

- What if the caller times out but the server commits?
- What if a message is delivered twice or out of order?
- What if one saga compensation fails?
- What if DNS returns an unhealthy address?
- What if all instances retry together?
- What data can be stale, and for how long?

## Senior-Level Tradeoff

Start with a modular monolith when one deployment and transaction boundary meet requirements. Extract a service only when independent ownership, scaling, data boundary, reliability, or deployment provides enough value to justify network failure, observability, testing, and operational cost.
