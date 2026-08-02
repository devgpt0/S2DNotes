# Frontend Observability and Safe Releases

## Idea

Frontend failures happen across browsers, devices, networks, and cached versions
that backend telemetry cannot see. Real-user monitoring (RUM) connects errors
and performance to route, release, browser, and user-visible outcome.

## Visual model

```text
browser -> errors + Web Vitals + traces -> telemetry intake
release/flag/version ------------------> dashboards and rollback decision
```

## Design steps

1. Attach release, route, browser, device, and trace/correlation IDs.
2. Capture uncaught errors, rejected promises, failed resources, and API outcomes.
3. Upload private source maps to the error system, not public artifact paths.
4. Sample performance while retaining important errors at higher rates.
5. Roll out with canaries/feature flags and compare guardrail metrics.
6. Provide kill switches and test rollback with service-worker/cache behavior.

## When to use it

Every production frontend. High-traffic or revenue-critical paths need route-level
SLOs, synthetic checks, and release health automation.

## Trade-offs

More session context improves debugging but increases privacy and cost risk.
Session replay should be narrowly scoped, redacted, consent-aware, and retained
briefly.

## Critical signals

- JavaScript error-free sessions and affected users.
- LCP/INP/CLS distributions, not only averages.
- API failure/latency from the browser's view.
- Conversion/task completion by release and experiment.

## Common mistakes

- Logging form values, tokens, or personal page content.
- Alerting on every individual browser error.
- Deploying source maps publicly with original source/secrets.
- Using flags without ownership, expiry, or tested off behavior.
