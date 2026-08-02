# Design a Frontend Observability and Safe-Release Platform

> **Difficulty:** Hard  
> **Main focus:** RUM, source maps, canaries, rollback

## Interview prompt

Design the platform that measures browser health and safely rolls out frontend releases across many applications.

## 1. Clarify the experience

**What I would say first:** Frontend telemetry must connect user experience to an exact release without collecting sensitive content. Releases need progressive exposure and automatic stop signals.

### Functional requirements

- Collect errors, performance, navigation, and product health signals.
- Symbolicate stack traces with protected source maps.
- Compare canary and baseline releases by browser, region, and route.
- Stop or roll back harmful releases quickly.

### Browser and product constraints

- Telemetry runs on the user's critical path and must be tiny.
- Browsers close, block requests, and vary widely.
- High-cardinality URLs and personal data create privacy risk.

## 2. State and API contracts

- Client event {app, release, routeTemplate, sessionSampleId, type, metrics, traceId}
- POST /v1/rum-events accepts compressed batches with strict schemas
- Release manifest maps asset hashes to release and protected source maps

## 3. Frontend architecture

```text
browser SDK -> local buffer/sampler -> edge collector -> event stream
                                                        |
                                      +-----------------+----------------+
                                      |                                  |
                                error grouping                     RUM aggregates
                                      |                                  |
source map vault -> symbolicator -----+-> release health/alerts <--------+
CI/CD -> canary controller -> CDN asset versions -> promote/rollback
```

## 4. Critical user flow

1. Build uploads private source maps and a release manifest before deployment.
2. Canary publishes immutable assets and routes a small stable cohort to the new release.
3. Browser SDK batches schema-validated sampled events with release ID.
4. Pipeline groups symbolicated errors and aggregates Web Vitals by route and segment.
5. Guardrails pause promotion or switch the HTML/manifest back to the prior asset version.

## 5. Deep dive

- Use route templates, not raw URLs, to control cardinality and personal data.
- Errors need grouping fingerprints that survive minification but separate distinct failures.
- Compare canary to simultaneous control because browser and traffic mix change over time.
- Rollback HTML and asset references; immutable old assets remain available during propagation.

## 6. Performance, resilience, and observability

- Load the SDK asynchronously, cap buffer memory, sample normal sessions, and retain rare fatal errors.
- Use sendBeacon or keepalive delivery only for small final batches.
- Alert on statistically and practically meaningful changes, not every fluctuation.
- Track SDK overhead, event loss, symbolication success, error-free sessions, LCP, INP, CLS, and rollback time.

## 7. Security and accessibility

- Allowlist fields, scrub text and query values, and honor consent and deletion policy.
- Protect source maps because they reveal source code.
- Ensure rollback controls require strong authentication and audited access.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Collect every session | Maximum visibility with high cost and privacy risk. |
| Adaptive sampling | Efficient but requires correct weighting. |
| Mutable assets | Easy overwrite but unsafe caches and rollback. |
| Immutable hashed assets | Reliable release identity and storage overhead. |

## 9. 60-second interview summary

CI publishes immutable assets, private source maps, and a release manifest. A small RUM SDK sends sampled schema-safe events tied to release IDs, canaries are compared with concurrent controls, and guardrails can stop promotion or restore the prior manifest quickly.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

