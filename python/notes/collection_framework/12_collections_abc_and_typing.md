# `collections.abc` and Typing for Collection Design

This file covers abstraction-level mastery for designing reusable collection APIs.

## 1) Why `collections.abc` Matters

`collections.abc` provides interfaces that describe behavior:
- `Iterable`
- `Iterator`
- `Sequence`
- `MutableSequence`
- `Set` / `MutableSet`
- `Mapping` / `MutableMapping`

Use these in type hints to express contracts by behavior, not concrete class.

## 2) Prefer Interface Hints over Concrete Types

Better:

```python
from collections.abc import Mapping, Iterable


def summarize(config: Mapping[str, int], values: Iterable[int]) -> int:
    return config.get("base", 0) + sum(values)
```

Less flexible:
- forcing `dict` and `list` when only mapping/iterable behavior is needed.

## 3) Read-Only vs Mutable Contracts

Use the narrowest valid contract:
- `Mapping` for read-only mapping requirements
- `MutableMapping` when writes are required
- `Sequence` when index access needed but mutation not required
- `Iterable` when only traversal is needed

This reduces accidental misuse and improves API clarity.

## 4) Runtime Checks with ABCs

```python
from collections.abc import Mapping

def load_settings(obj):
    if not isinstance(obj, Mapping):
        raise TypeError("Expected mapping-like input")
    return dict(obj)
```

## 5) Generic Type Parameters (Typing Layer)

```python
from collections.abc import Mapping

def invert_unique(d: Mapping[str, int]) -> dict[int, str]:
    out: dict[int, str] = {}
    for k, v in d.items():
        if v in out:
            raise ValueError("values must be unique")
        out[v] = k
    return out
```

## 6) Protocol vs ABC for Collection-Like APIs

Two design styles:
- ABC: explicit inheritance contract.
- Protocol: structural typing (duck typing with static guarantees).

Use Protocol when:
- you want behavior-based compatibility without inheritance coupling.

## 7) Custom Container Design Checklist

1. choose correct base abstraction (`MutableMapping`, etc.).
2. define mutation semantics clearly.
3. document iteration order guarantees.
4. define equality/hash behavior explicitly.
5. ensure predictable copy/serialization behavior.

## 8) Missing Pitfalls in Collection API Design

- exposing mutable internals directly.
- requiring concrete `list`/`dict` unnecessarily.
- mixing read/write responsibilities in one broad API.
- returning non-deterministic order to external interfaces unintentionally.

## 9) Interview-Ready Design Statements

1. "I type against `Mapping` when mutation is not required."
2. "I use `Sequence` for indexable read-only access."
3. "I keep APIs abstraction-first and convert to concrete types at boundaries."
4. "I choose narrow contracts to reduce coupling and bugs."
