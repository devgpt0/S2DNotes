# Java Advanced - Complete Learning Roadmap

Begin with [Advanced Java in simple words](00a-advanced-java-in-simple-words.md). It shows how the topics connect before the detailed rules and internals.

These notes assume Java 21 or newer and a working knowledge of Java fundamentals and collections.

Do not start here on day one. First complete fundamentals, OOP, collections, and basic streams. Then study these chapters in three groups:

- Developer level: generics, exceptions, files, strings, dates, JDBC, and testing.
- Advanced level: reflection, records/sealed types, networking, and virtual threads.
- Expert level: JVM/GC, modules/class loading, security, and migration.

## Learning Order

1. [Generics and type erasure](01-generics-type-erasure-and-wildcards.md)
2. [Exceptions and resource management](02-exceptions-and-resource-management.md)
3. [Annotations and reflection](03-annotations-and-reflection.md)
4. [Files, paths, and NIO.2](04-files-paths-and-nio2.md)
5. [Serialization and safe data exchange](05-serialization-and-data-exchange.md)
6. [Regular expressions and modern strings](06-regex-and-modern-strings.md)
7. [Date and time API](07-date-time-api.md)
8. [Records, sealed types, and pattern matching](08-records-sealed-types-and-pattern-matching.md)
9. [JVM, memory, garbage collection, and JIT](09-jvm-memory-gc-and-jit.md)
10. [Modules, class loading, and JARs](10-modules-class-loading-and-jars.md)
11. [Virtual threads and asynchronous work](11-virtual-threads-and-completable-future.md)
12. [Security, interview revision, and practice](12-security-interview-and-practice.md)
13. [JDBC and transaction fundamentals](13-jdbc-and-transaction-fundamentals.md)
14. [Testing with JUnit and Mockito](14-testing-junit-and-mockito.md)
15. [HTTP client, networking, and I/O boundaries](15-http-client-and-networking.md)
16. [Reference types, GC, and memory diagnosis](16-reference-types-gc-and-memory-diagnosis.md)
17. [Java evolution and migration](17-java-evolution-and-migration.md)
18. [Common advanced Java snippets and solved questions](18-common-code-snippets-and-solved-questions.md)

## How to Study

- Run each Java example as a small `main` method.
- Predict the output before reading the expected output.
- Change one value and explain the new result.
- Prefer standard Java APIs before adding a dependency.

## Completion Goal

After this module, you should be able to explain not only how an API works, but also its contracts, failure modes, performance implications, and safe production use.
