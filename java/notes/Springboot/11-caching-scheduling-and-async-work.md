# 11 - Caching, Scheduling, and Async Work

## 1) Caching

```java
@Service
final class CatalogService {
    @Cacheable(cacheNames = "products", key = "#id")
    ProductResponse find(long id) {
        return loadFromDatabase(id);
        // Result: subsequent calls with the same id can return the cached response.
    }

    @CacheEvict(cacheNames = "products", key = "#id")
    void evict(long id) {
        // Result: the cached product for id is removed after successful invocation.
    }
}
```

Enable caching with `@EnableCaching`. Define eviction, size, expiry, consistency, and failure behavior. Never cache security decisions or sensitive data without a deliberate threat analysis.

## 2) Scheduling

```java
@Component
final class CleanupJob {
    @Scheduled(cron = "0 0 2 * * *", zone = "UTC")
    void removeExpiredData() {
        System.out.println("cleanup started");
        // Output daily at 02:00 UTC: cleanup started
    }
}
```

Enable scheduling with `@EnableScheduling`. In a multi-instance deployment, every instance may run the job; use a distributed scheduler or lock when execution must be singular.

## 3) Async Methods

```java
@Service
final class ReportService {
    @Async("reportExecutor")
    CompletableFuture<String> generate() {
        return CompletableFuture.completedFuture("report-ready");
        // Result: caller receives a future completed with report-ready.
    }
}
```

Configure a bounded executor and rejection policy. Proxy-based `@Async` does not apply to ordinary self-invocation.

## 4) Choose the Correct Tool

- cache: reuse an expensive result
- scheduler: initiate time-based work
- async executor: move bounded in-process work off the caller thread
- queue: durable decoupled processing across processes
- virtual thread: scale blocking I/O while retaining synchronous control flow

Do not return success before critical work is durable. In-memory async work is lost if the process stops.
