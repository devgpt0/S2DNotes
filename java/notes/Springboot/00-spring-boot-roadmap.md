# Spring Boot - Complete Learning Roadmap

These notes target Spring Boot 4.1.0 with Java 21. Spring Initializr reported `4.1.0.RELEASE` as the current stable version when these notes were written.

## Learning Order

1. [Getting started and project structure](01-getting-started-and-project-structure.md)
2. [Dependency injection, beans, and lifecycle](02-dependency-injection-beans-and-lifecycle.md)
3. [Configuration, profiles, and validation](03-configuration-profiles-and-validation.md)
4. [REST APIs and strict request validation](04-rest-api-and-request-validation.md)
5. [Errors and Problem Details](05-errors-and-problem-details.md)
6. [JPA entities, repositories, and transactions](06-jpa-repositories-and-transactions.md)
7. [Queries, pagination, locking, and performance](07-queries-pagination-locking-and-performance.md)
8. [Spring Security](08-spring-security.md)
9. [Testing](09-testing.md)
10. [Actuator, metrics, and observability](10-actuator-metrics-and-observability.md)
11. [Caching, scheduling, and async work](11-caching-scheduling-and-async-work.md)
12. [Calling external HTTP services](12-external-http-services.md)
13. [Events, messaging, and consistency](13-events-messaging-and-consistency.md)
14. [Production deployment and operations](14-production-deployment-and-operations.md)
15. [Architecture, interview revision, and practice](15-architecture-interview-and-practice.md)

## Production Shape

Use thin controllers, transactional application services, repositories for persistence, DTOs at API boundaries, constructor injection, strict validation, explicit errors, and secure defaults.
