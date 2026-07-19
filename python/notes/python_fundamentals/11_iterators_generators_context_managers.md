# Iterators, Generators, and Context Managers - Beginner to Expert

These protocols power `for`, lazy pipelines, files, database cursors, `with`, and `async with`.

## 1. Iterable Versus Iterator

- An iterable can produce an iterator through `iter(value)`.
- An iterator produces one item at a time through `next(iterator)`.
- When finished, an iterator raises `StopIteration`.

```python
values = [10, 20]
iterator = iter(values)

print(next(iterator))
print(next(iterator))

try:
    next(iterator)
except StopIteration:
    print("finished")
```

Output:

```text
10
20
finished
```

## 2. What a `for` Loop Does

This loop:

```python
for value in [10, 20]:
    print(value)
```

Conceptually behaves like:

```python
iterator = iter([10, 20])

while True:
    try:
        value = next(iterator)
    except StopIteration:
        break
    print(value)
```

Output for both:

```text
10
20
```

Application code normally uses `for`; the expanded form explains the protocol.

## 3. Iterators Are Usually One-Pass

```python
iterator = iter([1, 2, 3])

print(list(iterator))
print(list(iterator))
```

Output:

```text
[1, 2, 3]
[]
```

Document whether an API accepts an iterable once or requires a reusable collection.

## 4. Build a Custom Iterator

```python
from collections.abc import Iterator


class Countdown(Iterator[int]):
    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("start must be non-negative")
        self._current = start

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self._current == 0:
            raise StopIteration

        value = self._current
        self._current -= 1
        return value


print(list(Countdown(3)))
```

Output:

```text
[3, 2, 1]
```

An iterator returns itself from `__iter__` because it owns one progressing cursor.

## 5. Build a Reusable Iterable

```python
from collections.abc import Iterator


class CountdownRange:
    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("start must be non-negative")
        self._start = start

    def __iter__(self) -> Iterator[int]:
        return iter(range(self._start, 0, -1))


countdown = CountdownRange(3)
print(list(countdown))
print(list(countdown))
```

Output:

```text
[3, 2, 1]
[3, 2, 1]
```

The iterable creates a fresh iterator for each traversal.

## 6. Generator Functions

A function containing `yield` creates a generator object when called. Its body starts on the first iteration.

```python
from collections.abc import Iterator


def countdown(start: int) -> Iterator[int]:
    if start < 0:
        raise ValueError("start must be non-negative")

    current = start
    while current > 0:
        yield current
        current -= 1


generator = countdown(3)
print(type(generator).__name__)
print(list(generator))
```

Output:

```text
generator
[3, 2, 1]
```

## 7. Generator State Is Suspended

```python
from collections.abc import Iterator


def lessons() -> Iterator[str]:
    print("start")
    yield "iterators"
    print("resume")
    yield "generators"


iterator = lessons()
print("created")
print(next(iterator))
print(next(iterator))
```

Output:

```text
created
start
iterators
resume
generators
```

The generator preserves its instruction position and local variables between yields.

## 8. Return Value from a Generator

`return value` ends a generator and attaches the value to `StopIteration.value`.

```python
from collections.abc import Generator


def one_lesson() -> Generator[str, None, int]:
    yield "python"
    return 1


iterator = one_lesson()
print(next(iterator))

try:
    next(iterator)
except StopIteration as stopped:
    print(stopped.value)
```

Output:

```text
python
1
```

The three `Generator` type arguments are yielded type, sent type, and returned type.

## 9. `yield from`

```python
from collections.abc import Iterable, Iterator


def flatten(groups: Iterable[Iterable[str]]) -> Iterator[str]:
    for group in groups:
        yield from group


print(list(flatten([["python", "go"], ["rust"]])))
```

Output:

```text
['python', 'go', 'rust']
```

`yield from` delegates iteration and also forwards generator `send`, `throw`, and return behavior. Use it when delegation semantics are intended, not only to save one line.

## 10. Generator Expressions

```python
squares = (value * value for value in range(5))
print(sum(squares))
```

Output:

```text
30
```

Generator expressions are lazy. List comprehensions materialize their complete result.

Use a generator when:

- one pass is sufficient;
- input can be large or unbounded;
- values can be produced incrementally;
- the consumer can process incrementally.

Use a collection when repeated traversal, indexing, length, or a stable snapshot is required.

## 11. `send`

`send` resumes a generator and makes a value become the result of the paused `yield` expression.

```python
from collections.abc import Generator


def running_total() -> Generator[int, int, None]:
    total = 0
    while True:
        value = yield total
        total += value


totals = running_total()
print(next(totals))
print(totals.send(5))
print(totals.send(7))
totals.close()
```

Output:

```text
0
5
12
```

The first advancement must use `next` or `send(None)` because no `yield` is paused yet. For ordinary data flow, a class with an explicit method is often clearer than a generator coroutine.

## 12. `throw` and `close`

- `throw(error)` raises an exception at the paused `yield`;
- `close()` raises `GeneratorExit` at the paused `yield`;
- `finally` runs during normal exhaustion, close, or an exception.

```python
from collections.abc import Iterator


def resource_stream() -> Iterator[int]:
    print("open")
    try:
        yield 1
        yield 2
    finally:
        print("close")


stream = resource_stream()
print(next(stream))
stream.close()
```

Output:

```text
open
1
close
```

Do not rely on garbage collection to close a partially consumed generator. Close it explicitly or place ownership in a context manager.

## 13. Lazy Pipelines and Exceptions

```python
from collections.abc import Iterable, Iterator


def parse_numbers(values: Iterable[str]) -> Iterator[int]:
    for value in values:
        yield int(value)


numbers = parse_numbers(["10", "invalid"])
print(next(numbers))

try:
    next(numbers)
except ValueError as error:
    print(type(error).__name__)
```

Output:

```text
10
ValueError
```

The error appears during consumption, not when the generator is created. Document lazy failure timing.

## 14. Iterator Invalidation

Changing a container while iterating can skip items, repeat work, or raise an error depending on the container and operation.

Prefer:

- building a new result;
- iterating over an intentional snapshot;
- collecting changes and applying them afterward.

Do not copy a massive collection casually; choose the mutation contract based on memory and consistency requirements.

## 15. Context Manager Protocol

A context manager defines setup and guaranteed exit behavior.

```python
from types import TracebackType


class Lesson:
    def __enter__(self) -> "Lesson":
        print("enter")
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        print(f"exit: {exception_type is None}")
        return False


with Lesson():
    print("body")
```

Output:

```text
enter
body
exit: True
```

Returning `False` lets an exception propagate. Returning `True` suppresses it. Suppress only exceptions the context manager can genuinely handle.

## 16. Function-Based Context Manager

```python
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer(label: str) -> Iterator[None]:
    started = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - started
        print(f"{label}: {elapsed >= 0}")


with timer("lesson"):
    total = sum(range(100))
    print(total)
```

Output:

```text
4950
lesson: True
```

Exactly one `yield` divides setup from cleanup. The `finally` block guarantees cleanup.

## 17. `closing` and `nullcontext`

- `contextlib.closing(value)` calls `value.close()` when the block ends;
- `nullcontext(value)` provides an optional no-op context manager.

Prefer an object's native context-manager support when available because it may define richer commit, rollback, or error behavior than `close` alone.

## 18. `ExitStack` for Dynamic Resources

```python
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    paths = [Path(directory, "a.txt"), Path(directory, "b.txt")]
    for path in paths:
        path.write_text(path.stem, encoding="utf-8")

    with ExitStack() as stack:
        streams = [
            stack.enter_context(path.open(encoding="utf-8"))
            for path in paths
        ]
        print([stream.read() for stream in streams])
```

Output:

```text
['a', 'b']
```

`ExitStack` closes acquired resources in reverse order, including when later acquisition fails.

## 19. Async Iterators

An async iterator's next operation can await I/O.

```python
import asyncio
from collections.abc import AsyncIterator


async def lessons() -> AsyncIterator[str]:
    for name in ["asyncio", "typing"]:
        await asyncio.sleep(0)
        yield name


async def main() -> None:
    async for name in lessons():
        print(name)


asyncio.run(main())
```

Output:

```text
asyncio
typing
```

Async iteration is for asynchronous production of values, not merely for ordinary in-memory lists.

## 20. Async Context Managers

```python
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


@asynccontextmanager
async def connection() -> AsyncIterator[str]:
    print("connect")
    try:
        yield "database"
    finally:
        await asyncio.sleep(0)
        print("disconnect")


async def main() -> None:
    async with connection() as name:
        print(name)


asyncio.run(main())
```

Output:

```text
connect
database
disconnect
```

Cancellation can arrive during cleanup. Critical async cleanup may need a deliberate bounded shutdown strategy based on the resource library's contract.

## 21. Type Contracts

Use the narrowest accurate protocol:

- `Iterable[T]`: caller can loop once;
- `Iterator[T]`: caller receives a stateful cursor;
- `Sequence[T]`: caller needs ordered reusable access and length/indexing;
- `Generator[YieldT, SendT, ReturnT]`: send/return types matter;
- `ContextManager[T]`: synchronous `with` value;
- `AsyncIterator[T]` and `AsyncContextManager[T]`: asynchronous protocols.

## 22. Production Review Checklist

- Is this value reusable or one-pass?
- When does work and failure occur: creation or consumption?
- Who closes a partially consumed generator?
- Can the pipeline grow memory through buffering or `list()`?
- Are side effects predictable under partial consumption?
- Does context-manager exit suppress anything?
- Are multiple resources released after partial acquisition failure?
- Is async cleanup safe under cancellation and bounded by a deadline?

## Final Rules

- distinguish iterable from iterator;
- use generators for incremental one-pass production;
- document lazy side effects and failure timing;
- do not retain or materialize unbounded streams;
- close partially consumed resource-owning generators;
- use context managers for deterministic cleanup;
- use `ExitStack` for a dynamic number of resources;
- use async protocols only for truly asynchronous lifecycle work.

