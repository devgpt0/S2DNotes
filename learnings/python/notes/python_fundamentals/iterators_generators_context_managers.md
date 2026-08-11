# PYTHON - ITERATORS, GENERATORS, AND CONTEXT MANAGERS

Iterators produce values one at a time. Context managers guarantee setup and cleanup.

## 1. Iterable Versus Iterator

An iterable can create an iterator. An iterator remembers traversal state and produces the next value.

```python
numbers = [10, 20]
iterator = iter(numbers)

print(iter(numbers) is numbers)
print(iter(iterator) is iterator)
```

Output:

```text
False
True
```

A list is iterable but not an iterator. An iterator returns itself from `iter()`.

## 2. `next()` and `StopIteration`

`next(iterator)` returns one item. Exhaustion raises `StopIteration`.

```python
iterator = iter([10, 20])

print(next(iterator))
print(next(iterator))

try:
    next(iterator)
except StopIteration as error:
    print(type(error).__name__)
```

Output:

```text
10
20
StopIteration
```

## 3. Iterators Are One-Pass

An exhausted iterator does not restart automatically.

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

Create a new iterator to traverse the iterable again.

## 4. How a `for` Loop Works

A `for` loop calls `iter()`, repeatedly calls `next()`, and stops on `StopIteration`.

```python
iterator = iter(["A", "B"])

while True:
    try:
        item = next(iterator)
    except StopIteration:
        break
    print(item)
```

Output:

```text
A
B
```

## 5. Custom Iterator

An iterator implements `__iter__()` and `__next__()`.

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


print(list(Countdown(3)))
```

Output:

```text
[3, 2, 1]
```

Use a generator when a custom iterator class would only store simple traversal state.

## 6. Generator Function

A function containing `yield` returns a generator iterator.

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1


generator = countdown(3)
print(type(generator).__name__)
print(list(generator))
```

Output:

```text
generator
[3, 2, 1]
```

## 7. Lazy Execution

Calling a generator function does not run its body. `next()` starts or resumes it.

```python
def values():
    print("started")
    yield 1
    print("resumed")
    yield 2


generator = values()
print("created")
print(next(generator))
print(next(generator))
```

Output:

```text
created
started
1
resumed
2
```

Local state is preserved between yields.

## 8. Generator `return`

`return` ends a generator. Its value becomes `StopIteration.value` during manual iteration.

```python
def one_value():
    yield 10
    return "finished"


generator = one_value()
print(next(generator))

try:
    next(generator)
except StopIteration as error:
    print(error.value)
```

Output:

```text
10
finished
```

## 9. `yield from`

`yield from iterable` delegates iteration to another iterable.

```python
def combined():
    yield from [1, 2]
    yield from [3, 4]


print(list(combined()))
```

Output:

```text
[1, 2, 3, 4]
```

## 10. Generator Expressions

A generator expression produces values lazily. A list comprehension builds the whole list immediately.

```python
generator = (number**2 for number in range(4))
values = [number**2 for number in range(4)]

print(type(generator).__name__)
print(next(generator))
print(values)
```

Output:

```text
generator
0
[0, 1, 4, 9]
```

Use a generator when one pass is enough and the full result need not be stored.

## 11. Lazy Pipelines

Generator expressions can process data stage by stage.

```python
numbers = range(1, 6)
even_numbers = (number for number in numbers if number % 2 == 0)
squares = (number**2 for number in even_numbers)

print(list(squares))
```

Output:

```text
[4, 16]
```

Each value flows through the pipeline only when requested.

## 12. Context Manager Protocol

A context manager implements `__enter__()` and `__exit__()`.

```python
class Session:
    def __enter__(self):
        print("open")
        return self

    def __exit__(self, exception_type, exception, traceback):
        print("close")
        return False


with Session() as session:
    print(type(session).__name__)
```

Output:

```text
open
Session
close
```

`__exit__()` runs even if the body raises.

## 13. Cleanup During an Exception

The context manager receives exception information during exit.

```python
class Session:
    def __enter__(self):
        print("open")
        return self

    def __exit__(self, exception_type, exception, traceback):
        print(exception_type.__name__ if exception_type else "none")
        print("close")
        return False


try:
    with Session():
        raise ValueError("invalid")
except ValueError:
    print("propagated")
```

Output:

```text
open
ValueError
close
propagated
```

Returning `False` allows the exception to propagate.

## 14. Exception Suppression

Returning `True` from `__exit__()` suppresses the exception.

```python
class IgnoreValueError:
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        return exception_type is ValueError


with IgnoreValueError():
    raise ValueError("ignored")

print("continued")
```

Output:

```text
continued
```

Suppress only errors the context manager explicitly knows how to handle.

## 15. `contextmanager` Decorator

`contextlib.contextmanager` builds a context manager around one `yield`.

```python
from contextlib import contextmanager


@contextmanager
def session():
    print("open")
    try:
        yield "resource"
    finally:
        print("close")


with session() as resource:
    print(resource)
```

Output:

```text
open
resource
close
```

Code before `yield` is setup. Code in `finally` is cleanup.

## 16. Multiple Context Managers

Managers enter left to right and exit right to left.

```python
from contextlib import contextmanager


@contextmanager
def managed(name):
    print("enter", name)
    try:
        yield
    finally:
        print("exit", name)


with managed("A"), managed("B"):
    print("body")
```

Output:

```text
enter A
enter B
body
exit B
exit A
```

## 17. Iterator Versus Generator Versus List

| Need | Choose |
| --- | --- |
| reusable stored values | list or tuple |
| one-pass lazy values | iterator |
| simple custom lazy logic | generator function |
| lazy expression | generator expression |
| deterministic resource cleanup | context manager |

## 18. Final Mental Model

Remember:

- iterable means it can produce an iterator;
- iterator means one-pass state plus `next()`;
- generator means an iterator whose frame pauses at `yield`;
- `for` handles `StopIteration`;
- `with` always calls exit logic after successful entry;
- lazy processing saves memory but does not make computation free.
