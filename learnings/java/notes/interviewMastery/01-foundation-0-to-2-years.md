# 01 - Foundation Interview Coverage: 0 to 2 Years

## Java Language

- JDK vs JRE vs JVM; source, bytecode, class loading, JIT
- primitives, wrappers, widening/narrowing, overflow, autoboxing
- variables, scope, lifetime, fields, local defaults
- operators, short-circuiting, loops, switch expressions
- methods, overloading, varargs, recursion, pass-by-value
- arrays, strings, string pool, builders, enums
- packages, imports, access modifiers, static, final, initialization order
- checked vs unchecked exceptions and try-with-resources

## OOP

- class vs object; state, behavior, identity
- encapsulation and invariants
- abstraction, interfaces, abstract classes
- inheritance vs composition
- compile-time vs runtime polymorphism
- overriding rules and covariant returns
- `Object` contract: equals, hashCode, toString
- immutable classes and defensive copies

## Collections and Generics

- List, Set, Queue, Map selection
- ArrayList vs LinkedList
- HashMap internals and equals/hashCode contract
- HashSet vs TreeSet
- Comparable vs Comparator
- Iterator and fail-fast behavior
- generic invariance, bounds, PECS, raw types

## Coding Standard

```java
static OptionalInt secondLargest(int[] values) {
    int[] sortedDistinct = Arrays.stream(values).distinct().sorted().toArray();
    if (sortedDistinct.length < 2) {
        return OptionalInt.empty();
    }
    return OptionalInt.of(sortedDistinct[sortedDistinct.length - 2]);
}
System.out.println(secondLargest(new int[] {3, 1, 3, 2}).orElseThrow());
// Output: 2
```

In an interview, first clarify empty/duplicate behavior and then prefer a one-pass solution when complexity matters.

## Expected Practical Skills

- write compilable code without IDE dependence
- use Git branch/commit/pull-request basics
- write focused unit tests
- read a stack trace
- explain time and space complexity
- build and run with Maven/Gradle wrapper
- implement a small REST CRUD API with validation
