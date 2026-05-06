# 01 - List Basics

## 1) What Is List

`List` is an ordered collection:

- maintains insertion order
- allows duplicates
- supports index-based access

## 2) Core Implementations

- `ArrayList`
- `LinkedList`
- `Vector` (legacy synchronized)
- `Stack` (legacy, extends `Vector`)
- `CopyOnWriteArrayList` (concurrent read-heavy scenarios)

## 3) Declaration Best Practice

```java
List<String> names = new ArrayList<>();
```

Prefer interface type (`List`) on left side for flexibility.

## 4) Common Methods

```java
list.add("A");
list.add(1, "B");
list.get(0);
list.set(0, "X");
list.remove(0);
list.remove("X");
list.contains("A");
list.size();
list.isEmpty();
```

## 5) Duplicate + Null Behavior

Most list implementations:

- allow duplicates
- allow `null` values (except some immutable factory lists when null inserted)

