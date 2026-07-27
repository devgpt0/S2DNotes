# Python Sets

Sets are mutable, unordered collections of unique, hashable items. They do not support indexing or duplicate values.

## Creating Sets

```python
values = {1, 2, 3}
empty_values = set()
```

`{}` creates an empty dictionary, not an empty set. `set([1, 2, 2])` creates `{1, 2}`.

## Adding and Removing

- `add(item)` adds a single hashable item.
- `update(iterable)` adds every item from an iterable.
- `remove(item)` raises `KeyError` if the item is absent.
- `discard(item)` does nothing if the item is absent.
- `pop()` removes and returns an arbitrary item.
- `clear()` removes all items.

Lists, dictionaries, and sets are unhashable, so they cannot be set members. A tuple is allowed only when all of its items are hashable.

## Set Operations

For `first = {1, 2, 3}` and `second = {2, 3, 4}`:

- `first | second` or `first.union(second)` returns `{1, 2, 3, 4}`.
- `first & second` or `first.intersection(second)` returns `{2, 3}`.
- `first - second` or `first.difference(second)` returns `{1}`.
- `first ^ second` or `first.symmetric_difference(second)` returns `{1, 4}`.

Use `issubset()`, `issuperset()`, and `isdisjoint()` to compare sets. The `difference_update()` method changes the original set.

## Immutable Sets

`frozenset` is an immutable set. A `frozenset` whose items are hashable can be used as a dictionary key or as a member of another set.
