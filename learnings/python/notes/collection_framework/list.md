# Python `list`
## 1) What Is a List
A list is an ordered, mutable sequence type.

Key properties:

- Ordered: index-based access is available
- Mutable: can add, remove, update elements
- Heterogeneous: can store mixed data types
- Iterable: can loop with `for`, comprehensions, and functional tools

Examples:

```python
my_list = [1, 2, 3, 4, 5]
mixed = [1, "hi", 3.14, True]
nested = [[1, 2], [3, 4]]
empty = []
```

## 2) Creating Lists

```python
a = [1, 2, 3]
b = list()                    # []
c = list("Ada")              # ['A', 'd', 'a']
d = list(range(5))            # [0, 1, 2, 3, 4]
e = list({10, 20, 30})        # order not guaranteed for set input
```

Important:

- `list(iterable)` requires an iterable
- `list(123)` raises `TypeError` because `int` is not iterable

## 3) Indexing and Slicing

```python
fruits = ["apple", "orange", "mango"]
fruits[0]      # apple
fruits[-1]     # mango
```

Slicing form:

```python
seq[start:end:step]
```

Rules:

- end index is excluded
- negative indices allowed
- out-of-range slicing does not raise error
- direct bad index access raises `IndexError`

```python
nums = [10, 20, 30, 40, 50]
nums[:3]       # [10, 20, 30]
nums[1:]       # [20, 30, 40, 50]
nums[1::2]     # [20, 40]
nums[::-1]     # [50, 40, 30, 20, 10]
```

## 4) Updating Lists

```python
fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"
fruits[1:3] = ["pear", "kiwi"]
```

Slice assignment can grow/shrink list depending on RHS length.

## 5) Add Operations

```python
fruits = ["apple", "banana"]
fruits.append("mango")            # add one element at end
fruits.insert(1, "grapes")        # insert at index
fruits.extend(["kiwi", "plum"])  # add multiple elements
```

Difference:

- `append([1,2])` adds one nested element
- `extend([1,2])` adds two separate elements

## 6) Remove Operations

```python
fruits = ["apple", "banana", "banana", "mango"]
fruits.remove("banana")   # removes first matching value
x = fruits.pop()           # remove and return last
y = fruits.pop(0)          # remove and return by index
del fruits[1]              # delete by index
del fruits[1:3]            # delete slice
fruits.clear()             # remove all
```

Notes:

- `remove` returns `None`
- `remove` raises `ValueError` if value absent
- `pop` raises `IndexError` on empty list or bad index

## 7) Copying: Alias, Shallow, Deep

Alias:

```python
a = [1, 2, 3]
b = a
b.append(4)
# both changed
```

Shallow copy:

```python
a = [1, 2, 3]
b = a[:]              # or list(a) or a.copy()
b[0] = 99
# a unchanged for flat list
```

Nested list caveat (shallow copy shares inner lists):

```python
c = [[1, 2], [3, 4]]
d = c[:]
d[0][0] = 99
# c also changes
```

Deep copy:

```python
import copy
c = [[1, 2], [3, 4]]
e = copy.deepcopy(c)
e[0][0] = 100
# c unchanged
```

## 8) Operators and Membership

```python
a = [1, 2, 3]
b = [4, 5]
a + b          # [1, 2, 3, 4, 5]
a * 2          # [1, 2, 3, 1, 2, 3]
```

Important:

```python
a + b + [6]    # valid
a + b + 6      # TypeError
```

Membership:

```python
fruits = ["apple", "mango", "banana"]
"apple" in fruits
"grape" not in fruits
```

Membership in list is linear search: O(n).

## 9) Built-ins with Lists

```python
nums = [1, 2, 3, 8, 9]
len(nums)
min(nums)
max(nums)
sum(nums)
```

Strings in `min/max` are lexicographic.

```python
names = ["Alice", "Bob", "Charlie"]
max(names)
ord('A')
```

## 10) Sorting and Reversing

In-place reverse:

```python
nums = [1, 2, 3]
nums.reverse()          # modifies nums
```

Iterator reverse:

```python
list(reversed(nums))    # new list
```

Sorted copy:

```python
words = ["banana", "an", "cherry"]
out = sorted(words, key=len, reverse=True)
```

In-place sort:

```python
nums = [-10, 5, -3, 2, -1]
nums.sort(key=abs, reverse=True)
```

Case-insensitive sorting:

```python
names = ["Alice", "alice", "Charlie"]
names.sort(key=str.lower)
```

## 11) Common Utility Methods

```python
fruits = ['apple', 'banana', 'apple', 'orange']
fruits.count('apple')
fruits.index('apple')
fruits.index('apple', 1)    # search from start index
```

`index` raises `ValueError` if not found.

## 12) Iteration Patterns

Element iteration:

```python
for fruit in fruits:
    print(fruit)
```

Index-based:

```python
for i in range(len(fruits)):
    print(i, fruits[i])
```
Preferred indexed loop:

```python
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

Reverse iteration:

```python
for x in reversed(fruits):
    print(x)
```

## 13) List Comprehension (In Depth)

Basic map:

```python
nums = [1, 2, 3, 4]
sq = [x * x for x in nums]
```

Filter:

```python
even = [x for x in nums if x % 2 == 0]
```

Map + filter:

```python
out = [x * 2 for x in nums if x > 2]
```

Conditional expression:

```python
labels = ["even" if x % 2 == 0 else "odd" for x in nums]
```

Nested comprehension:

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [item for row in matrix for item in row]
```

2D creation safely:

```python
grid = [[0 for _ in range(3)] for _ in range(3)]
```

Avoid this for nested mutable rows:

```python
bad = [[0] * 3] * 3   # rows reference same inner list
```

## 14) Lambda + List Workflows

Lambda with `sorted`:

```python
students = [("A", 8.5), ("B", 7.2), ("C", 9.1)]
out = sorted(students, key=lambda x: x[1], reverse=True)
```

Lambda with `map`/`filter`:

```python
nums = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, nums))
odd = list(filter(lambda x: x % 2 == 1, nums))
```

Practical note:

- For readability, list comprehensions are often preferred over simple `map/filter`

## 15) Nested Lists (In Depth)

Access:

```python
matrix = [[1, 2], [3, 4], [5, 6]]
matrix[0][1]   # 2
```

Update:

```python
matrix[1][0] = 99
```

Row/column patterns:

```python
row_sums = [sum(row) for row in matrix]
first_col = [row[0] for row in matrix]
```

## 16) Time Complexity Quick View

- `append`: amortized O(1)
- `pop()` from end: O(1)
- `pop(i)`: O(n)
- `insert(i, x)`: O(n)
- `remove(x)`: O(n)
- `x in list`: O(n)
- index access `lst[i]`: O(1)
- slicing `lst[a:b]`: O(k)
- sort: O(n log n)

## 17) Interview Pitfalls Checklist

- Confusing `append` vs `extend`
- Using `remove` when index-based deletion is needed
- Forgetting `remove/index` raise `ValueError`
- Shallow-copy surprises with nested lists
- Using `[[0]*m]*n` for matrix creation
- Expecting `sorted()` to modify original list
- Using `list.sort()` and assigning its return (it returns `None`)
- Off-by-one slicing mistakes (`end` exclusive)

## 19) Missing but Important: `deque` vs `list` for Queue Use-Cases

`list` is great for stack-style operations (`append`, `pop()` from end).
For queue front-removal (`pop(0)`), use `collections.deque`.

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)      # right side
q.appendleft(0)  # left side
first = q.popleft()
print(first, q)
```

Output:

```text
0 deque([1, 2, 3, 4])
```

Interview takeaway:
- frequent front operations -> `deque`
- random index access -> `list`

## 20) `bisect` for Maintaining Sorted Lists

`bisect` helps keep sorted order without sorting each time.

```python
from bisect import insort

arr = [10, 20, 40]
insort(arr, 30)
print(arr)  # [10, 20, 30, 40]
```

Output:

```text
[10, 20, 30, 40]
```

Use when:
- data is mostly sorted
- incremental inserts happen over time

## 21) Heap-Based Patterns (`heapq`) for Top-K

```python
import heapq

scores = [40, 10, 70, 20, 90, 60]
top3 = heapq.nlargest(3, scores)
print(top3)  # [90, 70, 60]
```

Output:

```text
[90, 70, 60]
```

Why this belongs in list notes:
- heap operations are list-backed and common in interview problems.

## 22) Slice Assignment and In-Place Bulk Update

```python
nums = [1, 2, 3, 4, 5]
nums[1:4] = [20, 30]
print(nums)  # [1, 20, 30, 5]
```

Output:

```text
[1, 20, 30, 5]
```

Useful for:
- controlled replacement
- in-place transformation without creating new variable names

## 23) List Performance Pitfalls in Real Systems

- repeated `pop(0)` in large lists
- repeated `in` checks in loops where set would be better
- repeated sorting inside loops
- building huge temporary lists when generator pipeline is enough

## 24) Sorting Deep Dive: Stability, Multi-Key, and DSU Pattern

Python uses Timsort (stable sort). Stability means if two elements compare equal,
their relative order is preserved.

```python
records = [
    {"name": "Ana", "dept": "ENG", "score": 92},
    {"name": "Raj", "dept": "ENG", "score": 92},
    {"name": "Mia", "dept": "HR", "score": 88},
]

# sort by score desc, then name asc
out = sorted(records, key=lambda r: (-r["score"], r["name"]))
```

Interview points:
- stable sort helps in chained sorts.
- `list.sort()` is in-place and memory-efficient.
- `sorted()` returns new list and works on any iterable.

## 25) Extended Slicing and Slice Assignment

```python
nums = [0, 1, 2, 3, 4, 5, 6]
print(nums[::2])      # [0, 2, 4, 6]
print(nums[::-1])     # reversed copy

nums[1:6:2] = [10, 30, 50]   # lengths must match when step != 1
print(nums)
```

Output:

```text
[0, 2, 4, 6]
[6, 5, 4, 3, 2, 1, 0]
[0, 10, 2, 30, 4, 50, 6]
```

Common trap:
- For stepped slice assignment, replacement length mismatch raises `ValueError`.

## 26) List Internals: Dynamic Array Growth (Conceptual)

`list` is a dynamic array:
- O(1) index access.
- append is amortized O(1) due to overallocation strategy.
- middle insert/delete is O(n) because elements shift.

This explains why:
- list is excellent for random access and append-heavy workloads.
- list is poor for queue front operations.

## 27) In-Place Methods Return `None` (High-Value Pitfall)

Methods like `sort`, `reverse`, `append`, `extend`, `insert`, `remove`, `clear`
mutate list and return `None`.

```python
nums = [3, 1, 2]
nums.sort()
print(nums)  # [1, 2, 3]
```

Output:

```text
[1, 2, 3]
```

Wrong pattern:
```python
# nums = nums.sort()   # nums becomes None
```

## 28) Advanced Interview Patterns with Lists

1. Two pointers:
   Sorted pair-sum, remove duplicates, partition logic.
2. Sliding window:
   Subarray/substring constraints.
3. Prefix sums:
   Range-sum and balance problems.
4. Monotonic stack/list:
   Next greater element style problems.
5. Merge intervals:
   Sort + linear scan.

## 29) List vs Tuple vs Array vs Deque (Decision Grid)

- list: general-purpose mutable sequence.
- tuple: fixed-size record, hashable if contents hashable.
- `array.array`: numeric typed compact storage.
- `collections.deque`: fast append/pop both ends.

Rule:
- pick by access pattern, mutation pattern, and memory profile.

## 30) Production Checklist for List Usage

1. Avoid `pop(0)` in hot paths.
2. Avoid needless full copies for large lists.
3. Prefer comprehensions over manual append loops for clarity.
4. Use `key=` sorting rather than custom comparator hacks.
5. Benchmark only after identifying hotspots.
