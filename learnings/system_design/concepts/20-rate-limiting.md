# Rate Limiting

## Idea

A rate limiter protects capacity and enforces fairness by deciding whether a
request consumes an allowed token/quota.

## Visual model

```text
token bucket: tokens refill over time
request -> token exists: allow and consume
        -> empty: reject/defer with retry guidance
```

## Design steps

1. Define identity: user, API key, IP, tenant, route, or combined key.
2. Choose fixed window, sliding window, token bucket, or leaky bucket.
3. Place coarse protection at edge and authoritative quota near service.
4. Make updates atomic and define regional/global behavior.
5. Return `429`, retry metadata, and observable reason codes.

## When to use it

Use token buckets for bursts with a sustained average; sliding windows for a
more accurate count; concurrency limits for expensive in-flight work.

## Trade-offs

Central state is accurate but adds latency/failure dependency. Local limits are
fast but only approximate a global quota.

## Common mistakes

- Limiting by IP behind NAT only.
- Trusting a client-provided identity.
- One hot quota key.
- Rate limit without protecting concurrent expensive requests.
