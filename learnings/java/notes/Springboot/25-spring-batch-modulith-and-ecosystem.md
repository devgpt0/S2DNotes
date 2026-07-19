# 25 - Spring Batch, Modulith, and Advanced Ecosystem

## What, Why, and How

- **Batch:** restartable bulk processing when a request is the wrong lifecycle. Model job/step state and idempotent chunks.
- **Modulith:** enforce/test module boundaries while keeping one deployment and local transactions.
- **Integration:** implement message channels, routers, transformers, and adapters for integration flows.
- **Cloud:** add only the distributed configuration/gateway/discovery/resilience capability the platform actually needs.
- **GraphQL:** expose a typed client-selected graph while enforcing batching, authorization, and query limits.

## Spring Batch

Spring Batch handles restartable, observable bulk processing through jobs, steps, readers, processors, writers, and a job repository.

```text
Job -> Step -> read chunk -> process items -> write chunk -> commit -> repeat
# Result: completed chunk progress is stored so restart can continue according to job configuration.
```

Interview topics:

- chunk vs tasklet processing
- job instance, job execution, step execution
- identifying job parameters
- restartability and idempotent writers
- skip, retry, rollback, and dead-letter policy
- partitioning and remote chunking
- bounded commit interval and memory

Do not use a web request thread to process a large import synchronously.

## Spring Modulith

Spring Modulith helps enforce modules inside one Spring Boot deployment and supports module-scoped testing, documentation, and event-driven interaction.

```java
@ApplicationModuleTest
class OrderModuleTest {
    @Test
    void moduleStarts() {
        System.out.println("order module started");
        // Test output: the order application module context starts successfully.
    }
}
```

A modular monolith preserves local transactions and simple operations while creating boundaries that can later support extraction.

## Spring Integration

Implements Enterprise Integration Patterns such as channels, routers, transformers, filters, splitters, aggregators, and adapters. Use it when an integration flow is clearer as messaging components than imperative orchestration.

## Spring Cloud

Common modules cover gateway, configuration, service discovery integrations, circuit breakers, contracts, streams, and Kubernetes support. Adopt individual capabilities based on platform needs; do not add the whole ecosystem by default.

## GraphQL

GraphQL lets clients select fields through a typed schema. Prevent N+1 with batching/data loaders, enforce authorization per field/resource, limit query depth/complexity, and avoid exposing persistence entities directly.

## Selection Guide

- Spring MVC: blocking request/response APIs
- WebFlux: end-to-end non-blocking reactive workloads
- Batch: restartable bulk jobs
- Kafka/Stream: durable asynchronous events
- Modulith: enforced modules in one deployment
- Integration: message-oriented integration workflows
- Spring AI: portable model, tool, memory, RAG, and MCP integrations
