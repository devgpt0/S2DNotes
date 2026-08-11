# PYTHON - TYPE HINTS AND STATIC ANALYSIS

Type hints describe expected values for readers and static tools. They do not validate runtime data.

## 1. Function Annotations

Annotate parameters after `:` and the return type after `->`.

```python
def total(price: int, quantity: int) -> int:
    return price * quantity


print(total(10, 3))
print(total.__annotations__)
```

Output:

```text
30
{'price': <class 'int'>, 'quantity': <class 'int'>, 'return': <class 'int'>}
```

Annotations become metadata that tools can inspect.

## 2. Hints Do Not Enforce Types

Python normally runs code even when arguments conflict with annotations.

```python
def combine(left: int, right: int) -> int:
    return left + right


print(combine(2, 3))
print(combine("Py", "thon"))
```

Output:

```text
5
Python
```

A static checker reports the second call. Runtime validation is separate.

## 3. Variable Annotations

Variable annotations document intended types.

```python
name: str = "Ana"
age: int = 25
scores: list[int] = [90, 95]

print(name)
print(age)
print(scores)
```

Output:

```text
Ana
25
[90, 95]
```

## 4. Collection Types

Use built-in generic syntax in Python 3.9+.

```python
names: list[str] = ["Ana", "Ravi"]
point: tuple[int, int] = (4, 7)
scores: dict[str, int] = {"Ana": 95}
tags: set[str] = {"python", "typing"}

print(names)
print(point)
print(scores["Ana"])
print(sorted(tags))
```

Output:

```text
['Ana', 'Ravi']
(4, 7)
95
['python', 'typing']
```

## 5. Union Types

`A | B` means a value may have either type.

```python
def normalize_id(value: int | str) -> str:
    return str(value)


print(normalize_id(42))
print(normalize_id("A-42"))
```

Output:

```text
42
A-42
```

## 6. Optional Values

`T | None` means a value may be `None`. Narrow it before using it as `T`.

```python
def display_name(name: str | None) -> str:
    if name is None:
        return "anonymous"
    return name.upper()


print(display_name(None))
print(display_name("Ana"))
```

Output:

```text
anonymous
ANA
```

## 7. Abstract Collection Inputs

Annotate required behavior instead of demanding one concrete collection type.

```python
from collections.abc import Iterable, Mapping, Sequence


def total(values: Iterable[int]) -> int:
    return sum(values)


def first(values: Sequence[str]) -> str:
    return values[0]


def role(profile: Mapping[str, str]) -> str:
    return profile["role"]


print(total({1, 2, 3}))
print(first(("Ana", "Ravi")))
print(role({"role": "Developer"}))
```

Output:

```text
6
Ana
Developer
```

Use `list` or `dict` when mutation or concrete behavior is part of the contract.

## 8. Callable Types

`Callable[[ArgTypes], ReturnType]` describes callable behavior.

```python
from collections.abc import Callable


def apply(operation: Callable[[int], int], value: int) -> int:
    return operation(value)


def double(value: int) -> int:
    return value * 2


print(apply(double, 5))
```

Output:

```text
10
```

## 9. Type Aliases

A type alias gives a domain name to an existing type expression.

```python
from typing import TypeAlias

UserId: TypeAlias = int


def format_user(user_id: UserId) -> str:
    return f"user-{user_id}"


print(format_user(42))
```

Output:

```text
user-42
```

Python 3.12 also supports `type UserId = int`.

## 10. `Literal`

`Literal` limits a value to listed constants for static checking.

```python
from typing import Literal

Mode = Literal["read", "write"]


def describe(mode: Mode) -> str:
    return f"mode={mode}"


print(describe("read"))
```

Output:

```text
mode=read
```

Runtime code must still reject unsupported external values when required.

## 11. `Final`

`Final` tells static tools that a name should not be reassigned.

```python
from typing import Final

MAX_RETRIES: Final[int] = 3

print(MAX_RETRIES)
```

Output:

```text
3
```

It is not runtime enforcement.

## 12. `TypedDict`

`TypedDict` describes the expected keys and value types of dictionary-shaped data.

```python
from typing import TypedDict


class User(TypedDict):
    name: str
    active: bool


user: User = {"name": "Ana", "active": True}

print(type(user).__name__)
print(user["name"])
```

Output:

```text
dict
Ana
```

At runtime it is still a normal dictionary. Validate untrusted input before assigning this type.

## 13. Dataclasses

A dataclass creates a concrete runtime class and works well for simple domain data.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    name: str
    active: bool


user = User(name="Ana", active=True)

print(user.name)
print(user)
```

Output:

```text
Ana
User(name='Ana', active=True)
```

Annotations still do not validate constructor values automatically.

## 14. Protocols

A `Protocol` describes required behavior without requiring inheritance.

```python
from typing import Protocol


class Named(Protocol):
    @property
    def name(self) -> str:
        ...


class User:
    def __init__(self, name: str) -> None:
        self.name = name


def greet(value: Named) -> str:
    return f"Hello, {value.name}"


print(greet(User("Ana")))
```

Output:

```text
Hello, Ana
```

This is structural typing: compatibility depends on behavior, not a shared base class.

## 15. Generics

A type variable preserves a relationship between input and output types.

```python
from typing import TypeVar

T = TypeVar("T")


def first(values: list[T]) -> T:
    return values[0]


print(first([1, 2, 3]))
print(first(["A", "B"]))
```

Output:

```text
1
A
```

The return type matches the list's item type.

## 16. `Self`

`Self` describes a method that returns an instance of the current class or subclass.

```python
from typing import Self


class Counter:
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def increment(self) -> Self:
        self.value += 1
        return self


counter = Counter()
print(counter.increment() is counter)
print(counter.value)
```

Output:

```text
True
1
```

## 17. `Any` Versus `object`

`Any` disables most checking. `object` accepts any value but requires narrowing before specific operations.

```python
from typing import Any


def unchecked(value: Any) -> Any:
    return value


def safe_text(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return value.upper()


print(unchecked(10))
print(safe_text("python"))
```

Output:

```text
10
PYTHON
```

Prefer `object` at unknown boundaries when callers must prove the concrete type.

## 18. Runtime Validation

Validate external input before treating it as a typed domain value. Do not coerce unexpected types silently.

```python
def require_age(value: object) -> int:
    if type(value) is not int:
        raise TypeError("age must be an int")
    if value < 0:
        raise ValueError("age cannot be negative")
    return value


print(require_age(25))

try:
    require_age("25")
except TypeError as error:
    print(error)
```

Output:

```text
25
age must be an int
```

## 19. Static Analysis Workflow

Run static checks before tests and deployment.

```text
pyright
ruff check .
ruff format --check .
```

Static analysis can catch incompatible arguments, missing returns, unreachable code, and unsafe optional access without executing the program.

## 20. Final Mental Model

| Need | Tool |
| --- | --- |
| describe a function contract | parameter and return annotations |
| optional value | `T | None` |
| one of several types | union `A | B` |
| dictionary shape | `TypedDict` |
| concrete data object | dataclass |
| behavior-based contract | `Protocol` |
| preserve type relationships | generic type variable |
| unknown but checked later | `object` |
| deliberately disable checking | `Any` |

Remember:

- annotations describe intent;
- static tools check code without running it;
- hints do not validate runtime data;
- narrow unknown values before use;
- prefer precise, honest contracts over broad annotations.
