# 12 - Calling External HTTP Services

## What, Why, and How

**What:** An HTTP client adapter translates a typed application call into a remote request and validates the response.

**Why:** Network calls can fail partially, return invalid data, or complete after the caller times out. Scattered calls create inconsistent error/security handling.

**How:** Create one typed client per dependency, configure trusted base URL and deadlines, validate data, retry only safe transient operations, isolate capacity, and publish metrics.

## 1) `RestClient`

Spring Boot configures a `RestClient.Builder` that can be customized centrally.

```java
@Component
final class InventoryClient {
    private final RestClient restClient;

    InventoryClient(RestClient.Builder builder, InventoryProperties properties) {
        this.restClient = builder.baseUrl(properties.baseUrl()).build();
    }

    InventoryResponse find(long productId) {
        return restClient.get()
                .uri("/api/inventory/{id}", productId)
                .retrieve()
                .body(InventoryResponse.class);
        // Result: HTTP 2xx JSON is decoded as InventoryResponse; error statuses raise a client exception.
    }
}
```

Use URI templates. Never concatenate untrusted values into a full URL.

## 2) Strict Response DTO

```java
record InventoryResponse(long productId, int available) {
    InventoryResponse {
        if (productId <= 0 || available < 0) {
            throw new IllegalArgumentException("invalid inventory response");
        }
        // Result: invalid downstream data fails immediately.
    }
}
```

External responses are untrusted input and require validation.

## 3) Timeouts

Configure connection, response, and overall operation deadlines. A client without timeouts can exhaust request threads and connection pools.

```yaml
inventory:
  base-url: https://inventory.internal
  timeout: 2s
# Result: the typed client configuration receives an explicit two-second deadline.
```

## 4) Retries

Retry only transient failures, with a small attempt limit, exponential backoff, jitter, and an overall deadline. Do not retry non-idempotent operations unless an idempotency key and server contract make it safe.

## 5) Resilience Checklist

- validate the scheme and host to prevent SSRF
- restrict redirects
- limit response size
- isolate connection pools and concurrency where needed
- propagate trace context
- use circuit breaking only with measured thresholds and a defined fallback
- never log authorization headers or complete sensitive payloads
- expose dependency latency and failure metrics
