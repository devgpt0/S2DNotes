# Dataclasses, Protocols, and Domain Modeling
## 1. Core truth

Dataclasses reduce repetitive class boilerplate.
Protocols describe behavior contracts without forcing a class hierarchy.
Domain modeling means shaping your classes around the real business concepts.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Product:
    sku: str
    price: float
    quantity: int

product = Product("P-100", 19.99, 3)
print(product)
```

Output:

```text
Product(sku='P-100', price=19.99, quantity=3)
```

The dataclass automatically gives `Product` a readable `__repr__`, so printing the object shows its fields.

## 2. Domain-model foundations

### Dataclasses remove boilerplate

```python
from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    price: float
    quantity: int

product = Product("P-100", 19.99, 3)
print(product)
```

Output:

```text
Product(sku='P-100', price=19.99, quantity=3)
```

Practical takeaway: use a dataclass when the class mainly stores data and the default generated methods are a good fit.

### Frozen dataclasses model value objects

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

money = Money(12.5, "USD")
print(money.amount)
```

Output:

```text
12.5
```

Practical takeaway: use `frozen=True` when the object should not change after it is created.

### `default_factory` creates a fresh mutable value

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)

cart = Cart()
cart.items.append("book")
print(cart.items)
```

Output:

```text
['book']
```

Practical takeaway: use `default_factory` instead of a mutable default like `[]`.

### `__post_init__` enforces invariants

```python
from dataclasses import dataclass

@dataclass
class Account:
    balance: float

    def __post_init__(self) -> None:
        if self.balance < 0:
            raise ValueError("balance cannot be negative")

account = Account(100.0)
print(account.balance)
```

Output:

```text
100.0
```

Practical takeaway: use `__post_init__` for validation that must happen after all fields are assigned.

## 3. Modeling tools

### `field(default_factory=...)`

Use this for lists, dictionaries, sets, or any other mutable default that should be fresh for each object.

### `__post_init__()`

Use this to validate invariant rules after object creation.

### `frozen=True`

Use this for value objects that should not be mutated.

### `slots=True`

Use this when you want leaner instances and fewer accidental attributes.

### `Protocol`

Use it to describe behavior that multiple unrelated classes can provide.

```python
from dataclasses import dataclass
from typing import Protocol

class PaymentGateway(Protocol):
    def charge(self, amount: float) -> str:
        ...

@dataclass
class FakeGateway:
    prefix: str = "TXN"

    def charge(self, amount: float) -> str:
        return f"{self.prefix}-{int(amount)}"

def place_order(gateway: PaymentGateway, amount: float) -> str:
    return gateway.charge(amount)

print(place_order(FakeGateway(), 42.0))
```

Output:

```text
TXN-42
```

The function only needs something with a `charge()` method, so the concrete class can vary.

## 4. Practical domain models

### Example 1: Simple product model

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Product:
    sku: str
    price: float
    quantity: int

product = Product("P-101", 29.5, 2)
print(product)
```

Output:

```text
Product(sku='P-101', price=29.5, quantity=2)
```

### Example 2: Immutable money value

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

money = Money(99.0, "USD")
print(money)
```

Output:

```text
Money(amount=99.0, currency='USD')
```

### Example 3: Cart with a safe list default

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)

cart = Cart()
cart.items.append("pen")
cart.items.append("notebook")
print(cart.items)
```

Output:

```text
['pen', 'notebook']
```

- Use dataclasses for input/output models and simple domain objects.
- Use frozen dataclasses for value objects such as money, coordinates, or identifiers.
- Use `default_factory` for collections owned by one instance.
- Use protocols for services that may have multiple implementations.

## 5. Modeling mistakes

### Mistake 1: Using a mutable default directly

Wrong:

```python
from dataclasses import dataclass

@dataclass
class Cart:
    items: list[str] = []
```

Correct:

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)
```

Rule to remember: never use a shared mutable default for per-instance data.

### Mistake 2: Using a dataclass for a class with heavy behavior

If the class has complicated logic, a normal class may be clearer.

### Mistake 3: Forgetting invariants

If balance cannot be negative, validate it at construction time.

### Mistake 4: Forcing inheritance when a protocol is enough

If the code only needs a method contract, a `Protocol` is often cleaner.

## 6. Modeling decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Simple data holder | `dataclass` | low boilerplate | the class has complex lifecycle rules |
| Immutable value object | `frozen=True` dataclass | protects state | the object must change often |
| Fresh mutable default | `default_factory` | avoids shared state | the field is not mutable |
| Behavioral contract | `Protocol` | flexible substitution | you need runtime inheritance rules |
| Strict runtime interface | ABC | explicit inheritance contract | structural typing is enough |

Selection rule:

- Start with a dataclass for plain data.
- Use `frozen=True` for values that should not change.
- Use `Protocol` when behavior matters more than the class hierarchy.

## 7. Safety and maintainability

- `slots=True` can reduce memory and prevent accidental attributes.
- `frozen=True` makes value objects safer to share.
- `default_factory` prevents hidden shared mutable state.
- Keep validation close to construction so invalid objects fail fast.

Best practices:

- Keep field names meaningful and domain-oriented.
- Validate important invariants in one place.
- Use protocols to reduce coupling between services and implementations.

## 8. Advanced model contracts

### Entity versus value object

- Entity: identity matters over time.
- Value object: the value itself matters, not identity.

### Structural typing with `Protocol`

Protocols let you say "any object with the right method is acceptable."
That is useful when different implementations should be swappable.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| Dataclass | reduces boilerplate |
| Frozen dataclass | immutable value object |
| `default_factory` | fresh mutable default |
| `__post_init__` | validate after init |
| `Protocol` | behavior contract |
| Domain modeling | identity vs value matters |

## 10. Dataclass API stability

`kw_only=True` prevents positional call sites from depending on field order;
`slots=True` removes the normal per-instance `__dict__` unless inherited layout
requires otherwise.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Money:
    amount: int
    currency: str


money = Money(amount=500, currency="INR")
print(money)
print(hasattr(money, "__dict__"))
```

Output:

```text
Money(amount=500, currency='INR')
False
```

Use `weakref_slot=True` with `slots=True` only when instances must support weak
references. Do not add it by default.

## 11. Dataclass-like transforms

Library authors can annotate a decorator or metaclass with
`typing.dataclass_transform` so static type checkers understand generated
initializers and field behavior. It supplies typing metadata; it does not create
runtime dataclass behavior by itself.

Application code should prefer `@dataclass` directly unless a framework already
owns model construction.
