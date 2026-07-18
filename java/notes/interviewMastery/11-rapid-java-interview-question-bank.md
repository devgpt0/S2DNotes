# 11 - Rapid Java Interview Question Bank

## Core Java

1. Why is String immutable, and what benefits follow?
2. Why must equal objects have equal hash codes?
3. Overloading vs overriding? Static binding vs dynamic dispatch?
4. Abstract class vs interface after default methods?
5. Why is Java pass-by-value even for objects?
6. Checked vs unchecked exceptions and when to create one?
7. `final`, `finally`, and deprecated finalization?
8. String pool and `intern`?
9. Shallow vs deep immutability?
10. Record limitations and appropriate use?

## Collections and Streams

11. HashMap lookup and collision behavior?
12. ConcurrentHashMap vs synchronized map?
13. ArrayList vs LinkedList in real workloads?
14. Comparable vs Comparator?
15. Fail-fast vs weakly consistent iteration?
16. `map` vs `flatMap`?
17. `reduce` vs `collect`?
18. Why can parallel streams be slower or incorrect?

## JVM and Concurrency

19. Stack, heap, metaspace, and native memory?
20. Class loading and parent delegation?
21. Happens-before and safe publication?
22. `volatile` vs synchronized vs atomic?
23. Deadlock prevention?
24. Executor sizing and bounded queues?
25. CompletableFuture composition and exception handling?
26. Virtual threads: benefit and limits?
27. How do you diagnose memory leak/high CPU/stuck requests?

## Spring and Database

28. How does Boot auto-configuration back off?
29. Bean lifecycle and proxy-based self-invocation problem?
30. Filter vs interceptor vs AOP?
31. Transaction propagation and rollback rules?
32. JPA persistence context, dirty checking, and N+1?
33. Optimistic vs pessimistic locking?
34. Authentication vs authorization and 401 vs 403?
35. Index selection and isolation anomalies?
36. MVC vs WebFlux vs MVC with virtual threads?

## Architecture

37. Modular monolith vs microservices?
38. Saga vs two-phase commit?
39. Outbox and idempotent consumer?
40. Cache consistency and stampede prevention?
41. Timeout, retry, circuit breaker, bulkhead, and rate limiter?
42. At-least-once delivery and exactly-once business effect?
43. Backward-compatible API/database/event evolution?
44. SLI, SLO, error budget, RPO, and RTO?
45. RAG security, prompt injection, and tool authorization?

For every answer, include a concrete example and tradeoff rather than a memorized definition.
