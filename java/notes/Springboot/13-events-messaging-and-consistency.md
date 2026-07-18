# 13 - Events, Messaging, and Consistency

## 1) In-Process Domain Event

```java
record OrderCreated(long orderId) {
    OrderCreated {
        if (orderId <= 0) {
            throw new IllegalArgumentException("orderId must be positive");
        }
        // Example event: OrderCreated[orderId=10]
    }
}
```

```java
@Service
final class OrderService {
    private final ApplicationEventPublisher events;

    OrderService(ApplicationEventPublisher events) {
        this.events = events;
    }

    @Transactional
    void create(long orderId) {
        saveOrder(orderId);
        events.publishEvent(new OrderCreated(orderId));
        // Result: the event is published in the current application process.
    }
}
```

## 2) Run After Commit

```java
@Component
final class OrderCreatedListener {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void on(OrderCreated event) {
        System.out.println("committed order=" + event.orderId());
        // Output after successful transaction commit: committed order=10
    }
}
```

An in-process event is not durable. Process failure can still lose after-commit work.

## 3) Transactional Outbox

For reliable external publication:

1. Store the business change and an outbox row in one database transaction.
2. A publisher reads unpublished rows and sends them to the broker.
3. Mark the row published using an idempotent process.
4. Consumers deduplicate by event ID.

```text
orders transaction -> orders row + outbox row -> publisher -> broker -> consumer
# Result: database commit and intent to publish are atomic.
```

## 4) Consumer Rules

- validate schema and version
- make handling idempotent
- define retryable vs permanent failure
- use bounded retries and a dead-letter policy
- commit acknowledgement only after durable processing
- preserve ordering only where the domain requires it
- never assume exactly-once delivery without proving every boundary

Events describe facts that happened, such as `OrderCreated`; commands request actions, such as `CreateOrder`.
