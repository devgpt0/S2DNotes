# 06 - equals, hashCode, and Ordering Contracts

## 1) Why Contracts Matter

Collection behavior depends heavily on object equality and ordering contracts.

- hash-based collections rely on `equals` + `hashCode`
- sorted collections rely on comparator/natural ordering

## 2) `equals/hashCode` Contract

If `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` must be true.

Concept taught: Correct key equality enables expected hash map lookup.

```java
record UserKey(String country, int id) {}
Map<UserKey, String> map = new HashMap<>();
map.put(new UserKey("IN", 1), "Ram");
System.out.println(map.get(new UserKey("IN", 1)));
```

Expected output:

```text
Ram
```

## 3) Comparator Contract

Comparators should be:

- anti-symmetric
- transitive
- consistent on repeated calls

Concept taught: Comparator defines sorted order in `TreeSet`/`TreeMap`.

```java
Set<String> s = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
s.add("a");
s.add("A");
s.add("b");
System.out.println(s);
```

Expected output:

```text
[a, b]
```

Explanation:

- comparator treats `a` and `A` as equal for ordering, so only one remains

## 4) Common Mistake

Using mutable fields inside `equals/hashCode` for map/set keys can break lookup consistency after mutation.

## 5) Summary

Correct equality and ordering contracts are non-negotiable for collection correctness.
