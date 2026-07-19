# Complete Java Developer Notes Roadmap

If you are completely new to programming, begin with [How to use these notes](01-how-to-use-these-notes.md) and keep the [simple Java glossary](02-java-words-in-simple-language.md) open beside you.

Do not try to learn every interview term on the first reading. The notes are designed in three passes:

1. **Beginner pass:** understand the idea and run the first example.
2. **Developer pass:** learn rules, errors, testing, and production use.
3. **Expert pass:** study internals, tradeoffs, performance, and interview scenarios.

## Learning Modules

1. [Java fundamentals](javaFundamentals/00-java-fundamentals-roadmap.md)
2. [OOP, clean code, and all GoF patterns](oopsAndCleanCode/00-oop-clean-code-roadmap.md)
3. [Collection Framework](collectionFramework/core/core.md)
4. [Stream API](streamApi/00-stream-api-roadmap.md)
5. [Advanced Java](javaAdvanced/00-java-advanced-roadmap.md)
6. [Concurrency and multithreading](javaConcurrencyMultithreaded/00-concurrency-mastery-roadmap.md)
7. [Spring Boot, Spring ecosystem, and Spring AI](Springboot/00-spring-boot-roadmap.md)
8. [Interview preparation from 0 to 15 years](interviewMastery/00-java-developer-interview-roadmap-0-to-15-years.md)
9. [Master index of common coding and interview questions](03-common-interview-code-index.md)

Each technical module now begins with an **in simple words** chapter. Read that chapter first. It gives you the mental model and runnable output before formal terminology and expert details.

## Coverage

The combined notes cover language fundamentals, OOP, all 23 GoF patterns, collections, generics, lambdas, streams, JVM internals, memory/GC, I/O, JDBC, testing, concurrency patterns, virtual threads, Spring MVC/WebFlux/Data/Security/Batch/Modulith, Kafka, microservices, system design, DevOps/cloud, Spring AI, RAG, tools, MCP, security, and senior engineering leadership.

## Recommended Study Order

- Beginner: modules 1-4
- Working Java developer: modules 5-7
- Interview revision: module 8 in parallel with the relevant technical module
- Senior/lead/architect: distributed systems, troubleshooting, security, system design, and leadership sections in module 8

Every new practical snippet contains printed output or an explicit result explanation.

## Prerequisite Gates

Move forward when you can complete the gate without looking at the answer:

| After module | You should be able to build or explain |
|---|---|
| Fundamentals | a console program with input, decisions, loops, methods, arrays, and clear printed output |
| OOP | a small domain model with protected invariants, composition, and focused tests |
| Collections | why a `List`, `Set`, `Map`, or `Queue` fits a concrete requirement |
| Streams | a side-effect-free transformation and the equivalent loop |
| Advanced Java | safe file/resource handling, generics, time, testing, and JVM basics |
| Concurrency | ownership of mutable state, cancellation, timeouts, and bounded work |
| Spring Boot | a validated, secured, tested REST use case with observable failures |

## One Concept, Three Passes

Suppose a chapter teaches a `Map`:

1. **Beginner:** insert a key/value, print it, and predict the result.
2. **Developer:** handle a missing key, choose mutability, and test the behavior.
3. **Expert:** discuss key contracts, concurrency, memory, and operational tradeoffs.

Do not begin with internals. First make the behavior visible, then understand its guarantees, then study its implementation and tradeoffs.

## Evidence of Learning

A completed module produces something observable: console output, a passing assertion, an HTTP response, a database state change, or a measured profile. `System.out` is ideal for small language demonstrations; production Spring applications should use structured logging and tests rather than ad hoc prints.
