# PYTHON - DATA TYPES

A data type defines a value's behavior, supported operations, and mutability.

## 1. Everything Is an Object

Every Python value is an object with a type and identity.

```python
value = 10

print(value)
print(type(value).__name__)
print(isinstance(value, object))
```

Output:

```text
10
int
True
```

## 2. Dynamic Typing

A name has no permanent type. It can be rebound to an object of another type.

```python
value = 10
print(type(value).__name__)

value = "ten"
print(type(value).__name__)
```

Output:

```text
int
str
```

Objects have types; names reference objects.

## 3. Main Built-in Types

| Category | Types |
| --- | --- |
| Numeric | `int`, `float`, `complex`, `bool` |
| Text | `str` |
| Sequence | `list`, `tuple`, `range` |
| Mapping | `dict` |
| Set | `set`, `frozenset` |
| Binary | `bytes`, `bytearray`, `memoryview` |
| Null value | `NoneType` |

## 4. Integers: `int`

Integers represent whole numbers and can grow beyond fixed machine-word limits.

```python
small = 42
large = 10**30

print(small)
print(large)
print(type(large).__name__)
```

Output:

```text
42
1000000000000000000000000000000
int
```

## 5. Floating-Point Numbers: `float`

Floats represent binary floating-point numbers. Many decimal fractions are approximate.

```python
result = 0.1 + 0.2

print(result)
print(result == 0.3)
```

Output:

```text
0.30000000000000004
False
```

Use `decimal.Decimal` when exact decimal arithmetic is required.

## 6. Complex Numbers: `complex`

A complex number has real and imaginary parts. Python uses `j` for the imaginary unit.

```python
number = 3 + 4j

print(number.real)
print(number.imag)
print(abs(number))
```

Output:

```text
3.0
4.0
5.0
```

## 7. Booleans: `bool`

`bool` has two values: `True` and `False`. It is a subclass of `int`.

```python
print(True + True)
print(False * 10)
print(isinstance(True, int))
```

Output:

```text
2
0
True
```

Use Booleans for conditions, not as numeric substitutes.

## 8. Null Value: `None`

`None` means no value or no result. It is the only `NoneType` object.

```python
result = None

print(result)
print(type(result).__name__)
print(result is None)
```

Output:

```text
None
NoneType
True
```

Check it with `is None`, not `== None`.

## 9. Strings: `str`

A string is an immutable sequence of Unicode characters.

```python
language = "Python"

print(language[0])
print(language[-1])
print(language[1:4])
print(len(language))
```

Output:

```text
P
n
yth
6
```

String operations create new strings.

```python
name = "Py"
combined = name + "thon"

print(name)
print(combined)
print(name is combined)
```

Output:

```text
Py
Python
False
```

## 10. Lists: `list`

A list is an ordered, mutable sequence that allows duplicates.

```python
numbers = [10, 20, 20]
numbers.append(30)
numbers[0] = 5

print(numbers)
print(numbers[1])
```

Output:

```text
[5, 20, 20, 30]
20
```

Use a list when order matters and items may change.

## 11. Tuples: `tuple`

A tuple is an ordered, immutable sequence.

```python
point = (4, 7)
x, y = point

print(point)
print(x)
print(y)
```

Output:

```text
(4, 7)
4
7
```

A one-item tuple needs a trailing comma:

```python
value = (10,)

print(value)
print(type(value).__name__)
```

Output:

```text
(10,)
tuple
```

## 12. Ranges: `range`

`range` is an immutable sequence of integers generated lazily.

```python
numbers = range(2, 8, 2)

print(list(numbers))
print(numbers[1])
print(6 in numbers)
```

Output:

```text
[2, 4, 6]
4
True
```

The stop value is excluded.

## 13. Dictionaries: `dict`

A dictionary maps unique hashable keys to values and preserves insertion order.

```python
profile = {"name": "Ana", "role": "Developer"}
profile["active"] = True
profile["role"] = "Lead"

print(profile)
print(profile["name"])
```

Output:

```text
{'name': 'Ana', 'role': 'Lead', 'active': True}
Ana
```

Dictionary membership checks keys.

```python
profile = {"name": "Ana"}

print("name" in profile)
print("Ana" in profile)
```

Output:

```text
True
False
```

## 14. Sets: `set`

A set is a mutable collection of unique hashable values.

```python
numbers = {3, 1, 2, 3}
numbers.add(4)

print(sorted(numbers))
print(2 in numbers)
```

Output:

```text
[1, 2, 3, 4]
True
```

Set display order is not a stable contract, so examples sort the result.

## 15. Frozen Sets: `frozenset`

A `frozenset` is an immutable set and can be used as a dictionary key.

```python
permissions = frozenset({"read", "write"})
access = {permissions: "editor"}

print(sorted(permissions))
print(access[permissions])
```

Output:

```text
['read', 'write']
editor
```

## 16. Bytes: `bytes`

`bytes` is an immutable sequence of integers from `0` to `255`.

```python
data = b"ABC"

print(data)
print(data[0])
print(data.decode("utf-8"))
```

Output:

```text
b'ABC'
65
ABC
```

Text is `str`; encoded binary data is `bytes`.

## 17. Byte Arrays: `bytearray`

`bytearray` is the mutable counterpart of `bytes`.

```python
data = bytearray(b"ABC")
data[0] = 90

print(data)
print(bytes(data))
```

Output:

```text
bytearray(b'ZBC')
b'ZBC'
```

## 18. Mutable and Immutable Types

Mutation changes an existing object. Immutable objects cannot change after creation.

| Usually mutable | Immutable |
| --- | --- |
| `list` | `int`, `float`, `complex`, `bool` |
| `dict` | `str`, `tuple`, `range` |
| `set` | `bytes`, `frozenset`, `NoneType` |
| `bytearray` |  |

```python
items = [1, 2]
items_before = id(items)
items.append(3)

text = "Py"
text_before = id(text)
text += "thon"

print(id(items) == items_before)
print(id(text) == text_before)
```

Output:

```text
True
False
```

The list is mutated. String concatenation creates a new string.

## 19. Tuple Immutability Is Shallow

A tuple cannot replace its elements, but it may contain a mutable object.

```python
record = ("scores", [80, 90])
record[1].append(100)

print(record)
```

Output:

```text
('scores', [80, 90, 100])
```

The tuple still references the same list; the list itself changed.

## 20. Hashable Values

A hashable value has a stable hash and can be a dictionary key or set member.

```python
valid_key = (1, 2)
mapping = {valid_key: "point"}

print(mapping[(1, 2)])

try:
    hash([1, 2])
except TypeError as error:
    print(type(error).__name__)
```

Output:

```text
point
TypeError
```

Most immutable built-in values are hashable. Lists, dictionaries, and sets are not.

## 21. Nested Collections

Collections can contain other objects. Inner mutable objects remain mutable.

```python
students = [
    {"name": "Ana", "scores": [90, 95]},
    {"name": "Ravi", "scores": [80, 85]},
]

students[0]["scores"].append(100)
print(students[0])
```

Output:

```text
{'name': 'Ana', 'scores': [90, 95, 100]}
```

Trace each level separately when reasoning about nested data.

## 22. Choosing a Collection

| Need | Type |
| --- | --- |
| ordered, changeable items | `list` |
| fixed record or immutable sequence | `tuple` |
| key-value lookup | `dict` |
| unique values and set operations | `set` |
| immutable unique values | `frozenset` |
| lazy integer sequence | `range` |
| immutable binary data | `bytes` |
| mutable binary data | `bytearray` |

## 23. Final Mental Model

For any value, ask:

1. What is its exact type?
2. Is it mutable?
3. Is it ordered?
4. Does it allow duplicates?
5. Is it hashable?
6. Which operations does its type support?

Remember:

- names reference typed objects;
- mutable objects can change in place;
- immutable operations create new objects;
- equality compares values, while identity compares objects;
- choose a data type from required behavior, not habit.
