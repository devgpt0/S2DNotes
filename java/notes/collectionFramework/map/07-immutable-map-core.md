# 07 - Immutable Map Core (Complete)

## 1) What Immutable Map Means

Immutable maps cannot be structurally modified after creation.

Common factories:

- `Map.of(...)`
- `Map.ofEntries(...)`
- `Map.copyOf(...)`

## 2) `Map.of` Basics

Concept taught: Build constant map with strict validation.

```java
Map<String, Integer> m = Map.of("A", 1, "B", 2);
System.out.println(m);
// m.put("C", 3); // UnsupportedOperationException
```

Expected output:

```text
{A=1, B=2}
```

## 3) `Map.copyOf` Defensive Snapshot

Concept taught: Snapshot immutable copy of source map.

```java
Map<String, Integer> src = new HashMap<>();
src.put("A", 1);
Map<String, Integer> snap = Map.copyOf(src);

src.put("B", 2);
System.out.println(src);
System.out.println(snap);
```

Expected output:

```text
{A=1, B=2}
{A=1}
```

## 4) `Map.ofEntries` for Larger Maps

Concept taught: Create immutable maps with many entries cleanly.

```java
Map<Integer, String> m = Map.ofEntries(
    Map.entry(1, "A"),
    Map.entry(2, "B"),
    Map.entry(3, "C")
);
System.out.println(m);
```

Expected output:

```text
{1=A, 2=B, 3=C}
```

## 5) Validation Rules

Immutable factory maps reject:

- null keys
- null values
- duplicate keys

Concept taught: duplicate key creation throws error.

```java
try {
    Map.of("A", 1, "A", 2);
} catch (IllegalArgumentException ex) {
    System.out.println("duplicate key rejected");
}
```

Expected output:

```text
duplicate key rejected
```

## 6) Unmodifiable View vs Immutable Snapshot

Concept taught: Wrapper view tracks source changes, copy snapshot does not.

```java
Map<String, Integer> src = new HashMap<>();
src.put("X", 1);
Map<String, Integer> view = Collections.unmodifiableMap(src);
Map<String, Integer> snap = Map.copyOf(src);

src.put("Y", 2);
System.out.println(view);
System.out.println(snap);
```

Expected output:

```text
{X=1, Y=2}
{X=1}
```

## 7) When to Use

- constant configuration maps
- safe API return values
- share-read data across threads

## 8) Summary

Use immutable factory maps for safety, predictable contracts, and fewer shared-state bugs.
