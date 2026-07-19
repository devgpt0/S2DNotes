# 16 - Enterprise and Architectural Patterns

These are not GoF patterns, but they are common in senior Java interviews.

These patterns solve system-level problems. Beginners should first learn controller, service, repository, and one database transaction. Return here after building a small application.

## 1) Layered Architecture

Controller -> application service -> repository. Dependencies point toward domain policy. Layers should reflect responsibilities, not merely create pass-through classes.

```java
record CreateOrderCommand(long customerId) {}
interface OrderRepository { long save(CreateOrderCommand command); }
final class CreateOrderService {
    private final OrderRepository orders;
    CreateOrderService(OrderRepository orders) { this.orders = orders; }
    long create(CreateOrderCommand command) { return orders.save(command); }
}
System.out.println(new CreateOrderService(command -> 42L).create(new CreateOrderCommand(7)));
// Output: 42
```

## 2) Repository and Data Mapper

Repository presents collection-like domain access. Data Mapper translates between persistence rows and domain objects without making the domain depend on SQL/JPA details.

## 3) Unit of Work

A transaction tracks changes and commits them atomically. JPA's persistence context provides identity mapping and dirty checking within a unit of work.

## 4) Dependency Injection

Dependencies are supplied externally, usually through constructors. Spring's default singleton scope is container-managed Singleton, not a globally fetched Singleton.

## 5) MVC

Model holds data, View renders it, and Controller translates input into application operations. In REST APIs, JSON serialization acts as the representation layer.

## 6) Hexagonal / Ports and Adapters

Domain/application policy depends on ports; HTTP, database, and messaging implementations are adapters.

```java
interface PaymentPort { String charge(int amount); }
final class CheckoutUseCase {
    private final PaymentPort payments;
    CheckoutUseCase(PaymentPort payments) { this.payments = payments; }
    String checkout(int amount) { return payments.charge(amount); }
}
System.out.println(new CheckoutUseCase(amount -> "charged:" + amount).checkout(100));
// Output: charged:100
```

## 7) CQRS

Commands change state; queries return read models. Separate models only when different scaling, consistency, or modeling needs justify the complexity.

## 8) Event Sourcing

Persist domain events as the source of truth and rebuild state by replay. It requires event versioning, idempotency, snapshots, and operational tooling. It is not the same as publishing events from a CRUD database.

## 9) Saga

A saga coordinates a distributed business process through local transactions and compensating actions. Choreography uses events; orchestration uses a coordinator. Compensation is domain behavior, not a database rollback.

## 10) Transactional Outbox

Write business state and an outbox record in one local transaction, then publish the outbox asynchronously. Consumers must be idempotent.

## 11) Strangler Fig and Anti-Corruption Layer

Incrementally replace a legacy system behind routing boundaries. An anti-corruption layer translates legacy concepts so they do not contaminate the new domain model.
