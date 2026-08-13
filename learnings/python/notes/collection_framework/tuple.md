# Python `tuple`
## 1) What is a tuple?
A tuple is an ordered, immutable sequence type in Python.

- Ordered: preserves insertion order.
- Immutable: tuple structure cannot be changed after creation.
- Heterogeneous: can hold mixed data types.
- Indexable and sliceable like lists.

```python
t = (10, "python", 3.14)
print(t[0])   # 10
```

Output:

```text
10
```

## 2) Creating tuples

### Standard creation
```python
t1 = (1, 2, 3)
t2 = 1, 2, 3          # parentheses optional (packing)
t3 = tuple([1, 2, 3]) # from iterable
```

### Empty tuple
```python
empty = ()
```

### Single-element tuple (important)
```python
a = (5,)   # tuple
b = (5)    # int, not tuple
```

## 3) Tuple packing and unpacking

### Packing
```python
t = 1, 2, 3
```

### Unpacking
```python
a, b, c = t
```

### Rule
Number of variables must match number of values (unless `*` is used).

```python
# ValueError
# a, b = (1, 2, 3)
```

### Extended unpacking (`*`)
```python
t = (1, 2, 3, 4, 5)
a, *mid, b = t
print(a)    # 1
print(mid)  # [2, 3, 4]
print(b)    # 5
```

Output:

```text
1
[2, 3, 4]
5
```

## 4) Accessing tuple elements

### Indexing
```python
t = (10, 20, 30, 40)
print(t[0])   # 10
print(t[-1])  # 40
```

Output:

```text
10
40
```

### Slicing
```python
t = (1, 2, 3, 5, 7)
print(t[1:4])   # (2, 3, 5)
print(t[::-1])  # (7, 5, 3, 2, 1)
print(t[::2])   # (1, 3, 7)
```

Output:

```text
(2, 3, 5)
(7, 5, 3, 2, 1)
(1, 3, 7)
```

## 5) Tuple operations

### Concatenation
```python
t = (1, 2) + (3, 4)
print(t)  # (1, 2, 3, 4)
```

Output:

```text
(1, 2, 3, 4)
```

### Repetition
```python
t = (1, 2) * 3
print(t)  # (1, 2, 1, 2, 1, 2)
```

Output:

```text
(1, 2, 1, 2, 1, 2)
```

### Membership
```python
print(2 in (1, 2, 3))  # True
```

Output:

```text
True
```

## 6) Immutability: what is and is not protected

Tuple structure is immutable, but inner mutable objects can still change.

```python
t = ([1, 2], [3, 4])
t[0][0] = 99
print(t)  # ([99, 2], [3, 4])
```

Output:

```text
([99, 2], [3, 4])
```

## 7) Tuple methods
Tuples have only two methods:

```python
t = (1, 2, 2, 3, 2)
print(t.count(2))  # 3
print(t.index(3))  # 3
```

Output:

```text
3
3
```

## 8) Useful built-ins with tuples
```python
t = (4, 1, 9, 2)
print(len(t))  # 4
print(min(t))  # 1
print(max(t))  # 9
print(sum(t))  # 16
```

Output:

```text
4
1
9
16
```

## 9) Tuple vs list

| Feature | Tuple | List |
|---|---|---|
| Mutability | Immutable | Mutable |
| Memory | Lower | Higher |
| Methods | Few (`count`, `index`) | Many |
| Hashable | Yes (if all elements hashable) | No |
| Typical use | Fixed records | Dynamic collections |

## 10) Hashability and dictionary keys
A tuple can be a dict key only if all elements are hashable.

```python
d = {(1, 2): "point"}   # valid

# invalid: list is unhashable
# d = {([1, 2], 3): "x"}
```

## 11) Function use: return values, `*args`, `**kwargs`

### Returning multiple values
```python
def get_xy():
    return 10, 20   # tuple packing

x, y = get_xy()     # unpacking
```

### `*args` and `**kwargs`
```python
def demo(a, *args, **kwargs):
    print(a)
    print(args)    # tuple
    print(kwargs)  # dict

demo(1, 2, 3, x=4, y=5)
```

Output:

```text
1
(2, 3)
{'x': 4, 'y': 5}
```

### Unpacking in function calls
```python
def add3(a, b, c):
    return a + b + c

t = (1, 2, 3)
print(add3(*t))   # 6
```

Output:

```text
6
```

## 12) Swapping and multiple assignment
```python
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5
```

Output:

```text
10 5
```

## 13) Loop unpacking
```python
pairs = [(1, 2), (3, 4), (5, 6)]
for x, y in pairs:
    print(x, y)
```

Output:

```text
1 2
3 4
5 6
```

## 14) Structural pattern matching (3.10+)
Works in Python 3.11+ exactly as below:

```python
point = (0, 7)

match point:
    case (0, y):
        print("On Y-axis:", y)
    case (x, 0):
        print("On X-axis:", x)
    case (x, y):
        print("General point:", x, y)
```

Output:

```text
On Y-axis: 7
```

## 15) Copy behavior: assignment, shallow copy, deep copy
Important for nested mutable elements.

```python
import copy

t1 = (1, [2, 3], 4)
t2 = t1                 # assignment
t3 = copy.copy(t1)      # shallow copy (tuple often reused)
t4 = copy.deepcopy(t1)  # deep copy

t1[1].append(99)
print(t2)  # (1, [2, 3, 99], 4)
print(t3)  # (1, [2, 3, 99], 4)
print(t4)  # (1, [2, 3], 4)
```

Output:

```text
(1, [2, 3, 99], 4)
(1, [2, 3, 99], 4)
(1, [2, 3], 4)
```

Notes:
- For immutable-only tuples, `copy.copy()` may return the same object.
- Tuple slicing like `t[:]` may also return the same object.

## 16) Performance notes (practical)
- Tuples are usually more memory-efficient than lists.
- Iteration can be slightly faster for tuples.
- Use tuples for fixed-size, read-only records.
- Use lists when frequent modifications are needed.

## 17) Common errors and pitfalls

1. Missing comma in single-element tuple.
```python
(1)    # int
(1,)   # tuple
```

2. Unpacking count mismatch.
```python
# ValueError: too many values to unpack
# a, b = (1, 2, 3)
```

3. Assuming tuple means deep immutability.
```python
t = ([1, 2],)
t[0].append(3)  # valid
```

## 18) When to use tuple
Use tuple when:
- Data shape is fixed.
- You want safe read-only intent.
- You need hashable compound keys.
- You are modeling records like coordinates, RGB, config keys.

Use list when:
- You add/remove/update often.
- Sequence length is dynamic.

## 19) Final mental model
- Packing: many values -> one tuple.
- Unpacking: one tuple -> many variables.
- `*args`: function-side positional packing into tuple.
- `*t` at call-site: tuple unpacking into arguments.
- Tuple protects structure, not inner mutable object state.

## 20) `namedtuple` and `typing.NamedTuple` (Missing but Useful)

When tuple position-only access becomes unclear, use named fields.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)
```

Output:

```text
10 20
```

Benefits:
- keeps tuple immutability and lightweight behavior.
- improves readability in records with fixed meaning.

## 21) Tuple as Stable Composite Keys

Tuples are ideal composite keys in dictionaries and sets.

```python
visits = {}
key = ("user-1", "2026-06-28")
visits[key] = visits.get(key, 0) + 1
print(visits[key])
```

Output:

```text
1
```

Use cases:
- caching
- grouped counters
- matrix coordinates

## 22) Hashability Edge Cases

Tuple is hashable only if all elements are hashable.

```python
ok = (1, "a", (2, 3))
# bad = (1, [2, 3])  # inner list makes tuple unhashable
```

## 23) Tuple vs Dataclass for Record Modeling

Choose tuple when:
- tiny immutable positional record is enough.

Choose dataclass when:
- named fields, defaults, validation, or methods are needed.

Interview line:
- tuples are minimal data carriers; dataclasses are richer domain models.

## 24) Sequence Protocol Behavior with Tuples

Tuples support sequence operations:
- `len(t)`
- indexing/slicing
- iteration
- membership (`in`)
- concatenation/repetition (`+`, `*`)

They do not support item assignment/deletion.

## 25) Advanced Unpacking Patterns

```python
record = ("INV-1", "paid", 1200, "USD", "2026-06-28")
invoice_id, status, amount, *_, date = record
print(invoice_id, amount, date)
```

Output:

```text
INV-1 1200 2026-06-28
```

Why useful:
- robust extraction from fixed-shape records.
- clean handling of "middle fields I do not need now."

## 26) Tuple in Pattern Matching (Interview Favorite)

```python
event = ("error", 504, "gateway timeout")

match event:
    case ("error", code, msg) if code >= 500:
        print("server-side error:", msg)
    case ("error", code, msg):
        print("client-side error:", msg)
    case _:
        print("other event")
```

Output:

```text
server-side error: gateway timeout
```

## 27) Tuple Memory and Performance Positioning

In practice tuples are often:
- slightly smaller in memory than lists.
- a little faster to iterate for same elements.

But major wins usually come from algorithm and data-shape decisions, not micro-optimizing tuple vs list alone.

## 28) When Tuple Harms Readability

Problem pattern:
- long tuples with magic index usage (`row[6]`, `row[9]`).

Refactor choices:
- `namedtuple`
- `dataclass`
- small class/domain object

Rule:
- if readers need comments to remember index meaning, tuple is too implicit.

## 29) Tuple-Centric Interview Problems

1. Use tuple keys in frequency maps.
2. Normalize pair keys (sorted tuple) for undirected relationships.
3. Nested unpacking in loops and comprehensions.
4. Distinguish hashable tuple vs tuple containing mutable object.

## 30) Tuple Mastery Checklist

1. Single-item tuple comma rule is automatic.
2. Packing/unpacking is second nature.
3. `*` extended unpacking is comfortable.
4. Hashability rules are clear for keys.
5. You can choose tuple vs namedtuple vs dataclass correctly.
