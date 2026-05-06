# 11 - Common Bugs and Best Practices

## 1) ConcurrentModificationException

Wrong:

```java
for (String s : list) {
    if (s.isBlank()) list.remove(s); // unsafe
}
```

Correct:

```java
list.removeIf(String::isBlank);
```

or use iterator remove.

## 2) Equals/HashCode for `contains` and `remove`

For custom objects, implement `equals` and `hashCode` properly.

## 3) Avoid Raw Types

Wrong:

```java
List list = new ArrayList();
```

Use generics:

```java
List<String> list = new ArrayList<>();
```

## 4) Do Not Overuse LinkedList

Many developers choose `LinkedList` expecting faster insert always.
In real workloads, `ArrayList` often wins due to cache locality.

## 5) Clear API Contracts

When returning list from method, decide and document:

- mutable or immutable
- live view or snapshot copy

