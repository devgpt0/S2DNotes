# 02 - HashMap Core

## 1) Internal Idea

`HashMap` uses buckets (array slots).

For `put(key, value)`:

1. Compute hash.
2. Find bucket index.
3. If key already exists, replace value.
4. Else insert new entry.

For `get(key)`:

1. Compute hash.
2. Go to bucket.
3. Find matching key.
4. Return value or `null`.

## 2) Collision

Collision means different keys land in same bucket index.

Important:

- Same bucket does not mean same key.
- `equals` decides real key match.

## 3) Resize and Load Factor

Default values:

- initial capacity: `16`
- load factor: `0.75`
- resize threshold: `capacity * loadFactor` (so 12 initially)

When size crosses threshold, map resizes (usually doubles).

## 4) equals and hashCode Contract

If custom objects are keys, always override both `equals` and `hashCode`.

Rule:

- if `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` must be true.

## 5) Iteration Best Practice

Use `entrySet()` when you need both key and value.

```java
for (Map.Entry<String, Integer> e : map.entrySet()) {
    System.out.println(e.getKey() + " : " + e.getValue());
}
```
