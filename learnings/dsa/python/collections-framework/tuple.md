# Python Tuples

Tuples are ordered, immutable collections. They allow duplicate values and can contain different types.

## Creating Tuples

```python
point = (10, 20)
single_value = (5,)
empty_values = ()
```

The comma creates a tuple: `(5)` is an integer, while `(5,)` is a one-item tuple. Parentheses are optional in many contexts, so `1, 2, 3` is also a tuple.

## Access and Operations

Tuples support indexing, negative indexing, slicing, membership testing, concatenation, and repetition.

```python
values = (1, 2, 3)
values[0]       # 1
values[1:]      # (2, 3)
values + (4,)   # (1, 2, 3, 4)
```

An item reference cannot be reassigned. Attempting `values[0] = 9` raises `TypeError`.

## Methods and Unpacking

Tuples provide `count(value)` and `index(value)`. `index()` raises `ValueError` when the value is absent.

```python
x, y = (10, 20)
first, *middle, last = (1, 2, 3, 4)
```

The starred target receives a list. Tuple packing and unpacking also allow value swapping: `a, b = b, a`.

## Hashability

A tuple can be a dictionary key or set member only when all of its contained values are hashable. A tuple can contain a list, but then the tuple itself is unhashable. Immutability prevents changing the tuple's item references, not changing a mutable object stored inside it.

Tuples are well suited to fixed records such as coordinates and function results with a stable number of values.
