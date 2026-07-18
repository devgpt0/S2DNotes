# 15 - Architecture, Interview Revision, and Practice

## 1) Request Flow

```text
HTTP request
  -> security filters
  -> controller and DTO validation
  -> transactional service
  -> repository / external adapter
  -> response DTO
  -> HTTP response
# Result: responsibilities stay separated and each boundary can be tested.
```

## 2) Example Service Boundary

```java
@Service
final class CreateOrderService {
    private final OrderRepository orders;
    private final InventoryGateway inventory;

    CreateOrderService(OrderRepository orders, InventoryGateway inventory) {
        this.orders = orders;
        this.inventory = inventory;
    }

    @Transactional
    OrderResponse create(CreateOrderCommand command) {
        inventory.requireAvailable(command.productId(), command.quantity());
        Order saved = orders.save(Order.create(command));
        return OrderResponse.from(saved);
        // Result: one validated business operation returns a response DTO.
    }
}
```

The controller translates HTTP into a command. The service owns the use case. The entity protects domain state. The repository persists it.

## 3) Interview Quick Answers

- Auto-configuration creates beans conditionally from the classpath, existing beans, and configuration.
- Constructor injection makes dependencies explicit and supports immutable fields.
- A starter supplies a curated dependency set; the Boot BOM manages compatible versions.
- `@Transactional` is normally proxy-based; self-invocation bypasses the proxy.
- DTO validation protects the HTTP boundary; database constraints protect stored integrity.
- `@SpringBootTest` loads the full context; slice tests load a focused part.
- Authentication identifies the caller; authorization checks permission.
- Actuator provides operational endpoints; exposure and access must be restricted.
- Caching needs expiry and invalidation; async execution needs bounded resources and durability decisions.
- An outbox closes the database-to-broker dual-write gap.

## 4) Practice Project

Build a product-order API with:

1. strict create/update DTOs and Problem Details
2. products and orders persisted with Flyway migrations
3. pagination with allow-listed sorting
4. optimistic locking for inventory
5. JWT resource-server authorization
6. unit, MVC, repository, and container-backed integration tests
7. metrics for order outcomes without high-cardinality tags
8. an outbox event for completed orders
9. graceful shutdown and a buildpack container image

Every invalid state must fail explicitly, and every external call must have a timeout.

## 5) Final Review Checklist

- controllers contain no business logic
- DTOs and configuration are strictly validated
- transactions wrap complete database use cases
- queries are bounded and inspected for N+1 behavior
- authorization protects both actions and object ownership
- errors do not leak internals
- logs contain operational context but no secrets or personal data
- tests cover success, validation, authorization, conflict, and rollback paths
- production limits, health probes, migrations, and observability are defined
