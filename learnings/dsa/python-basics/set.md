# Python Sets: 60 MCQs

Questions 31-60 are based on the concepts taught in [Python Set Notes](../../python/notes/collection_framework/set.md).

## Part A: Concept MCQs (1-30)

1. Which expression creates an empty set?
   - A. `{}`
   - B. `[]`
   - C. `set()`
   - D. `()`

2. What is the value of `{1, 2, 2, 3}`?
   - A. `{1, 2, 2, 3}`
   - B. `{1, 2, 3}`
   - C. `[1, 2, 3]`
   - D. Error

3. Which statement is true about a standard `set`?
   - A. It preserves insertion order as part of its API contract.
   - B. It stores duplicate items.
   - C. It is an unordered collection of unique items.
   - D. Its elements can be accessed by index.

4. What does `values.add(5)` do?
   - A. Adds `5` only if it is not already present.
   - B. Adds `5` at index `0`.
   - C. Adds every item in `5`.
   - D. Returns a new set containing `5`.

5. What is the value of `values` after `values = {1, 2}; values.add(2)`?
   - A. `{1, 2, 2}`
   - B. `{1, 2}`
   - C. `{2}`
   - D. Error

6. What does `values.update([2, 3])` do for `values = {1}`?
   - A. Adds `[2, 3]` as one item.
   - B. Changes `values` to `{[2, 3]}`.
   - C. Adds each item from the iterable, resulting in `{1, 2, 3}`.
   - D. Returns `{2, 3}` without changing `values`.

7. What happens when `{1, 2}.remove(3)` is evaluated?
   - A. It returns `False`.
   - B. It does nothing.
   - C. It raises `KeyError`.
   - D. It raises `ValueError`.

8. What happens when `{1, 2}.discard(3)` is evaluated?
   - A. It raises `KeyError`.
   - B. It does nothing and does not raise an error.
   - C. It removes `2`.
   - D. It returns `False`.

9. What does `values.pop()` do for a non-empty set?
   - A. Removes and returns the smallest item.
   - B. Removes and returns an arbitrary item.
   - C. Returns an arbitrary item without removing it.
   - D. Removes every item.

10. What does `values.clear()` do?
    - A. Removes all items from the existing set.
    - B. Removes only duplicates.
    - C. Returns an empty copy.
    - D. Deletes the variable.

11. What is the result of `{1, 2} | {2, 3}`?
    - A. `{2}`
    - B. `{1, 3}`
    - C. `{1, 2, 3}`
    - D. Error

12. What is the result of `{1, 2} & {2, 3}`?
    - A. `{1, 2, 3}`
    - B. `{2}`
    - C. `{1, 3}`
    - D. `set()`

13. What is the result of `{1, 2, 3} - {2, 4}`?
    - A. `{2}`
    - B. `{1, 2, 3, 4}`
    - C. `{1, 3}`
    - D. `{4}`

14. What is the result of `{1, 2, 3} ^ {2, 3, 4}`?
    - A. `{2, 3}`
    - B. `{1, 4}`
    - C. `{1, 2, 3, 4}`
    - D. `set()`

15. Which expression checks whether `{1, 2}` is a subset of `{1, 2, 3}`?
    - A. `{1, 2}.issubset({1, 2, 3})`
    - B. `{1, 2}.contains({1, 2, 3})`
    - C. `{1, 2}.subset({1, 2, 3})`
    - D. `{1, 2} in {1, 2, 3}`

16. What does `{1, 2, 3}.isdisjoint({4, 5})` return?
    - A. `True`
    - B. `False`
    - C. `None`
    - D. Error

17. Which type can be an element of a set?
    - A. `list`
    - B. `dict`
    - C. `set`
    - D. `tuple` containing only hashable items

18. Why cannot `[1, 2]` be added to a set?
    - A. Lists are ordered.
    - B. Lists are mutable and therefore unhashable.
    - C. Lists cannot contain integers.
    - D. Sets accept only strings.

19. What does `frozenset([1, 1, 2])` create?
    - A. A mutable set `{1, 2}`
    - B. An immutable set containing `1` and `2`
    - C. A tuple `(1, 1, 2)`
    - D. Error

20. What is `len(set('hello'))`?
    - A. `3`
    - B. `4`
    - C. `5`
    - D. `6`

21. Which expression tests whether `3` belongs to a set named `values`?
    - A. `values.has(3)`
    - B. `values[3]`
    - C. `3 in values`
    - D. `values.contains(3)`

22. What is the result of `set([1, 2, 2, 3])`?
    - A. `[1, 2, 3]`
    - B. `{1, 2, 3}`
    - C. `(1, 2, 3)`
    - D. Error

23. What is the type of `{}`?
    - A. `set`
    - B. `list`
    - C. `dict`
    - D. `tuple`

24. What is the result of `{1, 2} <= {1, 2, 3}`?
    - A. `True`
    - B. `False`
    - C. `{1, 2}`
    - D. Error

25. What is the result of `{1, 2} < {1, 2}`?
    - A. `True`
    - B. `False`
    - C. `None`
    - D. Error

26. Which method returns a new set containing items common to both sets?
    - A. `difference()`
    - B. `union()`
    - C. `intersection()`
    - D. `symmetric_difference()`

27. What does `first.difference_update(second)` do?
    - A. Replaces `second` with the difference.
    - B. Removes from `first` every item also present in `second`.
    - C. Returns a new set without modifying either set.
    - D. Adds `second` to `first`.

28. Which statement safely iterates over a copy while removing matching values from `values`?
    - A. `for value in values:`
    - B. `for value in values.copy():`
    - C. `for value in set:`
    - D. `for value in values.pop():`

29. Which set operation is commonly used to remove duplicate items from a list?
    - A. `list(values)`
    - B. `set(values)`
    - C. `tuple(values)`
    - D. `dict(values)`

30. Which property is true of `frozenset`?
    - A. It supports `add()`.
    - B. It supports item assignment.
    - C. It can be used as a dictionary key when its items are hashable.
    - D. It preserves duplicate items.

## Part A Answers and Reasons

1. **C — `set()`**. `{}` creates an empty dictionary, while `set()` creates an empty set.
2. **B — `{1, 2, 3}`**. A set keeps only one instance of each equal value.
3. **C — It is an unordered collection of unique items**. Sets do not provide index-based access and remove duplicates.
4. **A — Adds `5` only if it is not already present**. Set membership is unique, so adding an existing item has no effect.
5. **B — `{1, 2}`**. Adding an existing set member does not create a duplicate.
6. **C — Adds each item, resulting in `{1, 2, 3}`**. `update()` consumes an iterable and adds its elements individually.
7. **C — It raises `KeyError`**. `remove()` requires the item to exist.
8. **B — It does nothing and does not raise an error**. `discard()` safely handles an absent item.
9. **B — Removes and returns an arbitrary item**. Sets are unordered, so no item position is guaranteed.
10. **A — Removes all items from the existing set**. `clear()` mutates the set to make it empty.
11. **C — `{1, 2, 3}`**. `|` computes the union of the two sets.
12. **B — `{2}`**. `&` computes the intersection: items appearing in both sets.
13. **C — `{1, 3}`**. Set difference keeps items in the left set that are absent from the right set.
14. **B — `{1, 4}`**. Symmetric difference keeps items that occur in exactly one set.
15. **A — `issubset()`**. This method tests whether every item of the first set occurs in the second.
16. **A — `True`**. The sets have no item in common, so they are disjoint.
17. **D — A tuple containing only hashable items**. Set members must be hashable; such tuples are hashable.
18. **B — Lists are mutable and unhashable**. Mutable lists cannot be used as set members.
19. **B — An immutable set containing `1` and `2`**. `frozenset` removes duplicates and cannot be modified.
20. **B — `4`**. The distinct characters in `hello` are `h`, `e`, `l`, and `o`.
21. **C — `3 in values`**. The `in` operator checks set membership.
22. **B — `{1, 2, 3}`**. Converting a list to a set removes duplicate values.
23. **C — `dict`**. Empty braces are the dictionary literal.
24. **A — `True`**. `<=` tests subset-or-equal for sets.
25. **B — `False`**. `<` requires a proper subset, and equal sets are not proper subsets.
26. **C — `intersection()`**. It returns values shared by both sets.
27. **B — Removes common items from `first`**. `difference_update()` changes the left-hand set in place.
28. **B — `for value in values.copy():`**. Iterating over a copy avoids changing the set being iterated.
29. **B — `set(values)`**. Constructing a set keeps unique values only.
30. **C — It can be used as a dictionary key**. An immutable, hashable `frozenset` is valid as a dictionary key.

## Part B: Code-Snippet MCQs (31-60)

### 31. What is printed?

```python
values = {1, 2, 2, 3}
print(len(values), sorted(values))
```

- A. `4 [1, 2, 2, 3]`
- B. `3 [1, 2, 3]`
- C. `4 [1, 2, 3]`
- D. `3 [3, 2, 1]`

### 32. What is printed?

```python
values = {1, 2}
values.add(2)
print(len(values))
```

- A. `1`
- B. `2`
- C. `3`
- D. `KeyError`

### 33. What is printed?

```python
values = {1}
values.update([2, 3], (3, 4))
print(sorted(values))
```

- A. `[1, 2, 3, 3, 4]`
- B. `[2, 3, 4]`
- C. `[1, 2, 3, 4]`
- D. `TypeError`

### 34. What happens?

```python
values = {1, 2}
values.remove(3)
```

- A. Nothing happens
- B. Returns `False`
- C. Raises `KeyError`
- D. Raises `ValueError`

### 35. What is printed?

```python
values = {1, 2}
values.discard(3)
print(sorted(values))
```

- A. `[1, 2]`
- B. `[1]`
- C. `[2]`
- D. `KeyError`

### 36. What is printed?

```python
values = {10, 20, 30}
values.pop()
print(len(values))
```

- A. `0`
- B. `1`
- C. `2`
- D. `3`

### 37. What is printed?

```python
left = {1, 2}
right = {2, 3}
result = left | right
print(sorted(result), sorted(left))
```

- A. `[1, 2, 3] [1, 2]`
- B. `[2] [1, 2]`
- C. `[1, 3] [1, 3]`
- D. `[1, 2, 3] [1, 2, 3]`

### 38. What is printed?

```python
left = {1, 2, 3}
right = {2, 3, 4}
print(sorted(left & right))
```

- A. `[1, 4]`
- B. `[2, 3]`
- C. `[1, 2, 3, 4]`
- D. `[]`

### 39. What is printed?

```python
left = {1, 2, 3}
right = {2, 4}
print(sorted(left - right))
```

- A. `[2]`
- B. `[1, 3]`
- C. `[1, 3, 4]`
- D. `[4]`

### 40. What is printed?

```python
left = {1, 2, 3}
right = {2, 4}
print(sorted(left ^ right))
```

- A. `[2]`
- B. `[1, 3]`
- C. `[1, 3, 4]`
- D. `[1, 2, 3, 4]`

### 41. What is printed?

```python
values = {1, 2}
values |= {2, 3}
print(sorted(values))
```

- A. `[1, 2]`
- B. `[2]`
- C. `[1, 2, 3]`
- D. `[1, 3]`

### 42. What is printed?

```python
values = {1, 2, 3}
values &= {2, 3, 4}
print(sorted(values))
```

- A. `[1, 4]`
- B. `[2, 3]`
- C. `[1, 2, 3, 4]`
- D. `[]`

### 43. What is printed?

```python
small = {1, 2}
large = {1, 2, 3}
print(small.issubset(large), large.issuperset(small))
```

- A. `True True`
- B. `True False`
- C. `False True`
- D. `False False`

### 44. What is printed?

```python
first = {1, 2}
second = {2, 1}
print(first <= second, first < second)
```

- A. `True True`
- B. `True False`
- C. `False True`
- D. `False False`

### 45. What is printed?

```python
first = {1, 2}
second = {3, 4}
print(first.isdisjoint(second))
```

- A. `True`
- B. `False`
- C. `set()`
- D. `None`

### 46. What is printed?

```python
result = {number * number for number in range(6) if number % 2 == 0}
print(sorted(result))
```

- A. `[0, 2, 4]`
- B. `[0, 4, 16]`
- C. `[1, 9, 25]`
- D. `[4, 16, 36]`

### 47. What happens?

```python
values = {[1, 2], [3, 4]}
```

- A. A two-item set is created
- B. The lists become tuples
- C. Raises `TypeError`
- D. Raises `IndexError`

### 48. What is printed?

```python
values = {(1, 2), (3, 4)}
print((1, 2) in values)
```

- A. `True`
- B. `False`
- C. `TypeError`
- D. `KeyError`

### 49. What is printed?

```python
values = frozenset([1, 2, 2])
print(len(values), 2 in values)
```

- A. `3 True`
- B. `2 True`
- C. `2 False`
- D. `TypeError`

### 50. What is printed?

```python
key = frozenset({'read', 'write'})
permissions = {key: 'editor'}
print(permissions[frozenset({'write', 'read'})])
```

- A. `'editor'`
- B. `KeyError`
- C. `TypeError`
- D. `frozenset({'read', 'write'})`

### 51. What happens?

```python
values = frozenset({1, 2})
values.add(3)
```

- A. The value is added
- B. Nothing happens
- C. Raises `AttributeError`
- D. Raises `KeyError`

### 52. What is printed?

```python
first = {1, 2}
second = first.copy()
second.add(3)
print(sorted(first), sorted(second))
```

- A. `[1, 2, 3] [1, 2, 3]`
- B. `[1, 2] [1, 2, 3]`
- C. `[1, 2] [3]`
- D. `TypeError`

### 53. What is printed?

```python
first = {1, 2}
second = first
second.add(3)
print(sorted(first))
```

- A. `[1, 2]`
- B. `[3]`
- C. `[1, 2, 3]`
- D. `None`

### 54. What is printed?

```python
values = {1, 2, 3, 4}
values.difference_update({2, 4, 6})
print(sorted(values))
```

- A. `[2, 4]`
- B. `[1, 3]`
- C. `[1, 3, 6]`
- D. `[1, 2, 3, 4, 6]`

### 55. What is printed?

```python
values = {1, 2, 3}
values.symmetric_difference_update({2, 4})
print(sorted(values))
```

- A. `[2]`
- B. `[1, 3]`
- C. `[1, 3, 4]`
- D. `[1, 2, 3, 4]`

### 56. What is printed?

```python
seen = set()
for value in [1, 2, 3, 2, 4]:
    if value in seen:
        print(value)
        break
    seen.add(value)
```

- A. `1`
- B. `2`
- C. `3`
- D. Nothing

### 57. What is printed?

```python
first = [1, 2, 2, 3]
second = [2, 3, 4]
print(sorted(set(first) & set(second)))
```

- A. `[1, 4]`
- B. `[2, 2, 3]`
- C. `[2, 3]`
- D. `[1, 2, 3, 4]`

### 58. What is printed?

```python
seen = set()
duplicates = set()
for character in 'banana':
    if character in seen:
        duplicates.add(character)
    else:
        seen.add(character)
print(sorted(duplicates))
```

- A. `['a']`
- B. `['a', 'n']`
- C. `['b', 'a', 'n']`
- D. `[]`

### 59. What is printed?

```python
edge_one = frozenset({'A', 'B'})
edge_two = frozenset({'B', 'A'})
print(edge_one == edge_two)
```

- A. `True`
- B. `False`
- C. `TypeError`
- D. Order dependent

### 60. What is printed?

```python
values = [3, 1, 3, 2, 1]
print(sorted(set(values)))
```

- A. `[3, 1, 3, 2, 1]`
- B. `[3, 2, 1]`
- C. `[1, 2, 3]`
- D. `{1, 2, 3}`

## Part B Answers and Reasons

31. **B - `3 [1, 2, 3]`**. Sets keep only unique values.
32. **B - `2`**. Adding an existing value changes nothing.
33. **C - `[1, 2, 3, 4]`**. `update()` consumes every iterable and removes duplicates.
34. **C - `KeyError`**. `remove()` requires the value to exist.
35. **A - `[1, 2]`**. `discard()` ignores an absent value.
36. **C - `2`**. `pop()` removes one arbitrary member.
37. **A - `[1, 2, 3] [1, 2]`**. Union creates a new set and leaves `left` unchanged.
38. **B - `[2, 3]`**. Intersection keeps values found in both sets.
39. **B - `[1, 3]`**. Difference keeps left-side values absent from the right.
40. **C - `[1, 3, 4]`**. Symmetric difference keeps values found in exactly one set.
41. **C - `[1, 2, 3]`**. `|=` performs an in-place union.
42. **B - `[2, 3]`**. `&=` performs an in-place intersection.
43. **A - `True True`**. Both relationship checks describe the same containment.
44. **B - `True False`**. Equal sets satisfy subset-or-equal but not proper subset.
45. **A - `True`**. The sets have no common member.
46. **B - `[0, 4, 16]`**. The comprehension squares the even inputs.
47. **C - `TypeError`**. Mutable lists are unhashable set members.
48. **A - `True`**. A tuple of integers is hashable.
49. **B - `2 True`**. `frozenset` is immutable and removes duplicates.
50. **A - `'editor'`**. Equal frozensets have equal hashes regardless of item order.
51. **C - `AttributeError`**. A frozenset has no mutating `add()` method.
52. **B - `[1, 2] [1, 2, 3]`**. `copy()` creates a separate set.
53. **C - `[1, 2, 3]`**. Assignment aliases the same set.
54. **B - `[1, 3]`**. `difference_update()` removes common values in place.
55. **C - `[1, 3, 4]`**. The in-place symmetric difference removes `2` and adds `4`.
56. **B - `2`**. The second `2` is the first repeated value encountered.
57. **C - `[2, 3]`**. Converting to sets removes duplicates before intersection.
58. **B - `['a', 'n']`**. Both characters occur more than once.
59. **A - `True`**. Frozenset equality is independent of iteration order.
60. **C - `[1, 2, 3]`**. The set removes duplicates and `sorted()` provides deterministic order.
