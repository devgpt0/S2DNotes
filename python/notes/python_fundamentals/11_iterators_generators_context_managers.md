# Iterators, Generators, and Context Managers Mastery

## 1) Iterable vs Iterator vs Generator

- Iterable: object you can loop over (`list`, `dict`, `set`, file).
- Iterator: object with `__next__()` and stateful progression.
- Generator: concise iterator created with `yield`.

## 2) Why This Matters

Mastery here gives:
- lower memory usage
- cleaner streaming pipelines
- safer resource handling

## 3) Generator Basics

```python
def chunks(data: list[int], size: int):
    for i in range(0, len(data), size):
        yield data[i : i + size]
```

Use when data can be processed incrementally.

## 4) Generator Expressions

```python
nums = [1, 2, 3, 4]
squares = (x * x for x in nums)
print(sum(squares))
```

Guideline:
- prefer generator expressions for one-pass aggregate operations.

## 5) `yield from` for Composition

```python
def flatten(parts):
    for p in parts:
        yield from p
```

This keeps nested iteration logic simple.

## 6) Iterator Pitfalls

- iterators are one-pass (consumed after iteration).
- calling `list()` on huge generators removes memory advantage.
- mixing lazy iterables with side effects can cause hard-to-trace bugs.

## 7) Context Manager Fundamentals

`with` ensures deterministic cleanup.

```python
from pathlib import Path

def first_line(path: Path) -> str:
    with path.open("r", encoding="utf-8") as file:
        return file.readline().strip()
```

## 8) Custom Context Managers

```python
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer(label: str):
    start = perf_counter()
    try:
        yield
    finally:
        print(label, perf_counter() - start)
```

## 9) Async Context Managers (Bridge to Async Module)

In async code, resources often require `async with`.
Same cleanup principle, async lifecycle.

## 10) Interview Must-Know Points

1. `yield` pauses function state.
2. Generator function returns iterator, not final computed collection.
3. `with` is safer than manual open/close.
4. `finally`-style cleanup behavior applies even on exceptions.

## 11) Production Checklist

1. Stream large data with generators.
2. Use `with` for files/locks/connections.
3. Keep generator functions side-effect light.
4. Document whether function returns concrete collection or iterator.
