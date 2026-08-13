# Python `set`
## 1. What Is a Set?

A **set** is a built-in Python collection type that:
- Stores **unique** values only
- Is **unordered** (no fixed index position)
- Is **mutable** (you can add/remove items)
- Uses **hashing** internally for fast lookup

```python
s = {1, 2, 3}
print(sorted(s))
print(type(s))
```

Output:
```python
[1, 2, 3]
<class 'set'>
```

## 2. Duplicate Values Are Removed Automatically

```python
s = {1, 2, 2, 3, 3, 3}
print(sorted(s))
print(len(s))
```

Output:
```python
[1, 2, 3]
3
```

## 3. Empty Set vs Empty Dictionary

`{}` creates a dictionary, not a set.

```python
a = {}
b = set()

print(type(a))
print(type(b))
```

Output:
```python
<class 'dict'>
<class 'set'>
```

## 4. Sets Are Unordered

Order is not guaranteed.

```python
s = {10, 20, 30, 40}
print(sorted(s))
```

Output:

```text
[10, 20, 30, 40]
```

## 5. No Indexing in Sets

Sets are not subscriptable.

```python
s = {1, 2, 3}

try:
    print(s[0])
except TypeError as e:
    print(e)
```

Output:
```python
'set' object is not subscriptable
```

## 6. Add One Element: `add()`

```python
s = {1, 2}
s.add(3)
print(s)
```

Output:
```python
{1, 2, 3}
```

## 7. Adding Duplicate Has No Effect

```python
s = {1, 2, 3}
s.add(2)
print(s)
```

Output:
```python
{1, 2, 3}
```

## 8. Add Multiple Elements: `update()`

```python
s = {1, 2}
s.update([3, 4, 5])
print(s)
```

Output:
```python
{1, 2, 3, 4, 5}
```

`update()` can take multiple iterables:

```python
s = {1}
s.update([2, 3], (4, 5), {6})
print(s)
```

Output:
```python
{1, 2, 3, 4, 5, 6}
```

## 9. Remove Elements

### `remove(x)` (raises error if missing)

```python
s = {1, 2, 3}
s.remove(2)
print(s)
```

Output:
```python
{1, 3}
```

```python
s = {1, 2, 3}

try:
    s.remove(100)
    print(s)
except KeyError as e:
    print(e)
```

Output:
```python
100
```

### `discard(x)` (no error if missing)

```python
s = {1, 2, 3}
s.discard(100)
print(s)
```

Output:
```python
{1, 2, 3}
```

### `pop()` (removes and returns an arbitrary element)

```python
s = {10, 20, 30}
removed = s.pop()
print(removed in {10, 20, 30})
print(len(s))
```

Output:

```text
True
2
```

### `clear()` (remove all items)

```python
s = {1, 2, 3}
s.clear()
print(s)
print(len(s))
```

Output:
```python
set()
0
```

## 10. Fast Membership Check

```python
s = {1, 2, 3}
print(2 in s)
print(10 in s)
```

Output:
```python
True
False
```

## 11. Iterate Through a Set

```python
s = {10, 20, 30}
for x in sorted(s):
    print(x)
```

Output:

```text
10
20
30
```

## 12. Set Operations

```python
a = {1, 2}
b = {2, 3}

print(a | b)          # union
print(a.union(b))     # union (method)
```

Output:
```python
{1, 2, 3}
{1, 2, 3}
```

```python
a = {1, 2, 3}
b = {2, 3, 4}

print(a & b)                  # intersection
print(a.intersection(b))      # intersection (method)
```

Output:
```python
{2, 3}
{2, 3}
```

```python
a = {1, 2, 3}
b = {2, 3, 4}

print(a - b)                  # difference
print(b - a)
```

Output:
```python
{1}
{4}
```

```python
a = {1, 2, 3}
b = {2, 3, 4}

print(a ^ b)                  # symmetric difference
print(a.symmetric_difference(b))
```

Output:
```python
{1, 4}
{1, 4}
```

## 13. Relationship Checks

```python
a = {1, 2}
b = {1, 2, 3}

print(a.issubset(b))
print(b.issuperset(a))
```

Output:
```python
True
True
```

```python
a = {1, 2}
b = {3, 4}

print(a.isdisjoint(b))
```

Output:
```python
True
```

## 14. Set Comprehension

```python
s = {x * x for x in range(6)}
print(s)
```

Output:
```python
{0, 1, 4, 9, 16, 25}
```

## 15. Convert Other Collections to Set

```python
nums = [1, 2, 2, 3, 3]
s = set(nums)

print(s)
print(type(s))
```

Output:
```python
{1, 2, 3}
<class 'set'>
```

## 16. Remove Duplicates from List

Basic way:

```python
nums = [1, 2, 2, 3, 3]
unique = list(set(nums))

print(unique)
```

Output:

```text
[1, 2, 3]
```

If you want to keep original order:

```python
nums = [3, 1, 2, 1, 3, 4]
unique_ordered = list(dict.fromkeys(nums))

print(unique_ordered)
```

Output:
```python
[3, 1, 2, 4]
```

## 17. Valid and Invalid Set Elements

Set elements must be **hashable**.

Valid:

```python
s = {1, 2.5, "hello", (1, 2), True}
print(len(s), 1 in s, "hello" in s, (1, 2) in s)
```

Output:

```text
4 True True True
```

Note: `True` and `1` are considered equal in Python, so only one may appear.

Invalid (list is mutable, so unhashable):

```python
try:
    s = {[1, 2], [3, 4]}
    print(s)
except TypeError as e:
    print(e)
```

Output:
```python
unhashable type: 'list'
```

## 18. `frozenset` (Immutable Set)

```python
fs = frozenset([1, 2, 3, 3])
print(fs)
print(type(fs))
```

Output:
```python
frozenset({1, 2, 3})
<class 'frozenset'>
```

Cannot modify:

```python
fs = frozenset([1, 2, 3])

try:
    fs.add(4)
    print(fs)
except AttributeError as e:
    print(e)
```

Output:
```python
'frozenset' object has no attribute 'add'
```

## 19. Copy and In-Place Updates

```python
s1 = {1, 2, 3}
s2 = s1.copy()

print(s1)
print(s2)
print(s1 is s2)
```

Output:
```python
{1, 2, 3}
{1, 2, 3}
False
```

In-place operators:

```python
a = {1, 2}
b = {2, 3}

a |= b      # update with union
print(a)

a &= {2, 3, 4}
print(a)

a -= {3}
print(a)

a ^= {2, 5}
print(a)
```

Output:
```python
{1, 2, 3}
{2, 3}
{2}
{5}
```

## 20. Practical Coding Patterns

### A) Find common elements of two lists

```python
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
common = set(a) & set(b)

print(common)
```

Output:
```python
{3, 4}
```

### B) Detect duplicate in O(n)

```python
nums = [1, 2, 3, 4, 2]
seen = set()
duplicate_found = False

for x in nums:
    if x in seen:
        duplicate_found = True
        print("Duplicate found:", x)
        break
    seen.add(x)

print(duplicate_found)
```

Output:
```python
Duplicate found: 2
True
```

### C) Duplicate characters in string

```python
word = "banana"
seen = set()
duplicates = set()

for ch in word:
    if ch in seen:
        duplicates.add(ch)
    else:
        seen.add(ch)

print(duplicates)
```

Output:
```python
{'a', 'n'}
```

## 21. Time Complexity (Average Case)

| Operation | Complexity |
|---|---|
| `x in s` | `O(1)` |
| `add` | `O(1)` |
| `remove` / `discard` | `O(1)` |
| `union` | `O(len(a) + len(b))` |
| `intersection` | `O(min(len(a), len(b)))` |

Worst-case can be worse, but average is fast due to hashing.

## 22. Interview-Level Mental Model

Think of a set as:

> A hash table that stores only unique, hashable keys.

This explains:
- Why duplicates disappear
- Why membership test is fast
- Why order is not guaranteed
- Why mutable objects (like lists) are not allowed as elements

## 23. Quick Revision Checklist

- Use `set()` for empty set, not `{}`.
- Sets are unordered and unindexed.
- Elements must be hashable.
- `remove` raises error if missing, `discard` does not.
- `pop` removes an arbitrary element.
- Use set operations (`|`, `&`, `-`, `^`) for clean logic.
- Use sets for fast lookups and duplicate handling.

## 24. Advanced Set Algebra for Real Problems

Use set operations to model domain rules:

```python
all_users = {"u1", "u2", "u3", "u4"}
active_users = {"u1", "u3"}
banned_users = {"u4"}

eligible = (all_users & active_users) - banned_users
print(sorted(eligible))
```

Output:

```text
['u1', 'u3']
```

This pattern appears in access control, feature flags, and reconciliation jobs.

## 25. `frozenset` as Dictionary Key (Often Missed)

`frozenset` is immutable and hashable, so it can be a key.

```python
pricing = {
    frozenset({"coffee", "sandwich"}): 199,
    frozenset({"tea", "cookie"}): 99,
}

print(pricing[frozenset({"sandwich", "coffee"})])
```

Output:

```text
199
```

Great when combination order should not matter.

## 26. Set Comprehension with Conditions

```python
values = [-4, -1, 0, 3, 3, 5]
positive_squares = {x * x for x in values if x > 0}
print(positive_squares)  # {9, 25}
```

Output:

```text
{9, 25}
```

## 27. Missing Reliability and Performance Notes

- set order is not a stable contract for business logic.
- avoid repeatedly converting same list to set in tight loops; precompute once.
- for ordered de-duplication, use `list(dict.fromkeys(seq))`.
- worst-case hash collisions exist; design with defensive timeouts for untrusted input.

## 28. Set vs List vs Dict Membership Decision

- many membership checks + unique items -> `set`
- membership + associated values -> `dict`
- order-sensitive sequence operations -> `list`

## 29. Set Operation Complexity Nuances

Average-case complexity depends on operand sizes and operation type.

Guideline:
- `a & b` is usually optimized by iterating smaller set.
- `a | b` touches both sets.
- `a - b` iterates `a`, checks membership in `b`.

For large data pipelines, choosing operand order can reduce runtime.

## 30. In-Place Set Updates vs New Set Creation

```python
a = {1, 2, 3}
b = {3, 4, 5}

c = a & b       # new set
a &= b          # mutate a
print(a, c)
```

Output:

```text
{3} {3}
```

When to use:
- immutable flow/readability: prefer new set.
- memory-sensitive in-place transform: use update operators.

## 31. Deterministic Output and Testing

Set order is intentionally non-indexed and not for deterministic output.
For logs/tests/UI output, sort explicitly:

```python
ids = {"u3", "u1", "u2"}
print(sorted(ids))  # ['u1', 'u2', 'u3']
```

Output:

```text
['u1', 'u2', 'u3']
```

## 32. `frozenset` for Undirected Graph Edges

Use `frozenset({u, v})` for order-independent pair keys.

```python
edges = {
    frozenset({"A", "B"}),
    frozenset({"B", "C"}),
}
print(frozenset({"B", "A"}) in edges)  # True
```

Output:

```text
True
```

## 33. Missing Pitfalls in Real Projects

- mutating source data while deriving sets can create stale logic.
- repeatedly converting same list to set inside loop is costly.
- confusing `{}` as empty set (it is dict).
- relying on set ordering in business logic causes flaky behavior.

## 34. Advanced Set Patterns for Interviews

1. Distinct window checks in O(n).
2. Longest consecutive sequence using set membership.
3. Efficient dedupe and intersection across multiple feeds.
4. Set-based permission models (allow/deny precedence).

## 35. Production Readiness Checklist for Sets

1. Validate elements are hashable.
2. Use `discard` when missing keys are acceptable.
3. Use explicit sorted order at boundaries (API/reporting).
4. Choose in-place vs new-set operations intentionally.
5. Treat set as fast membership tool, not ordered container.
