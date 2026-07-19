# 13 - Coverage Audit and Topic Map

This audit maps recurring Java interview areas to their detailed notes.

## Language and Runtime

- syntax, variables, types, operators, arrays, strings, pass-by-value, access, initialization -> [fundamentals](../javaFundamentals/00-java-fundamentals-roadmap.md)
- exceptions, generics, reflection, annotations, I/O, dates, records, modules -> [advanced Java](../javaAdvanced/00-java-advanced-roadmap.md)
- JVM memory, GC, class loading, JIT, diagnosis -> [advanced Java](../javaAdvanced/09-jvm-memory-gc-and-jit.md) and [troubleshooting](09-jvm-performance-and-troubleshooting.md)
- Java evolution and migration -> [migration](../javaAdvanced/17-java-evolution-and-migration.md)

## OOP and Patterns

- OOP, SOLID, clean code, refactoring, DI -> [OOP roadmap](../oopsAndCleanCode/00-oop-clean-code-roadmap.md)
- Singleton, Factory Method, Abstract Factory, Builder, Prototype -> [creational patterns](../oopsAndCleanCode/13-gof-creational-patterns.md)
- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy -> [structural patterns](../oopsAndCleanCode/14-gof-structural-patterns.md)
- all 11 GoF behavioral patterns -> [behavioral patterns](../oopsAndCleanCode/15-gof-behavioral-patterns.md)
- repository, hexagonal, CQRS, event sourcing, saga, outbox -> [architectural patterns](../oopsAndCleanCode/16-enterprise-and-architectural-patterns.md)

## Data Processing and Concurrency

- collections and implementations -> [Collection Framework](../collectionFramework/core/core.md)
- lambdas and functional interfaces -> [lambda notes](../collectionFramework/lamdba/lambda.md)
- complete Stream API -> [streams](../streamApi/00-stream-api-roadmap.md)
- Java Memory Model, locks, atomics, executors, futures, virtual threads -> [concurrency](../javaConcurrencyMultithreaded/00-concurrency-mastery-roadmap.md)
- concurrency design patterns -> [pattern map](../javaConcurrencyMultithreaded/19-concurrency-design-pattern-coverage-map.md)

## Persistence, Testing, and Networking

- JDBC, prepared statements, connection pooling, ACID -> [JDBC](../javaAdvanced/13-jdbc-and-transaction-fundamentals.md)
- JUnit, Mockito, Testcontainers, test types -> [testing](../javaAdvanced/14-testing-junit-and-mockito.md)
- HTTP client, DNS/TCP/TLS, boundary security -> [networking](../javaAdvanced/15-http-client-and-networking.md)
- SQL, indexes, isolation, modeling -> [database interviews](07-sql-database-and-transaction-interviews.md)

## Spring Ecosystem

- Boot setup, DI, configuration, REST, errors, JPA, security, tests, Actuator -> [Spring Boot](../Springboot/00-spring-boot-roadmap.md)
- bean lifecycle, auto-configuration, proxies, AOP, filters/interceptors -> [Spring internals](../Springboot/16-spring-internals-aop-and-web-pipeline.md)
- transactions/JPA edge cases -> [advanced persistence](../Springboot/17-advanced-transactions-and-persistence-pitfalls.md)
- reactive/WebFlux -> [WebFlux](../Springboot/18-webflux-and-reactive-programming.md)
- Kafka and messaging -> [Kafka](../Springboot/19-kafka-and-reliable-messaging.md)
- Spring Batch, Modulith, Integration, Cloud, GraphQL -> [ecosystem](../Springboot/25-spring-batch-modulith-and-ecosystem.md)

## Spring AI

- Spring AI 2.0 dependencies, configuration, ChatClient, streaming -> [fundamentals](../Springboot/21-spring-ai-fundamentals-and-chat-client.md)
- structured output, tool calling, chat memory, advisors -> [tools and memory](../Springboot/22-spring-ai-structured-output-tools-and-memory.md)
- ingestion, embeddings, vector stores, RAG, retrieval security -> [RAG](../Springboot/23-spring-ai-rag-and-vector-stores.md)
- MCP, evaluation, testing, observability, AI threat model -> [MCP and security](../Springboot/24-spring-ai-mcp-testing-observability-and-security.md)

## Senior and Architect Coverage

- microservices, consistency, resilience, messaging, system design -> [system design](08-microservices-and-system-design.md)
- performance and incident diagnosis -> [JVM troubleshooting](09-jvm-performance-and-troubleshooting.md)
- CI/CD, Kubernetes, cloud, security -> [delivery and security](10-testing-devops-cloud-and-security.md)
- staff/principal architecture and leadership -> [8-12 years](04-lead-staff-8-to-12-years.md) and [12-15 years](05-principal-architect-12-to-15-years.md)

## Audit Result

The original gaps around Singleton/full GoF coverage, Java interview traps, JDBC/testing/networking, Spring internals/reactive/messaging/microservices, Spring AI/RAG/MCP, coding algorithms, SQL, DevOps/cloud, system design, and 0-15 year seniority expectations now have dedicated chapters.
