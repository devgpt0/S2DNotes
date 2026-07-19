# 10 - Actuator, Metrics, and Observability

## What, Why, and How

**What:** Actuator exposes operational endpoints. Logs describe events, metrics summarize behavior, and traces connect work across services.

**Why:** Production problems require evidence about traffic, errors, latency, saturation, and dependency behavior.

**How:** Expose only required secured endpoints, instrument bounded technical/business signals, propagate trace context, and alert on sustained user-impacting behavior.

## 1) Actuator Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
    <!-- Result: production endpoints and Micrometer observation support are added. -->
</dependency>
```

## 2) Expose Only Required Endpoints

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      show-details: when_authorized
# Result: only health, info, and prometheus are web-exposed; health details require authorization.
```

Secure management endpoints and preferably isolate them on an internal network or port.

## 3) Custom Metric

```java
@Service
final class OrderMetrics {
    private final Counter completed;

    OrderMetrics(MeterRegistry registry) {
        completed = Counter.builder("orders.completed")
                .description("Completed orders")
                .register(registry);
    }

    void recordCompletion() {
        completed.increment();
        // Result: orders.completed increases by one.
    }
}
```

Never put user IDs, request IDs, email addresses, or other unbounded values in metric tags.

## 4) Logs, Metrics, and Traces

- logs explain discrete events
- metrics show aggregate system behavior
- traces connect work across service boundaries
- correlation IDs help support investigations

```java
private static final Logger LOGGER = LoggerFactory.getLogger(OrderService.class);

LOGGER.info("order completed orderId={}", orderId);
// Output: one structured completion log; never include payment or personal data.
```

## 5) Health Design

Liveness answers whether the process should restart. Readiness answers whether it should receive traffic. Do not make liveness depend on every downstream service or a temporary dependency failure may cause restart loops.

## 6) Operational Signals

Track request latency, error rate, traffic, saturation, JVM memory, GC pauses, thread/connection pools, database latency, queue lag, and business-critical outcomes.
