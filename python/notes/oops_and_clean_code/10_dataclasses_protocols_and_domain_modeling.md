# Dataclasses, Protocols, and Domain Modeling

## 1) Dataclass for Clear Data Models

```python
from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    sku: str
    price: float
    quantity: int
```

Why:
- concise boilerplate reduction
- clearer data intent
- `slots=True` can reduce per-instance memory overhead

## 2) Frozen Dataclasses for Value Objects

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str
```

Use for immutable domain values.

## 3) `field(default_factory=...)` for Mutable Defaults

```python
from dataclasses import dataclass, field


@dataclass
class Cart:
    items: list[str] = field(default_factory=list)
```

Never use mutable defaults directly.

## 4) Protocol for Structural Contracts

```python
from typing import Protocol


class PaymentGateway(Protocol):
    def charge(self, amount: float) -> str:
        ...
```

Benefits:
- caller depends on behavior contract, not concrete class hierarchy.

## 5) ABC vs Protocol Decision

- ABC: explicit inheritance, strong runtime contract style.
- Protocol: structural typing, lower coupling, easier substitution.

## 6) Domain Modeling Heuristics

Ask:
1. Is this concept an entity (identity over time)?
2. Is it a value object (immutable value semantics)?
3. Is this behavior domain logic or infrastructure concern?

## 7) Invariant Enforcement

Use `__post_init__` for dataclass validation:

```python
from dataclasses import dataclass


@dataclass
class Account:
    balance: float

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("balance cannot be negative")
```

## 8) Interview Questions

1. Dataclass vs normal class tradeoffs?
2. When to use `frozen=True`?
3. ABC vs Protocol?
4. How to model invariants safely?
