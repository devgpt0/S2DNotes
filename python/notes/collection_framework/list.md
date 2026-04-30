# Python List Notes

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

## 18) Recommended Practice Flow

1. Master create/read/update/delete operations
2. Practice slicing and negative indices
3. Practice copy semantics (alias vs shallow vs deep)
4. Build list comprehension problems daily
5. Solve nested-list matrix-style tasks
6. Practice sort with `key`, `lambda`, `reverse`
7. Practice 20+ output-prediction snippets
