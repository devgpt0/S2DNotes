# 08 - Immutability and Defensive Copy (Set)

## 1) Immutable Set Factories

- `Set.of(...)`
- `Set.copyOf(...)`

No structural modifications allowed.

Concept taught: Immutable set creation.

```java
Set<String> imm = Set.of("A", "B");
System.out.println(imm);
// imm.add("C"); // UnsupportedOperationException
```

Expected output:

```text
[A, B]
```

## 2) `Set.copyOf` Snapshot

Concept taught: Immutable snapshot that does not track source updates.

```java
Set<String> src = new HashSet<>(Set.of("X"));
Set<String> snap = Set.copyOf(src);
src.add("Y");
System.out.println(src);
System.out.println(snap);
```

Expected output:

```text
[X, Y]
[X]
```

## 3) Unmodifiable View vs Snapshot

Concept taught: View reflects source; snapshot does not.

```java
Set<String> src = new HashSet<>(Set.of("A"));
Set<String> view = Collections.unmodifiableSet(src);
Set<String> snap = Set.copyOf(src);
src.add("B");
System.out.println(view);
System.out.println(snap);
```

Expected output:

```text
[A, B]
[A]
```

## 4) Defensive Copy Pattern

Concept taught: Protect internal set state in APIs.

```java
class Tags {
    private final Set<String> tags;
    Tags(Set<String> tags) { this.tags = new HashSet<>(tags); }
    Set<String> getTags() { return Set.copyOf(tags); }
}

Set<String> ext = new HashSet<>(Set.of("java"));
Tags t = new Tags(ext);
ext.add("python");
System.out.println(t.getTags());
```

Expected output:

```text
[java]
```

## 5) Summary

Use immutable snapshots at boundaries to avoid accidental shared-state mutations.
