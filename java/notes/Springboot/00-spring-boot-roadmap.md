# Spring Boot - Complete Learning Roadmap

These notes target Spring Boot 4.1.0 with Java 21. Spring Initializr reported `4.1.0.RELEASE` as the current stable version when these notes were written.

Spring Boot is not a replacement for Java fundamentals. Before starting, be comfortable with classes, interfaces, exceptions, collections, HTTP basics, SQL, and constructor injection.

Study in levels:

- Beginner: chapters 1-5 (start an app and build a validated REST API).
- Developer: chapters 6-14 (database, security, testing, operations, external services).
- Senior: chapters 15-20 and 25 (internals, transactions, reactive, messaging, distributed systems).
- AI specialization: chapters 21-24 after understanding normal Spring services and security.

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
16. [Spring internals, auto-configuration, AOP, and web pipeline](16-spring-internals-aop-and-web-pipeline.md)
17. [Advanced transactions and persistence pitfalls](17-advanced-transactions-and-persistence-pitfalls.md)
18. [WebFlux and reactive programming](18-webflux-and-reactive-programming.md)
19. [Kafka and reliable messaging](19-kafka-and-reliable-messaging.md)
20. [Microservices and distributed systems](20-microservices-and-distributed-systems.md)
21. [Spring AI fundamentals and ChatClient](21-spring-ai-fundamentals-and-chat-client.md)
22. [Spring AI structured output, tools, and memory](22-spring-ai-structured-output-tools-and-memory.md)
23. [Spring AI RAG and vector stores](23-spring-ai-rag-and-vector-stores.md)
24. [Spring AI MCP, testing, observability, and security](24-spring-ai-mcp-testing-observability-and-security.md)
25. [Spring Batch, Modulith, and advanced ecosystem](25-spring-batch-modulith-and-ecosystem.md)
26. [Complete REST application step by step](26-complete-rest-application-step-by-step.md)
27. [Spring Boot practicals and interview answers](27-spring-boot-practicals-and-interview-answers.md)
28. [Common Spring Boot code snippets and solved questions](28-common-code-snippets-and-solved-questions.md)

## Production Shape

Use thin controllers, transactional application services, repositories for persistence, DTOs at API boundaries, constructor injection, strict validation, explicit errors, and secure defaults.
