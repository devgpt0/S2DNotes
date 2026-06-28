# Type Hints and Static Analysis Mastery

## 1) Why Typing in Dynamic Python

Type hints improve:
- readability
- editor support
- refactor safety
- cross-team contracts

## 2) Start with Boundary Typing

Prioritize hints on:
- public functions
- service interfaces
- data transfer objects

## 3) Practical Hinting Patterns

```python
from collections.abc import Iterable, Mapping


def summarize(values: Iterable[int], config: Mapping[str, int]) -> int:
    return sum(values) + config.get("base", 0)
```

Prefer interface types (`Iterable`, `Mapping`) over concrete (`list`, `dict`) when mutation is not required.

## 4) Optional and Union Types

```python
def normalize_name(name: str | None) -> str:
    if name is None:
        return "unknown"
    return name.strip().lower()
```

## 5) Typed Data Models

Use:
- `TypedDict` for dict-like structured data
- `dataclass` for richer domain models

## 6) Generics and Reusable APIs

Generic helpers should preserve input-output type intent where possible.

## 7) Static Analysis Workflow

Common tools:
- mypy
- pyright

Adoption plan:
1. enable for changed/new files first
2. tighten settings gradually
3. avoid mass "ignore everything" patterns

## 8) Runtime vs Static Types

Type hints are mostly static tooling guidance.
They do not automatically enforce runtime checks unless you add explicit validation.

## 9) Common Pitfalls

- over-typing trivial local variables
- forcing complex type constructs that hurt readability
- ignoring Optional None-path handling
- using concrete mutable types in interfaces unnecessarily

## 10) Interview Points

1. Why type against `Mapping`/`Sequence`?
2. Difference between runtime checks and static checks?
3. When to use `TypedDict` vs `dataclass`?
4. How to roll typing into legacy code incrementally?
