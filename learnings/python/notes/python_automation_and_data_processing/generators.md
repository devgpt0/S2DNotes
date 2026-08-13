# Generators

## 1. Core truth

A generator is a lazy way to produce values one at a time.
It is often simpler than a custom iterator class.

```python
def numbers():
    yield 1
    yield 2

print(list(numbers()))
```

Output:

```text
[1, 2]
```

Each `yield` sends one value to the caller, and the generator resumes later from the same place.

## 2. Generator foundations

### `yield` pauses and resumes

```python
def count():
    yield 1
    yield 2

g = count()
print(next(g))
print(next(g))
```

Output:

```text
1
2
```

### Generators are one-pass

```python
def count():
    yield 1

g = count()
print(list(g))
print(list(g))
```

Output:

```text
[1]
[]
```

### Generators can simplify pipelines

```python
def doubled(values):
    for value in values:
        yield value * 2

print(list(doubled([1, 2, 3])))
```

Output:

```text
[2, 4, 6]
```

## 3. Generator operations

- `yield` creates lazy output.
- `yield from` delegates to another iterator or generator.
- `next()` drives generator progress.

```python
def values():
    yield from [1, 2, 3]

print(list(values()))
```

Output:

```text
[1, 2, 3]
```

## 4. Practical generator pipelines

### Example 1: Simple generator

```python
def letters():
    yield "a"
    yield "b"

print(list(letters()))
```

Output:

```text
['a', 'b']
```

### Example 2: Filter data lazily

```python
def evens(values):
    for value in values:
        if value % 2 == 0:
            yield value

print(list(evens([1, 2, 3, 4])))
```

Output:

```text
[2, 4]
```

### Example 3: Chain generators

```python
def one():
    yield 1

def two():
    yield from one()
    yield 2

print(list(two()))
```

Output:

```text
[1, 2]
```

- stream lines from files;
- produce filtered or transformed values;
- build memory-friendly processing pipelines;
- stop early when only part of the data is needed.

## 5. Generator mistakes

### Mistake 1: Forgetting that generators are exhausted

### Mistake 2: Returning a list when a generator would be cleaner

### Mistake 3: Mixing side effects and yielding without a clear order

## 6. Lazy-processing decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Reusable data | list | can be reused |
| Lazy one-pass values | generator | memory-friendly |
| Custom iteration state | generator often simpler | less boilerplate |

## 7. Performance and safety

- generators are efficient for large inputs;
- they are one-pass and must be recreated for reuse;
- keep generator bodies small and readable.

## 8. Advanced generator behavior

- generator expressions;
- generator delegation with `yield from`;
- interaction with `send`, `throw`, and `close` in advanced code.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| `yield` | pause and return one value |
| Generator | lazy value producer |
| `yield from` | delegate to another iterator |
| Exhaustion | one-pass behavior |

## 10. Delegation and return values

`yield from` forwards values and captures the delegated generator's return value.

```python
def child():
    yield 1
    yield 2
    return "complete"


def parent():
    result = yield from child()
    yield result


print(list(parent()))
```

Output:

```text
[1, 2, 'complete']
```

Inside a generator, `return value` becomes `StopIteration.value`. A `for` loop
consumes that exception and ignores the value.

## 11. Cleanup and early termination

Closing a generator raises `GeneratorExit` at its suspension point. Put owned
resource cleanup in `finally` or, preferably, open resources in a surrounding
context manager with an obvious owner.

```python
def values():
    try:
        yield 1
        yield 2
    finally:
        print("closed")


iterator = values()
print(next(iterator))
iterator.close()
```

Output:

```text
1
closed
```

Do not yield after receiving `GeneratorExit`. Unhandled `StopIteration` raised
inside generator code becomes `RuntimeError`; use `return` to end normally.

## 12. Pipeline ownership

- Keep generators single-purpose and free of hidden writes when possible.
- Document whether partial consumption is allowed.
- Bound upstream reads; laziness does not protect against an infinite downstream
  consumer or unbounded buffering in another tool.
- Prefer ordinary arguments over `send()` unless bidirectional coroutine behavior
  is genuinely required.
