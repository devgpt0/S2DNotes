# Type Hints, Ruff, and mypy - Beginner to Expert

Python remains dynamically executed. Type hints let static tools check contracts before runtime; Ruff checks style and many correctness problems.

## 1. First Typed Function

```python
def total(price: int, quantity: int) -> int:
    return price * quantity


print(total(21, 2))
```

Output:

```text
42
```

Python does not automatically reject `total("21", 2)` from annotations alone. Validate untrusted runtime input before it enters typed application code.

## 2. Boundary Strategy

```text
untrusted bytes/dict/JSON
    -> strict runtime parse and validation
    -> typed domain values
    -> statically checked application logic
```

Static typing and runtime validation solve different problems.

## 3. Variable and Collection Types

```python
course_id: str = "python"
levels: list[int] = [1, 2, 3]
titles: dict[str, str] = {"python": "Python"}
coordinates: tuple[int, int] = (10, 20)
```

Modern built-in generics are available in supported Python 3.12+ code.

## 4. Use Abstract Read-Only Inputs

```python
from collections.abc import Iterable, Mapping


def calculate_total(
    values: Iterable[int],
    weights: Mapping[str, int],
) -> int:
    return sum(values) + weights.get("bonus", 0)


print(calculate_total([10, 20], {"bonus": 12}))
```

Output:

```text
42
```

Accept `Sequence`, `Mapping`, or `Iterable` when only that behavior is required. Return concrete types when the caller owns a concrete result.

## 5. Union and Optional Values

```python
def display_name(name: str | None) -> str:
    if name is None:
        return "anonymous"
    return name


print(display_name(None))
print(display_name("Ada"))
```

Output:

```text
anonymous
Ada
```

`str | None` means exactly either a string or `None`. It does not mean the parameter can be omitted; a default value controls omission.

## 6. Narrow a Union

```python
def double(value: int | str) -> int:
    if isinstance(value, int):
        return value * 2
    return len(value) * 2


print(double(10))
print(double("go"))
```

Output:

```text
20
4
```

The `isinstance` branch narrows the union. Avoid assertions or casts that merely silence the checker without proving the runtime condition.

## 7. `object` Versus `Any`

- `object` accepts every Python object, but operations require narrowing.
- `Any` disables type checking for operations flowing through that value.

```python
def safe_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return repr(value)
```

Use `object` for an unknown value that must be inspected safely. Restrict `Any` to genuinely dynamic boundaries and convert it quickly into validated typed data.

## 8. Type Aliases and `NewType`

```python
from typing import NewType, TypeAlias

CourseId = NewType("CourseId", str)
ScoreMap: TypeAlias = dict[CourseId, int]


def score_for(scores: ScoreMap, course_id: CourseId) -> int:
    return scores[course_id]


python_id = CourseId("python")
print(score_for({python_id: 42}, python_id))
```

Output:

```text
42
```

A type alias gives a complex type a name. `NewType` creates a static distinction while remaining its underlying runtime value; it does not validate content.

## 9. Dataclasses for Domain Values

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Course:
    course_id: str
    title: str

    def __post_init__(self) -> None:
        if not self.course_id:
            raise ValueError("course_id must not be empty")
        if not self.title:
            raise ValueError("title must not be empty")


course = Course(course_id="python", title="Python")
print(course.title)
```

Output:

```text
Python
```

Annotations describe fields; `__post_init__` enforces runtime invariants. Do not normalize invalid external data silently.

## 10. `TypedDict` for Dict-Shaped Data

```python
from typing import TypedDict


class CoursePayload(TypedDict):
    course_id: str
    title: str


def display(payload: CoursePayload) -> str:
    return f"{payload['course_id']}: {payload['title']}"


print(display({"course_id": "python", "title": "Python"}))
```

Output:

```text
python: Python
```

`TypedDict` has no runtime validation. It is useful after a runtime parser has confirmed keys and values.

Optional keys:

```python
from typing import NotRequired, TypedDict


class CoursePatch(TypedDict):
    title: NotRequired[str]
```

An absent key differs from a present key whose value is `None`.

## 11. Structural Interfaces with `Protocol`

```python
from typing import Protocol


class CourseReader(Protocol):
    def find_title(self, course_id: str) -> str | None: ...


class MemoryCourses:
    def __init__(self) -> None:
        self._titles = {"python": "Python"}

    def find_title(self, course_id: str) -> str | None:
        return self._titles.get(course_id)


def print_title(reader: CourseReader, course_id: str) -> None:
    print(reader.find_title(course_id))


print_title(MemoryCourses(), "python")
```

Output:

```text
Python
```

`MemoryCourses` does not inherit from the protocol. Matching structure is enough for static checking.

Use `@runtime_checkable` only when limited runtime `isinstance` checks are required; it does not validate complete signatures at runtime.

## 12. Generic Functions

Python 3.12 type-parameter syntax:

```python
def first[T](values: list[T]) -> T:
    if not values:
        raise ValueError("values must not be empty")
    return values[0]


print(first([42, 43]))
print(first(["python", "rust"]))
```

Output:

```text
42
python
```

For libraries supporting older Python versions, use `TypeVar` syntax according to the declared minimum version.

## 13. Bounded Type Parameters

```python
from typing import Protocol


class SupportsLessThan(Protocol):
    def __lt__(self, other: "SupportsLessThan", /) -> bool: ...


def smaller[T: SupportsLessThan](left: T, right: T) -> T:
    return left if left < right else right
```

In real code, choose bounds that match actual supported operations. Overly clever generic constraints can be harder to maintain than a small concrete function.

## 14. Generic Classes

```python
class Box[T]:
    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value


box = Box(42)
print(box.get())
```

Output:

```text
42
```

## 15. Variance in Simple Words

Variance asks whether `Container[Child]` can be used where `Container[Parent]` is expected.

- immutable/read-only producers can often be covariant;
- consumers can sometimes be contravariant;
- mutable containers are usually invariant because they both accept and return values.

Do not change variance to silence an error. First verify that every operation remains type-safe.

## 16. Callable Types

```python
from collections.abc import Callable


def apply(value: int, operation: Callable[[int], int]) -> int:
    return operation(value)


print(apply(21, lambda value: value * 2))
```

Output:

```text
42
```

Use a `Protocol` with `__call__` when named parameters, overloads, or attributes form part of the callable contract.

## 17. Preserve Decorator Signatures with `ParamSpec`

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def traced(function: Callable[P, R]) -> Callable[P, R]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"calling {function.__name__}")
        return function(*args, **kwargs)

    return wrapper


@traced
def total(price: int, quantity: int) -> int:
    return price * quantity


print(total(21, 2))
```

Output:

```text
calling total
42
```

`ParamSpec` preserves the wrapped parameter list; the result type remains `R`.

## 18. `Self`

```python
from typing import Self


class Query:
    def __init__(self) -> None:
        self._limit: int | None = None

    def limit(self, value: int) -> Self:
        if value <= 0:
            raise ValueError("limit must be positive")
        self._limit = value
        return self


query = Query().limit(10)
print(type(query).__name__)
```

Output:

```text
Query
```

`Self` preserves subclass return types for fluent or alternate-constructor APIs.

## 19. Overloads

```python
from typing import Literal, overload


@overload
def parse(raw: str, *, many: Literal[True]) -> list[str]: ...


@overload
def parse(raw: str, *, many: Literal[False] | None = None) -> str: ...


def parse(raw: str, *, many: bool | None = None) -> str | list[str]:
    if many is True:
        return raw.split(",")
    return raw
```

Overloads describe caller-visible relationships. The final implementation performs runtime logic. Keep overload sets small and test every branch.

## 20. Exhaustive Enum Matching

```python
from enum import Enum
from typing import assert_never


class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


def label(status: Status) -> str:
    match status:
        case Status.DRAFT:
            return "Draft"
        case Status.PUBLISHED:
            return "Published"
        case _ as unreachable:
            assert_never(unreachable)
```

Adding a new enum member causes a strict type checker to identify the unhandled path.

## 21. Type Guards

```python
from typing import TypeGuard


def is_string_list(values: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(value, str) for value in values)


values: list[object] = ["python", "typing"]
if is_string_list(values):
    print(",".join(values))
```

Output:

```text
python,typing
```

A type guard is a promise made by its implementation. An incorrect guard makes static reasoning unsound.

## 22. mypy Configuration

Place configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true
show_error_codes = true
pretty = true
files = ["src", "tests"]
```

Run:

```powershell
python -m mypy
```

Strict mode includes checks for untyped definitions, `Any` leakage, optional values, and more. Add narrow per-module exceptions only for a demonstrated integration constraint, with ownership and a removal plan.

Do not use blanket `ignore_errors`, broad `# type: ignore`, or casts to hide real mismatches.

## 23. Ruff Configuration

```toml
[tool.ruff]
target-version = "py312"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = [
  "E",
  "F",
  "I",
  "UP",
  "B",
  "SIM",
  "RUF",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Run:

```powershell
python -m ruff check .
python -m ruff format --check .
```

Fix findings in code. Avoid broad rule suppression. Review automatic fixes before committing them.

## 24. Tool Responsibilities

| Tool | Main responsibility |
|---|---|
| Ruff formatter | deterministic source formatting |
| Ruff linter | imports, bugs, modernization, style, selected security-adjacent checks |
| mypy | static type consistency |
| pytest | runtime behavior |
| Bandit | common Python security patterns |
| runtime validation | untrusted external values and domain invariants |

No one tool replaces the others.

## 25. CI Commands

```powershell
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
python -m bandit -r src
```

Pin tool versions through the repository's dependency policy so developers and CI use consistent rules.

## 26. Common Mistakes

- using `Any` where `object` plus narrowing is safer;
- annotating an invalid runtime value without validating it;
- using `cast` as runtime conversion;
- confusing an optional key with a nullable value;
- exposing mutable concrete collections unnecessarily;
- losing a decorator's signature;
- adding ignores instead of fixing a contract;
- running mypy on only a few files so imports become untyped `Any`;
- enabling hundreds of lint rules without agreeing on the intended code policy.

## Final Rules

- validate external data at runtime;
- type public and architectural boundaries completely;
- minimize `Any` and narrow unknown `object` values;
- use protocols for behavior and concrete return types for owned results;
- preserve decorator signatures;
- use strict mypy and a deliberate Ruff rule set;
- fix errors instead of suppressing them;
- keep formatting, linting, typing, security checks, and tests as separate CI gates.
