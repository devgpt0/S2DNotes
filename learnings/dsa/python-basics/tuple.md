# Python Tuples: 60 MCQs

Questions 31-60 are based on the concepts taught in [Python Tuple Notes](../../python/notes/collection_framework/tuple.md).

## Part A: Concept MCQs (1-30)

1. Which expression creates an empty tuple?
   - A. `{}`
   - B. `[]`
   - C. `()`
   - D. `set()`

2. Which expression creates a one-item tuple containing `5`?
   - A. `(5)` 
   - B. `(5,)`
   - C. `[5]`
   - D. `{5}`

3. What is the type of `(5)`?
   - A. `tuple`
   - B. `int`
   - C. `list`
   - D. `set`

4. Which statement is true about tuples?
   - A. They are mutable and unordered.
   - B. They are immutable and preserve order.
   - C. They allow only unique items.
   - D. They can store only integers.

5. What does `values[0]` return for `values = ('a', 'b', 'c')`?
   - A. `'a'`
   - B. `'b'`
   - C. `'c'`
   - D. Error

6. What does `values[-1]` return for `values = ('a', 'b', 'c')`?
   - A. `'a'`
   - B. `'b'`
   - C. `'c'`
   - D. Error

7. What is the result of `(1, 2) + (3, 4)`?
   - A. `(1, 2, 3, 4)`
   - B. `[1, 2, 3, 4]`
   - C. `(4, 6)`
   - D. Error

8. What is the result of `(1, 2) * 2`?
   - A. `(2, 4)`
   - B. `(1, 2, 1, 2)`
   - C. `[1, 2, 1, 2]`
   - D. Error

9. What is the result of `('p', 'q', 'r', 's')[1:3]`?
   - A. `('p', 'q')`
   - B. `('q', 'r')`
   - C. `('q', 'r', 's')`
   - D. `('r', 's')`

10. What happens when `values[0] = 'x'` is attempted for a tuple?
    - A. The first item is replaced.
    - B. It raises `TypeError`.
    - C. It raises `KeyError`.
    - D. It adds a new item.

11. Which method returns the number of occurrences of a value in a tuple?
    - A. `find()`
    - B. `count()`
    - C. `index()`
    - D. `total()`

12. What does `(1, 2, 2, 3).count(2)` return?
    - A. `1`
    - B. `2`
    - C. `3`
    - D. `True`

13. What does `('a', 'b', 'c').index('b')` return?
    - A. `'b'`
    - B. `1`
    - C. `2`
    - D. `True`

14. What happens when `('a', 'b').index('z')` is evaluated?
    - A. It returns `None`.
    - B. It returns `-1`.
    - C. It raises `ValueError`.
    - D. It raises `KeyError`.

15. Which assignment correctly unpacks `point = (10, 20)`?
    - A. `x = y = point`
    - B. `x, y = point`
    - C. `x + y = point`
    - D. `x, y = (10)`

16. What is the value of `first` after `first, *middle, last = (1, 2, 3, 4)`?
    - A. `1`
    - B. `[1]`
    - C. `(1,)`
    - D. `4`

17. What is the value of `middle` after `first, *middle, last = (1, 2, 3, 4)`?
    - A. `(2, 3)`
    - B. `[2, 3]`
    - C. `2`
    - D. `[1, 4]`

18. What is the result of `tuple([1, 2, 3])`?
    - A. `[1, 2, 3]`
    - B. `(1, 2, 3)`
    - C. `{1, 2, 3}`
    - D. Error

19. Which expression checks whether `3` belongs to `values`?
    - A. `values.has(3)`
    - B. `values[3]`
    - C. `3 in values`
    - D. `values.contains(3)`

20. When can a tuple be used as a dictionary key?
    - A. Never.
    - B. Only when it contains strings.
    - C. When all of its items are hashable.
    - D. Only when it contains one item.

21. Why can `(1, [2, 3])` not be used as a dictionary key?
    - A. Tuples cannot be keys.
    - B. The contained list is unhashable.
    - C. The tuple has two items.
    - D. The tuple mixes data types.

22. What does `len((4, 5, 6))` return?
    - A. `2`
    - B. `3`
    - C. `6`
    - D. Error

23. What is the result of `min((4, 1, 7))`?
    - A. `1`
    - B. `4`
    - C. `7`
    - D. `(1, 4, 7)`

24. What is the value of `a` after `a, b = b, a` when initially `a = 1` and `b = 2`?
    - A. `1`
    - B. `2`
    - C. `(1, 2)`
    - D. Error

25. What is the result of `('a',) == ('a')`?
    - A. `True`
    - B. `False`
    - C. `None`
    - D. Error

26. What is the type of `1, 2, 3`?
    - A. `list`
    - B. `tuple`
    - C. `set`
    - D. `int`

27. What is the result of `tuple('cat')`?
    - A. `('cat',)`
    - B. `('c', 'a', 't')`
    - C. `['c', 'a', 't']`
    - D. Error

28. Which is a valid way to concatenate tuples `first` and `second`?
    - A. `first.append(second)`
    - B. `first.extend(second)`
    - C. `first + second`
    - D. `first.add(second)`

29. Can a tuple contain a mutable object such as a list?
    - A. No, tuples can contain only immutable objects.
    - B. Yes, but the tuple's item reference cannot be reassigned.
    - C. No, Python raises `TypeError` on creation.
    - D. Yes, and the tuple itself becomes mutable.

30. Which use case is most appropriate for a tuple?
    - A. A collection that must frequently gain and lose items.
    - B. A fixed record such as an `(x, y)` coordinate.
    - C. A collection requiring unique items only.
    - D. A key-value mapping.

## Part A Answers and Reasons

1. **C — `()`**. Parentheses with no items create an empty tuple.
2. **B — `(5,)`**. The trailing comma, not the parentheses, makes this a one-item tuple.
3. **B — `int`**. `(5)` is simply the integer `5` enclosed in grouping parentheses.
4. **B — They are immutable and preserve order**. Tuple positions remain ordered, but items cannot be reassigned.
5. **A — `'a'`**. Index `0` accesses the first tuple item.
6. **C — `'c'`**. Index `-1` accesses the final tuple item.
7. **A — `(1, 2, 3, 4)`**. `+` concatenates tuples into a new tuple.
8. **B — `(1, 2, 1, 2)`**. Tuple multiplication repeats the tuple's sequence.
9. **B — `('q', 'r')`**. Slicing includes index `1` and stops before index `3`.
10. **B — It raises `TypeError`**. Tuples do not permit item assignment because they are immutable.
11. **B — `count()`**. `count()` returns how many times a value appears.
12. **B — `2`**. The value `2` occurs twice in the tuple.
13. **B — `1`**. The first occurrence of `'b'` is at zero-based index `1`.
14. **C — It raises `ValueError`**. `index()` raises `ValueError` when no matching item exists.
15. **B — `x, y = point`**. The two tuple values are unpacked into the two variables.
16. **A — `1`**. The first target receives the first value from the tuple.
17. **B — `[2, 3]`**. A starred unpacking target collects the middle values in a list.
18. **B — `(1, 2, 3)`**. `tuple()` converts the list into a tuple.
19. **C — `3 in values`**. The `in` operator checks membership in a tuple.
20. **C — When all of its items are hashable**. A tuple's hashability depends on every item it contains.
21. **B — The contained list is unhashable**. A tuple containing an unhashable list is itself unhashable.
22. **B — `3`**. `len()` returns the number of tuple items.
23. **A — `1`**. `min()` returns the smallest comparable tuple item.
24. **B — `2`**. Simultaneous assignment evaluates the right side first, then swaps the values.
25. **B — `False`**. `('a',)` is a tuple, while `('a')` is the string `'a'`.
26. **B — `tuple`**. Comma-separated values form a tuple even without parentheses.
27. **B — `('c', 'a', 't')`**. `tuple()` iterates over the string's characters.
28. **C — `first + second`**. Tuples are immutable, so concatenation creates a new tuple.
29. **B — Yes, but the item reference cannot be reassigned**. The list can be mutated, but the tuple cannot replace its reference to that list.
30. **B — A fixed record such as an `(x, y)` coordinate**. Tuples suit ordered collections whose structure should not change.

## Part B: Code-Snippet MCQs (31-60)

### 31. What is printed?

```python
value = (5,)
print(type(value).__name__)
```

- A. `int`
- B. `list`
- C. `tuple`
- D. `set`

### 32. What is printed?

```python
packed = 1, 2, 3
print(packed)
```

- A. `[1, 2, 3]`
- B. `(1, 2, 3)`
- C. `{1, 2, 3}`
- D. `3`

### 33. What is printed?

```python
x, y = (10, 20)
print(x, y)
```

- A. `10 20`
- B. `(10, 20)`
- C. `20 10`
- D. `ValueError`

### 34. What happens?

```python
x, y = (1, 2, 3)
```

- A. `x` becomes `1` and `y` becomes `(2, 3)`
- B. The extra value is ignored
- C. Raises `ValueError`
- D. Raises `TypeError`

### 35. What is printed?

```python
first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)
```

- A. `1 (2, 3, 4) 5`
- B. `1 [2, 3, 4] 5`
- C. `(1,) (2, 3, 4) (5,)`
- D. `ValueError`

### 36. What is printed?

```python
def point():
    return 2, 3

result = point()
print(result)
```

- A. `[2, 3]`
- B. `(2, 3)`
- C. `2 3`
- D. `None`

### 37. What is printed?

```python
def collect(*args):
    print(type(args).__name__, args)

collect(1, 2, 3)
```

- A. `list [1, 2, 3]`
- B. `tuple (1, 2, 3)`
- C. `tuple [1, 2, 3]`
- D. `dict {1, 2, 3}`

### 38. What is printed?

```python
def add_three(a, b, c):
    return a + b + c

values = (1, 2, 3)
print(add_three(*values))
```

- A. `3`
- B. `6`
- C. `(1, 2, 3)`
- D. `TypeError`

### 39. What is printed?

```python
left = 1
right = 2
left, right = right, left
print(left, right)
```

- A. `1 2`
- B. `2 1`
- C. `(2, 1)`
- D. `ValueError`

### 40. What happens?

```python
values = (1, 2, 3)
values[0] = 9
```

- A. `values` becomes `(9, 2, 3)`
- B. Raises `TypeError`
- C. Raises `IndexError`
- D. Nothing happens

### 41. What is printed?

```python
values = ([1],)
values[0].append(2)
print(values)
```

- A. `([1],)`
- B. `([1, 2],)`
- C. `([2],)`
- D. `TypeError`

### 42. What is printed?

```python
locations = {(10, 20): 'park'}
print(locations[(10, 20)])
```

- A. `(10, 20)`
- B. `'park'`
- C. `KeyError`
- D. `TypeError`

### 43. What happens?

```python
locations = {(10, [20]): 'park'}
```

- A. A dictionary is created
- B. The list becomes a tuple
- C. Raises `TypeError`
- D. Raises `ValueError`

### 44. What is printed?

```python
values = ('a', 'b', 'c', 'd')
print(values[1:3])
```

- A. `['b', 'c']`
- B. `('b', 'c')`
- C. `('a', 'b', 'c')`
- D. `'bc'`

### 45. What is printed?

```python
first = (1, 2)
second = first + (3,)
print(first, second)
```

- A. `(1, 2, 3) (1, 2, 3)`
- B. `(1, 2) (1, 2, 3)`
- C. `(1, 2) (3,)`
- D. `TypeError`

### 46. What is printed?

```python
rows = ([],) * 2
rows[0].append(1)
print(rows)
```

- A. `([1], [])`
- B. `([1], [1])`
- C. `([], [])`
- D. `TypeError`

### 47. What is printed?

```python
values = (1, 2, 2, 3, 2)
print(values.count(2))
```

- A. `1`
- B. `2`
- C. `3`
- D. `4`

### 48. What happens?

```python
values = ('a', 'b')
print(values.index('z'))
```

- A. Prints `-1`
- B. Prints `None`
- C. Raises `ValueError`
- D. Raises `KeyError`

### 49. What is printed?

```python
pairs = [(1, 2), (3, 4)]
total = 0
for left, right in pairs:
    total += left + right
print(total)
```

- A. `4`
- B. `7`
- C. `10`
- D. `(1, 2, 3, 4)`

### 50. What is printed?

```python
values = (3, 1, 2)
print(sorted(values), values)
```

- A. `(1, 2, 3) (1, 2, 3)`
- B. `[1, 2, 3] (3, 1, 2)`
- C. `[1, 2, 3] [3, 1, 2]`
- D. `TypeError`

### 51. What is printed?

```python
point = (0, 5)
match point:
    case (0, y):
        print(y)
    case _:
        print('other')
```

- A. `0`
- B. `5`
- C. `other`
- D. `ValueError`

### 52. What is printed?

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
point = Point(2, 3)
print(point.x)
```

- A. `2`
- B. `3`
- C. `'x'`
- D. `AttributeError`

### 53. What is printed?

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

print(Point(1, 2) == (1, 2))
```

- A. `True`
- B. `False`
- C. `TypeError`
- D. `NotImplemented`

### 54. What is printed?

```python
from copy import deepcopy

first = (1, [2, 3])
second = deepcopy(first)
second[1].append(4)
print(first, second)
```

- A. `(1, [2, 3, 4]) (1, [2, 3, 4])`
- B. `(1, [2, 3]) (1, [2, 3, 4])`
- C. `(1, [2, 3]) (1, [2, 3])`
- D. `TypeError`

### 55. What is printed?

```python
values = tuple([1, 2, 3])
print(values)
```

- A. `[1, 2, 3]`
- B. `(1, 2, 3)`
- C. `{1, 2, 3}`
- D. `TypeError`

### 56. What is printed?

```python
numbers = (number * number for number in range(3))
print(tuple(numbers), tuple(numbers))
```

- A. `(0, 1, 4) (0, 1, 4)`
- B. `(0, 1, 4) ()`
- C. `() (0, 1, 4)`
- D. `TypeError`

### 57. What is printed?

```python
print((1, 9) < (2, 0))
```

- A. `True`
- B. `False`
- C. `TypeError`
- D. Comparison is random

### 58. What is printed?

```python
cache = {('user', 42): 'Asha'}
print(cache[('user', 42)])
```

- A. `('user', 42)`
- B. `'Asha'`
- C. `KeyError`
- D. `TypeError`

### 59. What is printed?

```python
first, *_, last = (1, 2, 3, 4)
print(first, last)
```

- A. `1 2`
- B. `1 4`
- C. `[1] [4]`
- D. `ValueError`

### 60. What is printed?

```python
def show(first, *args, **kwargs):
    print(first, args, kwargs['active'])

show(1, 2, 3, active=True)
```

- A. `1 [2, 3] True`
- B. `1 (2, 3) True`
- C. `(1, 2, 3) {'active': True}`
- D. `TypeError`

## Part B Answers and Reasons

31. **C - `tuple`**. The trailing comma creates a one-item tuple.
32. **B - `(1, 2, 3)`**. Commas pack the values into a tuple.
33. **A - `10 20`**. Exact unpacking assigns one value to each target.
34. **C - `ValueError`**. Two targets cannot receive three values without a starred target.
35. **B - `1 [2, 3, 4] 5`**. A starred target receives a list.
36. **B - `(2, 3)`**. Comma-separated return values form a tuple.
37. **B - `tuple (1, 2, 3)`**. Positional extras are collected in an `args` tuple.
38. **B - `6`**. `*values` unpacks the tuple into three arguments.
39. **B - `2 1`**. Multiple assignment evaluates the right side before rebinding.
40. **B - `TypeError`**. Tuple items cannot be reassigned.
41. **B - `([1, 2],)`**. The tuple is fixed, but its contained list remains mutable.
42. **B - `'park'`**. A tuple of integers is a valid dictionary key.
43. **C - `TypeError`**. The nested list makes the tuple unhashable.
44. **B - `('b', 'c')`**. Slicing a tuple returns a tuple.
45. **B - `(1, 2) (1, 2, 3)`**. Concatenation creates a new tuple.
46. **B - `([1], [1])`**. Repetition duplicates the same list reference.
47. **C - `3`**. The value `2` appears three times.
48. **C - `ValueError`**. `index()` fails when the value is absent.
49. **C - `10`**. Loop unpacking adds both values from both pairs.
50. **B - `[1, 2, 3] (3, 1, 2)`**. `sorted()` returns a list and leaves the tuple unchanged.
51. **B - `5`**. The first pattern matches and binds the second item to `y`.
52. **A - `2`**. Named tuples expose tuple positions through field names.
53. **A - `True`**. `NamedTuple` instances retain tuple equality behavior.
54. **B - `(1, [2, 3]) (1, [2, 3, 4])`**. Deep copying separates the inner list.
55. **B - `(1, 2, 3)`**. `tuple()` converts the iterable into a tuple.
56. **B - `(0, 1, 4) ()`**. A generator is exhausted after the first conversion.
57. **A - `True`**. Tuple comparison is lexicographic, so the first items decide here.
58. **B - `'Asha'`**. A hashable tuple works as a stable composite key.
59. **B - `1 4`**. The starred throwaway target collects the middle values.
60. **B - `1 (2, 3) True`**. Extra positional arguments form a tuple and keyword arguments a dictionary.
