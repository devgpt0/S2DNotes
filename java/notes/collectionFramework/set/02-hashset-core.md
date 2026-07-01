# 02 - HashSet Core (Complete)

## 1) Internal Idea

`HashSet` is backed by `HashMap` internally (elements stored as map keys).

- uniqueness by `equals` + `hashCode`
- no iteration order guarantee

## 2) Complexity

Average:

- `add/remove/contains`: `O(1)`

Worst case can degrade with high collisions.

## 3) Basic Behavior

Concept taught: Uniqueness + unordered iteration.

```java
Set<Integer> set = new HashSet<>();
set.add(3);
set.add(1);
set.add(2);
set.add(2);
System.out.println(set);
System.out.println(set.contains(2));
```

Possible output:

```text
[1, 2, 3]
true
```

Order may vary.

## 4) `equals/hashCode` Contract

Concept taught: Proper equality contract enables logical deduplication.

```java
record User(String id, String name) {}
Set<User> users = new HashSet<>();
users.add(new User("u1", "Ram"));
users.add(new User("u1", "Ram"));
System.out.println(users.size());
```

Expected output:

```text
1
```

## 5) Pre-sizing for Large Loads

Concept taught: Capacity hint to reduce resize cost.

```java
int expected = 50_000;
Set<Integer> set = new HashSet<>((int) (expected / 0.75f) + 1);
System.out.println("ready");
```

Expected output:

```text
ready
```

## 6) Null Behavior

`HashSet` allows one `null` element.

Concept taught: Null support in `HashSet`.

```java
Set<String> s = new HashSet<>();
s.add(null);
s.add(null);
System.out.println(s.size());
```

Expected output:

```text
1
```

## 7) Summary

`HashSet` is the default set for fast membership and dedup when ordering is not required.
