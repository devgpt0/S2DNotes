# Python Dictionaries

Dictionaries map unique, hashable keys to values. In modern Python, dictionaries preserve insertion order.

## Creating and Reading

```python
student = {"name": "Sam", "score": 90}
score = student["score"]
```

Bracket access raises `KeyError` when the key is absent. Use `student.get("score")` to receive `None` for an absent key, or `student.get("score", 0)` for an explicit default.

## Adding, Updating, and Removing

- `data[key] = value` adds a key or replaces its value.
- `update(other)` merges another mapping or iterable of key-value pairs into the existing dictionary.
- `pop(key)` removes and returns a value; it raises `KeyError` for a missing key unless a default is supplied.
- `popitem()` removes and returns the most recently inserted pair.
- `del data[key]` deletes a key-value pair.
- `clear()` removes every pair.
- `setdefault(key, default)` returns the current value, or inserts and returns `default` when the key is absent.

## Iteration

```python
for key in data:
    pass

for key, value in data.items():
    pass
```

`keys()`, `values()`, and `items()` return dynamic views. `key in data` tests keys, not values.

## Copying and Merging

`data.copy()` creates a shallow copy. The `|` operator creates a merged dictionary, with right-side values replacing matching left-side values:

```python
merged = {"a": 1} | {"a": 2, "b": 3}
# {"a": 2, "b": 3}
```

Lists and dictionaries cannot be keys because they are mutable and unhashable. Tuples may be keys only when all contained values are hashable.
