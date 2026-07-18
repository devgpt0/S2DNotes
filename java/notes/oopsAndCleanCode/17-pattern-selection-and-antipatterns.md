# 17 - Pattern Selection and Anti-Patterns

## Selection Questions

1. What concrete change or coupling problem exists today?
2. Can a constructor, method, record, enum, or lambda solve it directly?
3. Which contract must remain stable?
4. What lifecycle, concurrency, failure, and ownership rules apply?
5. Does the pattern reduce total complexity after tests and operations are included?

## Common Anti-Patterns

- God Object: one class owns unrelated responsibilities.
- Service Locator: dependencies are fetched from hidden global state.
- Anemic Domain Model: domain rules live in procedural services while objects are data bags.
- Singleton Abuse: global mutable state disguised as a pattern.
- Factory Everywhere: every constructor is wrapped without actual selection logic.
- Deep Inheritance: behavior depends on fragile base-class implementation details.
- Golden Hammer: one pattern or technology is forced onto every problem.
- Lava Flow: obsolete abstractions remain because nobody knows whether they are needed.
- Premature Abstraction: extension points exist for imagined requirements.
- Distributed Monolith: services deploy separately but require synchronous lockstep operation.

## Refactoring Singleton Abuse

```java
interface IdGenerator { long nextId(); }

final class OrderService {
    private final IdGenerator ids;
    OrderService(IdGenerator ids) { this.ids = ids; }
    long create() { return ids.nextId(); }
}

AtomicLong sequence = new AtomicLong();
System.out.println(new OrderService(sequence::incrementAndGet).create());
// Output: 1
```

The dependency is explicit and replaceable; no caller reaches into global state.

## Pattern Interview Answer Structure

For any pattern, explain:

- intent and problem
- participants and collaboration
- one production example
- benefit and tradeoff
- when not to use it
- a simpler alternative
- concurrency and testing implications

Knowing pattern names is less valuable than choosing the smallest design that preserves the required contract.
