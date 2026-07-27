# Python Lists

Lists are ordered, mutable collections. They allow duplicate values and can hold values of different types.

## Creating and Accessing

```python
values = [10, 20, 30]
first = values[0]
last = values[-1]
middle = values[1:3]
```

Use `len(values)` for the number of items and `value in values` to test membership.

## Adding and Removing

- `append(item)` adds one item at the end.
- `extend(iterable)` adds each item from an iterable.
- `insert(index, item)` inserts an item at an index.
- `pop()` removes and returns the final item; `pop(index)` uses a specific index.
- `remove(item)` removes the first matching value and raises `ValueError` when absent.
- `clear()` removes every item.
- `del values[index]` deletes an item by index.

## Ordering and Copying

`sort()` and `reverse()` change the existing list and return `None`. Use `sorted(values)` or `list(reversed(values))` when a new list is required.

Assignment shares the same list object:

```python
first = [1, 2]
second = first
```

Use `first.copy()` or `first[:]` for a shallow copy. A shallow copy does not copy nested objects.

## Common Operations

- `count(value)` counts matching values.
- `index(value)` returns the first matching index and raises `ValueError` when absent.
- List comprehensions create transformed lists, for example `[value * 2 for value in values]`.

Avoid `[[0] * columns] * rows` for independent nested rows because its inner lists are shared. Use `[[0] * columns for _ in range(rows)]` instead.
