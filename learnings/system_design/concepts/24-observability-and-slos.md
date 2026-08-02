# Observability and SLOs

## Idea

Observability helps explain system behavior from metrics, logs, and traces. An
SLO states the reliability users should receive.

## Classroom board

```text
request -> trace across services
services -> metrics (rate/errors/duration/saturation)
events -> structured logs with correlation ID
SLO breach risk -> actionable alert
```

## Design steps

1. Define user-journey SLIs and targets.
2. Instrument boundaries with stable names and low-cardinality labels.
3. Centralize structured logs and propagate trace context.
4. Alert on error-budget burn and symptoms, then maintain runbooks.

## When to use it

Every production system needs it from the first release.

## Trade-offs and mistakes

More telemetry costs money and can expose data. Avoid PII/secrets, unbounded
metric labels, alerting on every fluctuation, and dashboards without ownership.
