# 27 - Spring Boot Practicals and Interview Answers

## Practical 1: Course CRUD

Build create, find, update, delete, and page endpoints using the previous project.

Success criteria:

- separate request/response DTOs
- strict validation and Problem Details
- service transaction boundaries
- optimistic locking on update
- database uniqueness/check constraints
- security authorities
- MVC/JPA/integration tests
- metrics for success/conflict without high-cardinality tags

## Practical 2: Reliable Order Event

Create an order and outbox row in one transaction. Publish pending outbox rows to Kafka, mark them published idempotently, and make the consumer deduplicate event IDs. Test broker/database failure points.

## Practical 3: External Inventory Client

Call inventory with `RestClient`, validated DTO, trusted base URL, two-second deadline, bounded concurrency, safe retry for GET, and dependency metrics. Test timeout, invalid JSON, 404, 500, and cancellation/shutdown.

## Practical 4: Spring AI RAG Assistant

Ingest versioned course documents with tenant metadata, retrieve only authorized chunks, answer with citations, expose one read-only tool, add prompt/tool limits, and evaluate normal plus prompt-injection cases.

## Interview Questions with Answers

### 1. Spring vs Spring Boot?

Spring is the application framework and container ecosystem. Boot provides opinionated auto-configuration, starters, embedded runtime, external configuration, and operations support to create production Spring applications faster.

### 2. How does dependency injection work?

Spring builds bean definitions, constructs beans, resolves constructor dependencies by type/qualifier, applies post-processors/proxies, and manages lifecycle. Constructor injection makes required dependencies explicit.

### 3. What is auto-configuration?

Conditional configuration activated by classpath, properties, application type, and existing beans. It backs off when the user supplies the relevant bean. The condition report explains decisions.

### 4. Why does `@Transactional` fail on self-invocation?

Proxy-based advice runs when a caller enters through the proxy. A method calling another method on `this` bypasses that proxy. Put the boundary on the externally called service method or redesign responsibilities.

### 5. Persistence context and dirty checking?

Within a transaction, JPA tracks managed entity identity/state. Changes are detected and translated to SQL at flush without an explicit update call. Detached entities are not tracked.

### 6. N+1 problem?

One query loads parent rows, then one additional query per parent loads related data. Fix per use case with projections, fetch joins, entity graphs, or batch fetching and verify SQL counts.

### 7. 401 vs 403?

401 means valid authentication is required or supplied credentials are invalid. 403 means the authenticated caller is known but not authorized for the action/resource.

### 8. Filter vs interceptor vs AOP?

Filter surrounds servlet requests before Spring MVC. Interceptor surrounds mapped MVC handlers. AOP surrounds matched Spring bean method calls. Choose the boundary matching the concern.

### 9. `@SpringBootTest` vs slice test?

Full test loads the application context and optionally server. A slice loads a focused layer such as MVC or JPA, making tests faster and failures more specific.

### 10. MVC vs WebFlux?

MVC is the normal blocking request model and works well with virtual threads for blocking stacks. WebFlux is Reactive Streams/non-blocking and fits end-to-end non-blocking high-concurrency I/O. Mixing blocking calls into event loops removes its benefit.

### 11. How do you make database-to-Kafka reliable?

Write business data and outbox record in one local transaction, publish outbox asynchronously, and make consumers idempotent. A normal database commit followed by send has a dual-write failure gap.

### 12. What should production readiness include?

Validated configuration, least privilege, schema migrations, resource/time limits, health/readiness, metrics/logs/traces, graceful shutdown, security/dependency scanning, backup restore, rollback, and tested failure behavior.

### 13. Spring singleton vs GoF Singleton?

Spring singleton means one bean instance per application context/bean definition and is injected by the container. GoF Singleton provides global self-access and controls construction, often hiding dependencies and harming tests.

### 14. How do you secure Spring AI tools?

Expose the smallest tool set, validate typed inputs, authenticate/authorize inside every action, constrain network/path/data access, require confirmation for high impact, cap time/output, and audit safe metadata.

### 15. How should a fresher answer a design question?

Start with requirements and one simple request flow. Explain validation, service rule, transaction/database constraint, response/error, test, security, and monitoring. Add advanced patterns only when a stated problem requires them.
