# `collections.abc` and Typing
## 1. Core truth

`collections.abc` gives you abstract base classes that describe what a value can do.
They help you say "I need something mapping-like" instead of "I need exactly a `dict`."

```python
from collections.abc import Iterable, Mapping

def summarize(config: Mapping[str, int], values: Iterable[int]) -> int:
    return config.get("base", 0) + sum(values)

print(summarize({"base": 10}, [1, 2, 3]))
```

Output:

```text
16
```

The function reads a value from the mapping and adds it to the sum of the iterable.

## 2. Collection contracts

### `Iterable` means "can be looped over"

```python
from collections.abc import Iterable

def total(values: Iterable[int]) -> int:
    return sum(values)

print(total([1, 2, 3]))
```

Output:

```text
6
```

Practical takeaway: use `Iterable` when you only need to loop through values once.

### `Sequence` means "ordered and indexable"

```python
from collections.abc import Sequence

def first_and_last(items: Sequence[str]) -> tuple[str, str]:
    return items[0], items[-1]

print(first_and_last(("a", "b", "c")))
print(first_and_last(["x", "y"]))
```

Output:

```text
('a', 'c')
('x', 'y')
```

Practical takeaway: use `Sequence` when you need indexing, length, or slicing.

### `Mapping` means "dictionary-like read access"

```python
from collections.abc import Mapping

def summarize(config: Mapping[str, int]) -> int:
    return config.get("base", 0) + config.get("bonus", 0)

print(summarize({"base": 10, "bonus": 4}))
```

Output:

```text
14
```

Practical takeaway: use `Mapping` when you only need to read keys and values.

## 3. Runtime and typing contracts

### Runtime validation with `isinstance()`

```python
from collections.abc import Mapping

def load_settings(obj: object) -> dict[str, int]:
    if not isinstance(obj, Mapping):
        raise TypeError("Expected mapping-like input")
    return dict(obj)

print(load_settings({"a": 1, "b": 2}))
```

Output:

```text
{'a': 1, 'b': 2}
```

### Typed inversion with a mapping contract

```python
from collections.abc import Mapping

def invert_unique(data: Mapping[str, int]) -> dict[int, str]:
    result: dict[int, str] = {}
    for key, value in data.items():
        if value in result:
            raise ValueError("values must be unique")
        result[value] = key
    return result

print(invert_unique({"a": 1, "b": 2}))
```

Output:

```text
{1: 'a', 2: 'b'}
```

### `MutableMapping` when writes are required

Use `MutableMapping` only when the function needs to change the mapping.

## 4. Practical use

### Example 1: Read from any mapping-like object

```python
from collections.abc import Mapping

def get_timeout(config: Mapping[str, int]) -> int:
    return config.get("timeout", 30)

print(get_timeout({"timeout": 60}))
```

Output:

```text
60
```

### Example 2: Sum anything iterable

```python
from collections.abc import Iterable

def total(values: Iterable[int]) -> int:
    return sum(values)

print(total((2, 3, 5)))
```

Output:

```text
10
```

### Example 3: Use a sequence when indexing matters

```python
from collections.abc import Sequence

def middle(items: Sequence[str]) -> str:
    return items[len(items) // 2]

print(middle(["a", "b", "c"]))
```

Output:

```text
b
```

- Type read-only config as `Mapping`.
- Type a list of values that may be a tuple or list as `Sequence`.
- Type one-pass inputs such as generator pipelines as `Iterable`.
- Use `MutableMapping` for APIs that edit dictionaries in place.
- Use `Protocol` when you want structural compatibility without inheritance.

## 5. Contract mistakes

### Mistake 1: Requiring `dict` when `Mapping` is enough

If your function only reads keys and values, do not force callers to pass exactly a `dict`.

### Mistake 2: Using `Iterable` when you need indexing

An `Iterable` can be looped over, but it does not promise `items[0]` or slicing.

### Mistake 3: Using the wrong mutability contract

If the function writes to the object, type it as `MutableMapping`, not `Mapping`.

### Mistake 4: Confusing runtime checks with static typing

Type hints help tools and readers, but they do not enforce behavior by themselves.
Use `isinstance()` if you need a runtime check.

## 6. Contract decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Loop through values once | `Iterable` | Broad and flexible | You need indexing |
| Index by position | `Sequence` | Read-only ordered access | You need mutation-only operations |
| Read key/value pairs | `Mapping` | Narrow and clear | You must write to keys |
| Update keys and values | `MutableMapping` | Reflects write behavior | You only need read access |
| Behavior-based structural typing | `Protocol` | Flexible without inheritance | You need an ABC runtime check |

Selection rule:

- Choose the narrowest type that matches the behavior.
- Do not use a concrete type unless the concrete type itself matters.

## 7. Performance and maintainability

- Narrower contracts make APIs easier to understand.
- `Iterable` is the broadest choice, but it gives the least information.
- `Sequence` is better when callers need position-based behavior.
- `Mapping` is better when callers only need lookup behavior.
- Runtime ABC checks are useful at boundaries, especially when input comes from outside your code.

Best practices:

- Keep input contracts as small as possible.
- Convert to a concrete type only when you truly need one.
- Do not overstate the guarantees your function actually needs.

## 8. Protocols and ABCs

### `Protocol` versus `ABC`

`ABC` is useful when you want a known interface and runtime checks.
`Protocol` is useful when you want structural typing, meaning any object with the right methods can satisfy the contract.

This is especially useful for collection-like APIs that should accept more than one concrete class.

## 9. Mental model

| Contract | What it means | Best use |
| --- | --- | --- |
| `Iterable` | You can loop over it | One-pass traversal |
| `Sequence` | Ordered and indexable | Position-based access |
| `Mapping` | Dictionary-like read access | Lookup-only APIs |
| `MutableMapping` | Dictionary-like write access | In-place updates |
| `Protocol` | Behavior-based typing | Flexible structural contracts |

## 10. Iterator contracts and runtime protocols

Use `Iterator[T]` only when the caller may consume one-pass state with `next()`.
Use `Iterable[T]` when a normal loop is sufficient.

```python
from collections.abc import Iterable, Iterator

values = [1, 2, 3]
iterator = iter(values)
print(isinstance(values, Iterable))
print(isinstance(values, Iterator))
print(isinstance(iterator, Iterator))
```

Output:

```text
True
False
True
```

`@runtime_checkable` permits shallow `isinstance()` checks for a `Protocol`.
It checks attribute presence, not type signatures or semantic correctness.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closer(Protocol):
    def close(self) -> None: ...


class Resource:
    def close(self) -> None:
        pass


print(isinstance(Resource(), Closer))
```

Output:

```text
True
```
