# 12 - Common Bugs and Best Practices (Set)

## 1) Bug: Missing `equals/hashCode`

Concept taught: Incorrect equality contract causes duplicate logical entries.

```java
class User {
    String id;
    User(String id) { this.id = id; }
}

Set<User> users = new HashSet<>();
users.add(new User("u1"));
users.add(new User("u1"));
System.out.println(users.size());
```

Expected output:

```text
2
```

Fix: override `equals` and `hashCode`.

## 2) Bug: Mutable Fields in HashSet Keys

Changing fields used by `equals/hashCode` after insertion can break `contains/remove`.

## 3) Bug: Assuming HashSet Order

Concept taught: If order matters, use `LinkedHashSet` or `TreeSet`.

```java
Set<Integer> s = new HashSet<>(List.of(3, 1, 2));
System.out.println(s);
```

Output order is not guaranteed.

## 4) Bug: Comparator Inconsistent with Equals in TreeSet

Concept taught: Comparator defines uniqueness in sorted sets.

```java
Set<String> s = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
s.add("a");
s.add("A");
System.out.println(s.size());
```

Expected output:

```text
1
```

## 5) Best Practices

- prefer immutable element objects for hash/sorted sets
- choose set by order + complexity needs
- use defensive copies at API boundaries
- document null behavior and comparator logic

## 6) Summary

Most set bugs are contract issues (equality, ordering, mutability), not API syntax mistakes.
