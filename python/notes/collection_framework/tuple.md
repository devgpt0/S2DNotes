# Tuple in Python (3.11+) - Complete Worksheet Notes

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

## 4) Accessing tuple elements

### Indexing
```python
t = (10, 20, 30, 40)
print(t[0])   # 10
print(t[-1])  # 40
```

### Slicing
```python
t = (1, 2, 3, 5, 7)
print(t[1:4])   # (2, 3, 5)
print(t[::-1])  # (7, 5, 3, 2, 1)
print(t[::2])   # (1, 3, 7)
```

## 5) Tuple operations

### Concatenation
```python
t = (1, 2) + (3, 4)
print(t)  # (1, 2, 3, 4)
```

### Repetition
```python
t = (1, 2) * 3
print(t)  # (1, 2, 1, 2, 1, 2)
```

### Membership
```python
print(2 in (1, 2, 3))  # True
```

## 6) Immutability: what is and is not protected

Tuple structure is immutable, but inner mutable objects can still change.

```python
t = ([1, 2], [3, 4])
t[0][0] = 99
print(t)  # ([99, 2], [3, 4])
```

## 7) Tuple methods
Tuples have only two methods:

```python
t = (1, 2, 2, 3, 2)
print(t.count(2))  # 3
print(t.index(3))  # 3
```

## 8) Useful built-ins with tuples
```python
t = (4, 1, 9, 2)
print(len(t))  # 4
print(min(t))  # 1
print(max(t))  # 9
print(sum(t))  # 16
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

### Unpacking in function calls
```python
def add3(a, b, c):
    return a + b + c

t = (1, 2, 3)
print(add3(*t))   # 6
```

## 12) Swapping and multiple assignment
```python
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5
```

## 13) Loop unpacking
```python
pairs = [(1, 2), (3, 4), (5, 6)]
for x, y in pairs:
    print(x, y)
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
