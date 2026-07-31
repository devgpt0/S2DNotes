# Python Lists: 60 MCQs

Questions 31-60 are based on the concepts taught in [Python List Notes](../../python/notes/collection_framework/list.md).

## Part A: Concept MCQs (1-30)

1. Which expression creates an empty list?
   - A. `{}`
   - B. `[]`
   - C. `()`
   - D. `set()`

2. What is the value of `len([4, 5, 6])`?
   - A. `2`
   - B. `3`
   - C. `6`
   - D. Error

3. What does `items[-1]` return for `items = ['a', 'b', 'c']`?
   - A. `'a'`
   - B. `'b'`
   - C. `'c'`
   - D. Error

4. What is the result of `[1, 2] + [3, 4]`?
   - A. `[1, 2, 3, 4]`
   - B. `[4, 6]`
   - C. `[[1, 2], [3, 4]]`
   - D. Error

5. What does `numbers.append(3)` do?
   - A. Adds `3` at the beginning.
   - B. Adds `3` at the end.
   - C. Returns a new sorted list.
   - D. Removes the first `3`.

6. What is the value of `result` after `values = [1, 2]; result = values.append(3)`?
   - A. `[1, 2, 3]`
   - B. `[3]`
   - C. `3`
   - D. `None`

7. What is `values` after `values = [1, 2]; values.extend([3, 4])`?
   - A. `[1, 2, [3, 4]]`
   - B. `[1, 2, 3, 4]`
   - C. `[3, 4, 1, 2]`
   - D. Error

8. What is `values` after `values = [1, 2]; values.insert(1, 9)`?
   - A. `[9, 1, 2]`
   - B. `[1, 2, 9]`
   - C. `[1, 9, 2]`
   - D. Error

9. What does `values.pop()` do for a non-empty list?
   - A. Removes and returns the first item.
   - B. Removes and returns the last item.
   - C. Removes all items.
   - D. Returns the last item without removing it.

10. Which method removes the first matching value from a list?
    - A. `delete()`
    - B. `discard()`
    - C. `remove()`
    - D. `clear()`

11. What happens when `[1, 2].remove(3)` is evaluated?
    - A. It returns `False`.
    - B. It does nothing.
    - C. It raises `ValueError`.
    - D. It raises `KeyError`.

12. What is the result of `['p', 'q', 'r', 's'][1:3]`?
    - A. `['p', 'q']`
    - B. `['q', 'r']`
    - C. `['q', 'r', 's']`
    - D. `['r', 's']`

13. What is the result of `[0, 1, 2, 3, 4][::2]`?
    - A. `[0, 2, 4]`
    - B. `[1, 3]`
    - C. `[0, 1, 2]`
    - D. `[4, 2, 0]`

14. What is the result of `list(reversed([1, 2, 3]))`?
    - A. `[1, 2, 3]`
    - B. `[3, 2, 1]`
    - C. `None`
    - D. Error

15. What does `values.reverse()` do?
    - A. Returns a new reversed list.
    - B. Reverses the list in place and returns `None`.
    - C. Sorts the list in descending order.
    - D. Converts the list to a tuple.

16. What is the value of `result` after `values = [3, 1, 2]; result = values.sort()`?
    - A. `[1, 2, 3]`
    - B. `[3, 1, 2]`
    - C. `None`
    - D. Error

17. Which expression returns a new sorted list without changing `values`?
    - A. `values.sort()`
    - B. `sorted(values)`
    - C. `values.reverse()`
    - D. `list.sort(values)`

18. What is the result of `[3, 1, 2].sort(reverse=True)`?
    - A. `[3, 2, 1]`
    - B. `[1, 2, 3]`
    - C. `None`
    - D. Error

19. What does `[1, 2, 2, 3].count(2)` return?
    - A. `1`
    - B. `2`
    - C. `3`
    - D. `True`

20. What does `[10, 20, 30].index(20)` return?
    - A. `1`
    - B. `20`
    - C. `2`
    - D. `True`

21. What is the value of `a` after `a = [1, 2]; b = a; b.append(3)`?
    - A. `[1, 2]`
    - B. `[1, 2, 3]`
    - C. `[3]`
    - D. Error

22. Which expression creates a shallow copy of `values`?
    - A. `copy = values`
    - B. `copy = values[:]`
    - C. `copy = values.append()`
    - D. `copy = tuple(values)`

23. What is the result of `[x * 2 for x in [1, 2, 3]]`?
    - A. `[1, 2, 3, 1, 2, 3]`
    - B. `[2, 4, 6]`
    - C. `[1, 4, 9]`
    - D. `(2, 4, 6)`

24. Which expression checks whether `4` is present in `values`?
    - A. `values.has(4)`
    - B. `values.contains(4)`
    - C. `4 in values`
    - D. `values == 4`

25. What is the result of `[[1, 2], [3, 4]][1][0]`?
    - A. `1`
    - B. `2`
    - C. `3`
    - D. `4`

26. What is the main issue with `rows = [[0] * 3] * 2` when rows will be modified independently?
    - A. It creates a tuple.
    - B. Both rows refer to the same inner list.
    - C. It cannot contain integers.
    - D. It creates three rows.

27. Which statement correctly deletes the item at index `1` from `values`?
    - A. `remove values[1]`
    - B. `del values[1]`
    - C. `values.delete(1)`
    - D. `values.remove(1)`

28. What does `values.clear()` do?
    - A. Removes duplicate values only.
    - B. Returns a new empty list.
    - C. Removes every item from the existing list.
    - D. Deletes the variable `values`.

29. What is the result of `list(range(2, 8, 2))`?
    - A. `[2, 4, 6]`
    - B. `[2, 4, 6, 8]`
    - C. `[2, 3, 4, 5, 6, 7]`
    - D. `[8, 6, 4, 2]`

30. Which property is true of Python lists?
    - A. They are immutable and unordered.
    - B. They are mutable and preserve order.
    - C. They allow only unique items.
    - D. They can store only one data type.

## Part A Answers and Reasons

1. **B — `[]`**. Square brackets create a list; `{}` creates a dictionary.
2. **B — `3`**. The list has three elements: `4`, `5`, and `6`.
3. **C — `'c'`**. Index `-1` accesses the final item in a sequence.
4. **A — `[1, 2, 3, 4]`**. The `+` operator concatenates two lists into a new list.
5. **B — Adds `3` at the end**. `append()` adds one item to the end of the existing list.
6. **D — `None`**. `append()` mutates the list in place and does not return the list.
7. **B — `[1, 2, 3, 4]`**. `extend()` adds each item from the supplied iterable.
8. **C — `[1, 9, 2]`**. `insert(1, 9)` places `9` before the item currently at index `1`.
9. **B — Removes and returns the last item**. Without an index, `pop()` operates on the last list item.
10. **C — `remove()`**. `remove(value)` deletes the first occurrence of that value.
11. **C — It raises `ValueError`**. `remove()` raises `ValueError` if the requested value is missing.
12. **B — `['q', 'r']`**. A slice includes the start index and excludes the stop index.
13. **A — `[0, 2, 4]`**. The step of `2` selects every second item starting at index `0`.
14. **B — `[3, 2, 1]`**. `reversed()` iterates in reverse order, and `list()` materializes that iterator.
15. **B — Reverses in place and returns `None`**. `reverse()` changes the original list rather than creating a new one.
16. **C — `None`**. `sort()` changes `values` in place and returns `None`.
17. **B — `sorted(values)`**. `sorted()` returns a newly sorted list and leaves the original object unchanged.
18. **C — `None`**. `sort(reverse=True)` sorts the temporary list in descending order but returns `None`.
19. **B — `2`**. The value `2` occurs twice in the list.
20. **A — `1`**. Indexing starts at zero, so `20` is the item at index `1`.
21. **B — `[1, 2, 3]`**. `a` and `b` refer to the same list, so appending through `b` changes `a`.
22. **B — `copy = values[:]`**. A full slice produces a shallow copy of the list.
23. **B — `[2, 4, 6]`**. The comprehension multiplies every source value by `2`.
24. **C — `4 in values`**. The `in` operator performs a membership test.
25. **C — `3`**. The first index selects `[3, 4]`; the next index selects its first item.
26. **B — Both rows refer to the same inner list**. List multiplication repeats references, so changing one row changes the other.
27. **B — `del values[1]`**. `del` removes the item at the specified index.
28. **C — Removes every item from the existing list**. `clear()` empties the list in place.
29. **A — `[2, 4, 6]`**. `range(2, 8, 2)` starts at `2`, increments by `2`, and stops before `8`.
30. **B — They are mutable and preserve order**. Lists can be changed after creation and keep their item order.

## Part B: Code-Snippet MCQs (31-60)

### 31. What is printed?

```python
values = [1, 2]
values.append([3, 4])
print(values)
```

- A. `[1, 2, 3, 4]`
- B. `[1, 2, [3, 4]]`
- C. `[[1, 2], [3, 4]]`
- D. `None`

### 32. What is printed?

```python
values = [1, 2]
values.extend([3, 4])
print(values)
```

- A. `[1, 2, [3, 4]]`
- B. `[3, 4, 1, 2]`
- C. `[1, 2, 3, 4]`
- D. `None`

### 33. What is printed?

```python
values = [0, 1, 2, 3]
values[1:3] = [8]
print(values)
```

- A. `[0, 8, 3]`
- B. `[0, 8, 8, 3]`
- C. `[0, [8], 3]`
- D. `ValueError`

### 34. What is printed?

```python
first = [1, 2]
second = first
second.append(3)
print(first)
```

- A. `[1, 2]`
- B. `[1, 2, 3]`
- C. `[3]`
- D. `None`

### 35. What is printed?

```python
first = [[1], [2]]
second = first.copy()
second[0].append(9)
print(first)
```

- A. `[[1], [2]]`
- B. `[[1, 9], [2]]`
- C. `[[9], [2]]`
- D. `TypeError`

### 36. What is printed?

```python
from copy import deepcopy

first = [[1], [2]]
second = deepcopy(first)
second[0].append(9)
print(first)
```

- A. `[[1], [2]]`
- B. `[[1, 9], [2]]`
- C. `[[9], [2]]`
- D. `None`

### 37. What is printed?

```python
result = [number * number for number in range(6) if number % 2 == 0]
print(result)
```

- A. `[0, 2, 4]`
- B. `[0, 4, 16]`
- C. `[4, 16, 36]`
- D. `[1, 9, 25]`

### 38. What is printed?

```python
matrix = [[1, 2], [3, 4]]
flat = [value for row in matrix for value in row]
print(flat)
```

- A. `[[1, 2], [3, 4]]`
- B. `[1, 3, 2, 4]`
- C. `[1, 2, 3, 4]`
- D. `10`

### 39. What is printed?

```python
rows = [[0] * 2 for _ in range(2)]
rows[0][0] = 9
print(rows)
```

- A. `[[9, 0], [0, 0]]`
- B. `[[9, 0], [9, 0]]`
- C. `[[0, 0], [0, 0]]`
- D. `TypeError`

### 40. What is printed?

```python
values = [3, 1, 2]
result = values.sort()
print(result, values)
```

- A. `[1, 2, 3] [1, 2, 3]`
- B. `None [1, 2, 3]`
- C. `None [3, 1, 2]`
- D. `[1, 2, 3] None`

### 41. What is printed?

```python
words = ['pear', 'fig', 'banana']
result = sorted(words, key=len)
print(result)
```

- A. `['banana', 'pear', 'fig']`
- B. `['fig', 'pear', 'banana']`
- C. `['fig', 'banana', 'pear']`
- D. `None`

### 42. What is printed?

```python
records = [('A', 2), ('B', 1), ('C', 2)]
print(sorted(records, key=lambda item: item[1]))
```

- A. `[('B', 1), ('A', 2), ('C', 2)]`
- B. `[('B', 1), ('C', 2), ('A', 2)]`
- C. `[('A', 2), ('C', 2), ('B', 1)]`
- D. `TypeError`

### 43. What is printed?

```python
letters = ['a', 'b']
print(list(enumerate(letters, start=1)))
```

- A. `[(0, 'a'), (1, 'b')]`
- B. `[(1, 'a'), (2, 'b')]`
- C. `[('a', 1), ('b', 2)]`
- D. `[1, 2]`

### 44. What is printed?

```python
numbers = [1, 2, 3]
letters = ['a', 'b']
print(list(zip(numbers, letters)))
```

- A. `[(1, 'a'), (2, 'b')]`
- B. `[(1, 'a'), (2, 'b'), (3, None)]`
- C. `[(1, 2, 3), ('a', 'b')]`
- D. `ValueError`

### 45. What is printed?

```python
values = [10, 20, 30]
removed = values.pop(1)
print(removed, values)
```

- A. `10 [20, 30]`
- B. `20 [10, 30]`
- C. `20 [10, 20, 30]`
- D. `None [10, 30]`

### 46. What is printed?

```python
values = [0, 1, 2, 3, 4]
print(values[-4:-1])
```

- A. `[0, 1, 2, 3]`
- B. `[1, 2, 3]`
- C. `[1, 2, 3, 4]`
- D. `[4, 3, 2]`

### 47. What is printed?

```python
values = [0, 1, 2, 3, 4]
print(values[::-2])
```

- A. `[0, 2, 4]`
- B. `[4, 2, 0]`
- C. `[4, 3, 2, 1, 0]`
- D. `[3, 1]`

### 48. What is printed?

```python
first, *middle, last = [1, 2, 3, 4]
print(first, middle, last)
```

- A. `1 (2, 3) 4`
- B. `1 [2, 3] 4`
- C. `[1] [2, 3] [4]`
- D. `ValueError`

### 49. What is printed?

```python
rows = [[0] * 2] * 2
rows[0][0] = 9
print(rows)
```

- A. `[[9, 0], [0, 0]]`
- B. `[[9, 0], [9, 0]]`
- C. `[[0, 0], [0, 0]]`
- D. `IndexError`

### 50. What is printed?

```python
values = [1, 2, 2, 3]
for value in values:
    if value == 2:
        values.remove(value)
print(values)
```

- A. `[1, 3]`
- B. `[1, 2, 3]`
- C. `[1, 2, 2, 3]`
- D. `RuntimeError`

### 51. What is printed?

```python
values = [0, 1, 2, 3, 4]
del values[1:4]
print(values)
```

- A. `[0, 4]`
- B. `[1, 2, 3]`
- C. `[0, 1, 4]`
- D. `None`

### 52. What is printed?

```python
print(any([0, '', 3]), all([1, 2, 3]))
```

- A. `False False`
- B. `True False`
- C. `True True`
- D. `False True`

### 53. What is printed?

```python
result = [value if value % 2 == 0 else -value for value in range(4)]
print(result)
```

- A. `[0, 1, 2, 3]`
- B. `[0, -1, 2, -3]`
- C. `[0, 2]`
- D. `[-1, -3]`

### 54. What is printed?

```python
matrix = [[1, 2], [3, 4]]
print(matrix[1][0])
```

- A. `1`
- B. `2`
- C. `3`
- D. `4`

### 55. What is printed?

```python
import bisect

values = [1, 3, 4]
bisect.insort(values, 2)
print(values)
```

- A. `[2, 1, 3, 4]`
- B. `[1, 3, 4, 2]`
- C. `[1, 2, 3, 4]`
- D. `None`

### 56. What is printed?

```python
import heapq

print(heapq.nsmallest(2, [5, 1, 4, 2]))
```

- A. `[5, 4]`
- B. `[1, 2]`
- C. `{1, 2}`
- D. `[2, 1]`

### 57. What is printed?

```python
from collections import deque

queue = deque([1, 2, 3])
queue.popleft()
print(list(queue))
```

- A. `[1, 2]`
- B. `[2, 3]`
- C. `[1, 2, 3]`
- D. `[3, 2]`

### 58. What is printed?

```python
students = [('B', 90), ('A', 90), ('C', 80)]
students.sort(key=lambda item: (-item[1], item[0]))
print(students)
```

- A. `[('B', 90), ('A', 90), ('C', 80)]`
- B. `[('C', 80), ('A', 90), ('B', 90)]`
- C. `[('A', 90), ('B', 90), ('C', 80)]`
- D. `TypeError`

### 59. What is printed?

```python
values = [1, 2, 3]
copied = values[:]
copied[0] = 9
print(values, copied)
```

- A. `[9, 2, 3] [9, 2, 3]`
- B. `[1, 2, 3] [9, 2, 3]`
- C. `[1, 2, 3] [1, 2, 3]`
- D. `TypeError`

### 60. What is printed?

```python
values = [2, -10, 5, -3]
values.sort(key=abs, reverse=True)
print(values)
```

- A. `[-10, 5, -3, 2]`
- B. `[2, -3, 5, -10]`
- C. `[-10, -3, 2, 5]`
- D. `None`

## Part B Answers and Reasons

31. **B - `[1, 2, [3, 4]]`**. `append()` adds its argument as one item.
32. **C - `[1, 2, 3, 4]`**. `extend()` adds each item from the iterable.
33. **A - `[0, 8, 3]`**. Slice assignment may change the list length.
34. **B - `[1, 2, 3]`**. Both names reference the same list.
35. **B - `[[1, 9], [2]]`**. A shallow copy still shares nested lists.
36. **A - `[[1], [2]]`**. `deepcopy()` also copies the nested lists.
37. **B - `[0, 4, 16]`**. The comprehension squares only even numbers.
38. **C - `[1, 2, 3, 4]`**. The nested comprehension visits each row, then each value.
39. **A - `[[9, 0], [0, 0]]`**. The comprehension creates separate inner lists.
40. **B - `None [1, 2, 3]`**. `sort()` mutates and returns `None`.
41. **B - `['fig', 'pear', 'banana']`**. `key=len` sorts by length.
42. **A - `[('B', 1), ('A', 2), ('C', 2)]`**. Stable sorting preserves equal-key order.
43. **B - `[(1, 'a'), (2, 'b')]`**. Counting starts at one.
44. **A - `[(1, 'a'), (2, 'b')]`**. `zip()` stops at the shortest iterable.
45. **B - `20 [10, 30]`**. `pop(1)` removes and returns index one.
46. **B - `[1, 2, 3]`**. The stop index is excluded.
47. **B - `[4, 2, 0]`**. A negative step walks backward.
48. **B - `1 [2, 3] 4`**. A starred target collects a list.
49. **B - `[[9, 0], [9, 0]]`**. Multiplication repeats the inner-list reference.
50. **B - `[1, 2, 3]`**. Mutation shifts the next `2` past the iterator.
51. **A - `[0, 4]`**. `del` removes indices one through three.
52. **C - `True True`**. One first-list item and all second-list items are truthy.
53. **B - `[0, -1, 2, -3]`**. Evens stay positive and odds are negated.
54. **C - `3`**. The indices select row one, column zero.
55. **C - `[1, 2, 3, 4]`**. `insort()` maintains sorted order.
56. **B - `[1, 2]`**. `nsmallest()` returns the two smallest values.
57. **B - `[2, 3]`**. `popleft()` removes the first queue item.
58. **C - `[('A', 90), ('B', 90), ('C', 80)]`**. The key sorts score descending, then name ascending.
59. **B - `[1, 2, 3] [9, 2, 3]`**. A full slice creates a separate outer list.
60. **A - `[-10, 5, -3, 2]`**. Absolute values are sorted largest first.
