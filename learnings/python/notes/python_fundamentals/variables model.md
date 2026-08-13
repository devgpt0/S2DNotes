# PYTHON - VARIABLES AND NAME BINDING

A Python variable is just a label(reference) to an object in the memory

## 1. Assignment Binds a Name

Assignment evaluates the right side, then binds the left-side name to that object.

```python
score = 95

print(score)
print(type(score).__name__)
```

Output:

```text
95
int
```

## 2. Names Are Dynamically Typed

A name can be rebound to an object of another type.

```python
result = 10
print(result, type(result).__name__)

result = "complete"
print(result, type(result).__name__)
```

Output:

```text
10 int
complete str
```

The objects have types; the name does not have a fixed runtime type.

## 3. Identifier Rules

A variable name:

- may contain letters, digits, and underscores;
- cannot start with a digit;
- cannot be a Python keyword;
- is case-sensitive.

```python
user_name = "Ana"
user2 = "Ravi"
name = "lower"
Name = "upper"

print(user_name, user2)
print(name, Name)
```

Output:

```text
Ana Ravi
lower upper
```

## 4. Naming Conventions

| Name kind | Convention | Example |
| --- | --- | --- |
| variable | `snake_case` | `total_price` |
| function | `snake_case` | `calculate_total` |
| class | `PascalCase` | `OrderItem` |
| constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| internal name | leading underscore | `_cache` |

Use meaningful names that describe purpose, not implementation detail.

```python
item_count = 3
unit_price = 10
total_price = item_count * unit_price

print(total_price)
```

Output:

```text
30
```

## 5. Assignment Does Not Copy an Object

Assigning one name to another copies the reference.

```python
first = [1, 2]
second = first

print(first is second)
second.append(3)
print(first)
```

Output:

```text
True
[1, 2, 3]
```

Both names reference the same list.

## 6. Rebinding

Rebinding makes a name reference another object. It does not alter the old object.

```python
first = [1, 2]
second = first
second = [9, 10]

print(first)
print(second)
print(first is second)
```

Output:

```text
[1, 2]
[9, 10]
False
```

## 7. Mutation

Mutation changes an existing object without changing its identity.

```python
numbers = [1, 2]
identity_before = id(numbers)
numbers.append(3)

print(numbers)
print(id(numbers) == identity_before)
```

Output:

```text
[1, 2, 3]
True
```

## 8. Immutable Reassignment

Immutable values cannot change. An apparent update creates and binds a new object.

```python
number = 10
identity_before = id(number)
number += 1

print(number)
print(id(number) == identity_before)
```

Output:

```text
11
False
```

## 9. Multiple Assignment

Python can bind several names in one statement.

```python
name, age, active = "Ana", 25, True

print(name)
print(age)
print(active)
```

Output:

```text
Ana
25
True
```

The number of target names must match the number of values unless starred unpacking is used.

## 10. Chained Assignment

Chained assignment binds every name to the same object.

```python
first = second = []
first.append("shared")

print(second)
print(first is second)
```

Output:

```text
['shared']
True
```

Avoid chained assignment with mutable objects when independent values are intended.

## 11. Sequence Unpacking

Unpacking binds items from an iterable to separate names.

```python
point = (4, 7)
x, y = point

print(x)
print(y)
```

Output:

```text
4
7
```

## 12. Starred Unpacking

A starred target collects remaining items into a list.

```python
first, *middle, last = [1, 2, 3, 4, 5]

print(first)
print(middle)
print(last)
```

Output:

```text
1
[2, 3, 4]
5
```

Only one target may be starred in one assignment level.

## 13. Swapping Values

Python evaluates the right side before binding the left side.

```python
left = 10
right = 20
left, right = right, left

print(left, right)
```

Output:

```text
20 10
```

No temporary variable is required.

## 14. Augmented Assignment

Augmented assignment reads, operates, then rebinds or mutates depending on the type.

```python
number = 5
number += 2

items = [1]
alias = items
items += [2]

print(number)
print(items)
print(alias)
```

Output:

```text
7
[1, 2]
[1, 2]
```

Integer `+=` creates a new integer. List `+=` mutates the list.

## 15. Deleting a Name

`del name` removes the binding. It does not necessarily destroy the object.

```python
first = [1, 2]
second = first
del first

print(second)

try:
    print(first)
except NameError as error:
    print(type(error).__name__)
```

Output:

```text
[1, 2]
NameError
```

The list remains alive because `second` still references it.

## 16. Variable Annotations

An annotation documents the expected type. It does not enforce the type at runtime.

```python
count: int = 3
print(count, type(count).__name__)

count = "three"
print(count, type(count).__name__)
```

Output:

```text
3 int
three str
```

Static type checkers can report the incompatible reassignment.

## 17. Function Parameters Are Local Bindings

A parameter becomes a local name bound to the passed object.

```python
def append_item(items):
    print(items is original)
    items.append(3)


original = [1, 2]
append_item(original)
print(original)
```

Output:

```text
True
[1, 2, 3]
```

Python uses object sharing: mutation is visible, local rebinding is not.

```python
def replace(items):
    items = [9]
    print(items)


original = [1, 2]
replace(original)
print(original)
```

Output:

```text
[9]
[1, 2]
```

## 18. Local and Global Names

Assignment inside a function creates a local name unless declared `global` or `nonlocal`.

```python
status = "global"


def show_status():
    status = "local"
    print(status)


show_status()
print(status)
```

Output:

```text
local
global
```

Prefer parameters and return values to mutable global state.

## 19. Common Assignment Error

Reading a name before binding it raises `NameError`.

```python
try:
    print(total)
except NameError as error:
    print(type(error).__name__)

total = 10
print(total)
```

Output:

```text
NameError
10
```

## 20. Final Mental Model

For each assignment, trace:

1. Which right-side expression is evaluated?
2. Which object is produced or fetched?
3. Which name is bound to that object?
4. Do multiple names share the object?
5. Does the next operation mutate the object or rebind the name?

Remember:

- assignment binds names; it does not copy objects;
- mutation changes an object;
- rebinding changes a name-to-object connection;
- `del` removes a binding;
- parameters are local bindings to argument objects.
