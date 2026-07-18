# 19 - Kafka and Reliable Messaging

## Beginner Meaning

A producer writes records to a topic. Kafka divides the topic into partitions. Consumers read records, and a consumer group shares partitions between its members. Kafka keeps records so consumers can recover and read again.

The most important beginner rule: delivery can happen more than once, so processing must be idempotent.

## Core Model

- topic contains ordered partitions
- each record has an offset within one partition
- records with the same key route consistently when partitioning is stable
- a consumer group assigns a partition to at most one consumer in that group at a time
- ordering is per partition, not per topic

## Producer

```java
CompletableFuture<SendResult<String, OrderCreated>> future = kafkaTemplate.send(
        "orders.created", order.customerId(), new OrderCreated(order.id()));
future.whenComplete((result, failure) -> {
    if (failure != null) {
        System.out.println("publish failed");
    } else {
        System.out.println("published offset=" + result.getRecordMetadata().offset());
    }
});
// Output: published offset=<broker offset>, or publish failed.
```

Do not treat an asynchronous send call as durable success until its future completes successfully.

## Consumer

```java
@KafkaListener(topics = "orders.created", groupId = "billing")
void consume(OrderCreated event) {
    billingService.processIdempotently(event);
    // Result: the event is processed once logically even if Kafka redelivers it.
}
```

At-least-once delivery requires idempotent handling. Store an event ID or enforce a domain uniqueness constraint in the same local transaction as the effect.

## Delivery and Failure

- producer idempotence reduces duplicate records from retries
- transactions can atomically write Kafka records and offsets within Kafka boundaries
- database plus Kafka still needs outbox/CDC or another dual-write solution
- retry topics delay transient failures
- dead-letter topics isolate permanent failures for investigation
- poison messages need bounded attempts and actionable metadata

## Schema Evolution

Use versioned schemas. Add optional fields compatibly, define default behavior, retain old readers during deployment, and never reuse a field with different meaning.

## Operational Signals

Monitor consumer lag, rebalance frequency, processing latency, retry/DLT rate, broker acknowledgements, partition skew, and oversized messages.
