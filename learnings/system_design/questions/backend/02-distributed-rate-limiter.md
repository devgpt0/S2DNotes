# Design a Distributed Rate Limiter

> **Difficulty:** Medium  
> **Main focus:** atomic counters, fairness, failure policy

## Interview prompt

Design a rate limiter shared by many API gateway instances.

## 1. Clarify the scope

**What I would say first:** First I will clarify the policy key, allowed burst, enforcement location, and whether failure should allow or deny traffic.

### Functional requirements

- Limit by user, API key, IP, tenant, endpoint, or a combination.
- Support requests per second and controlled bursts.
- Return remaining quota and retry information.
- Apply policy changes safely across gateway instances.

### Out of scope for the first version

- Billing-grade quota reconciliation is separate from immediate traffic protection.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 2 million requests per second across regions.
- A network call on every request is expensive, so use local leases or regional enforcement where accuracy permits.
- Hot tenants create hot keys; shard by a stable hash and isolate very large customers.

## 3. API and data model

### Main contracts

- check(key, policyId, cost=1) -> {allowed, remaining, retryAfterMs}
- PUT /v1/policies/{id} {algorithm, limit, window, burst, failMode}

### Important data

- Policy(policy_id, scope, rate, burst, algorithm, version, fail_mode)
- Counter state in a fast atomic store; durable policy state in a database

## 4. High-level design

```text
client -> gateway -> local policy cache -> limiter client
                                      |
                                      +-> regional limiter shards -> atomic state store
                                                   |
policy API -> policy database -> change stream ----+
```

## 5. Critical request flow

1. Gateway builds the canonical limit key from authenticated identity and endpoint.
2. Load a versioned policy from local cache.
3. Atomically consume a token or update the sliding-window counter.
4. Allow the request or return 429 with Retry-After.
5. Emit decision metrics without logging sensitive identifiers.

## 6. Deep dive

- Token bucket is the default: tokens refill at a fixed rate and unused tokens permit a bounded burst.
- Use one atomic script or transaction per decision so concurrent gateways cannot overspend.
- For global limits, allocate regional token leases; this trades small temporary overshoot for lower latency.
- Hash-tag related keys only when multi-key atomicity is truly required.

## 7. Scaling, failures, and observability

- Choose fail-open for low-risk availability paths and fail-closed for expensive or security-sensitive operations.
- Bound local emergency tokens so a store outage cannot create unlimited traffic.
- Use timeouts, circuit breakers, and stale-but-versioned policy cache.
- Alert on allowed, blocked, store latency, policy-cache age, and estimated overshoot.

## 8. Security and privacy

- Derive user and tenant keys from trusted authentication, never client headers alone.
- Authorize policy changes, audit them, and roll out versions gradually.
- Protect against cardinality attacks that create unbounded counter keys.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Exact global limit | Stronger control but adds cross-region latency and a global dependency. |
| Regional leases | Fast and available but may temporarily overshoot. |
| Fixed window | Simple but bursts at boundaries. |
| Token bucket | Good burst control with small atomic state. |

## 10. 60-second interview summary

I enforce a token bucket near the gateway using atomic regional shards and versioned policy caches. Global quotas use bounded regional leases, and the fail-open or fail-closed behavior is part of each policy rather than an accident.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

