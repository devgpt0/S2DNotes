# Dunder Methods and Object Lifecycle
## 1. Core truth

Dunder methods are special methods with names like `__repr__` and `__len__`.
They let your objects behave naturally in Python syntax.

```python
class Course:
    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Course(title={self.title!r})"

course = Course("Python")
print(course)
print(repr(course))
```

Output:

```text
Course(title='Python')
Course(title='Python')
```

When `__str__` is not defined, `print()` falls back to `__repr__`.

## 2. Object protocol foundations

### `__repr__` should be precise

```python
class Course:
    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Course(title={self.title!r})"

course = Course("Python")
print(course)
print(repr(course))
```

Output:

```text
Course(title='Python')
Course(title='Python')
```

Practical takeaway: make `__repr__` useful for debugging and logging.

### `__str__` should be readable for humans

```python
class Course:
    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Course(title={self.title!r})"

    def __str__(self) -> str:
        return f"Course: {self.title}"

course = Course("Python")
print(course)
print(str(course))
```

Output:

```text
Course: Python
Course: Python
```

Practical takeaway: use `__str__` for user-facing output and `__repr__` for debugging output.

### `__eq__` and `__hash__` must agree

```python
class User:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)

users = {User(1), User(1)}
print(len(users))
```

Output:

```text
1
```

Practical takeaway: if two objects compare equal, they must also hash the same when they are hashable.

### `__call__` turns an object into a callable

```python
class Discount:
    def __init__(self, rate: float) -> None:
        self.rate = rate

    def __call__(self, amount: float) -> float:
        return amount * (1 - self.rate)

discount = Discount(0.1)
print(discount(100.0))
```

Output:

```text
90.0
```

Practical takeaway: use `__call__` when an object behaves like a configurable function.

## 3. Object protocol methods

### Printing methods

- `__repr__` for debugging
- `__str__` for human-friendly display

### Comparison methods

- `__eq__` for equality
- `__lt__`, `__le__`, `__gt__`, `__ge__` for meaningful ordering

### Container methods

- `__len__`
- `__iter__`
- `__contains__`
- `__getitem__`

### Callable and context-manager methods

- `__call__`
- `__enter__`
- `__exit__`

### Lifecycle methods

- `__new__`
- `__init__`

### Memory-related method

- `__slots__`

```python
class Bag:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, item: str) -> bool:
        return item in self.items

bag = Bag(["apple", "banana"])
print(len(bag))
print("apple" in bag)
```

Output:

```text
2
True
```

## 4. Practical protocol implementations

### Example 1: Better object printing

```python
class Course:
    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Course(title={self.title!r})"

print(Course("Python"))
```

Output:

```text
Course(title='Python')
```

### Example 2: Container-like class

```python
class Bag:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, item: str) -> bool:
        return item in self.items

bag = Bag(["apple", "banana"])
print(len(bag))
print("banana" in bag)
```

Output:

```text
2
True
```

### Example 3: Context manager

```python
class TraceBlock:
    def __enter__(self) -> "TraceBlock":
        print("enter")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        print("exit")

with TraceBlock():
    print("inside")
```

Output:

```text
enter
inside
exit
```

- Use `__repr__` to make debugging easier.
- Use `__str__` for readable user-facing output.
- Use `__call__` for configurable policies, validators, or command-style objects.
- Use `__enter__` and `__exit__` for deterministic resource handling.
- Use `__slots__` when memory and attribute discipline matter.

## 5. Protocol mistakes

### Mistake 1: Making `__repr__` vague

The debug representation should help you identify the object quickly.

### Mistake 2: Putting mutable fields into hash logic

If a hashed object changes after it is placed in a set or dict, lookups can break.

### Mistake 3: Defining ordering without a real domain order

Use explicit `key=` functions when the order is just for presentation.

### Mistake 4: Assuming `__slots__` is always better

It reduces flexibility, so use it only when the tradeoff is worth it.

## 6. Protocol decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Debug output | `__repr__` | precise and unambiguous | you want human prose |
| Human display | `__str__` | readable for users | you need exact reconstruction |
| Equality | `__eq__` | compares meaningful state | identity alone should decide |
| Hashing | `__hash__` | works in sets and dicts | the object changes often |
| Callable behavior | `__call__` | stateful function-like object | a plain function is enough |
| Resource cleanup | `__enter__` / `__exit__` | deterministic lifecycle | no cleanup is needed |
| Lean instances | `__slots__` | fewer accidental attrs | you need dynamic attributes |

Selection rule:

- Use only the dunder methods that match the domain behavior.
- Prefer explicit `key=` sorting over custom ordering when possible.

## 7. Safety and maintainability

- Keep dunder methods small and deterministic.
- Make hashable objects effectively immutable.
- Avoid surprising side effects in printing or comparison methods.
- Use `__slots__` only after you know the tradeoff helps.

Best practices:

- Make `__repr__` developer-friendly.
- Make `__str__` human-friendly.
- Make special methods consistent with each other.

## 8. Advanced lifecycle behavior

### `__new__` versus `__init__`

- `__new__` creates the instance.
- `__init__` initializes the instance.

### `__slots__`

`__slots__` prevents accidental attribute creation and can reduce memory usage.

```python
class LockedCourse:
    __slots__ = ("title",)

    def __init__(self, title: str) -> None:
        self.title = title

course = LockedCourse("Python")
print(hasattr(course, "__dict__"))
```

Output:

```text
False
```

## 9. Mental model

| Hook | Remember |
| --- | --- |
| `__repr__` | debug-friendly |
| `__str__` | user-friendly |
| `__eq__` / `__hash__` | stay consistent |
| `__call__` | object behaves like a function |
| `__enter__` / `__exit__` | context management |
| `__new__` / `__init__` | create then initialize |
| `__slots__` | leaner instances, less flexibility |

## 10. Binary operations should return `NotImplemented`

When an operand type is unsupported, return `NotImplemented` so Python can try
the reflected operation. Raising immediately prevents that protocol.

```python
class Distance:
    def __init__(self, meters: int) -> None:
        self.meters = meters

    def __add__(self, other: object):
        if not isinstance(other, Distance):
            return NotImplemented
        return Distance(self.meters + other.meters)


print((Distance(2) + Distance(3)).meters)
```

Output:

```text
5
```

Equality and hashing form one contract: equal objects must have equal hashes.
Defining mutable value-based equality normally means instances must remain
unhashable.

## 11. Avoid `__del__` for resource ownership

Finalizer timing and interpreter-shutdown state are not reliable application
control flow. Reference cycles and implementation differences can delay cleanup,
and exceptions from `__del__` cannot be handled normally.

Use context managers for deterministic cleanup. Use `weakref.finalize()` only as
a fallback for resources whose owner cannot expose an explicit close operation.
