# 09 - Immutability and Defensive Copy

## 1) Immutable Factory

```java
List<String> fixed = List.of("A", "B", "C");
```

- cannot add/remove/set
- throws `UnsupportedOperationException` on modification

## 2) Defensive Copy

When receiving external list:

```java
this.items = new ArrayList<>(items); // mutable independent copy
```

When exposing internal list:

```java
return List.copyOf(items); // immutable snapshot
```

## 3) `Arrays.asList` Trap

```java
List<Integer> a = Arrays.asList(1, 2, 3);
a.set(0, 9); // allowed
// a.add(4); // not allowed
```

It is fixed-size view backed by array, not fully mutable `ArrayList`.

