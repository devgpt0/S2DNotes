# Iterators

## 1. Core truth

An iterator is an object that returns values one at a time.
It is useful when you want to process data step by step instead of all at once.

```python
items = iter(["a", "b"])
print(next(items))
print(next(items))
```

Output:

```text
a
b
```

`next()` asks the iterator for the next value until it runs out.

## 2. Iterator foundations

### An iterable can become an iterator

```python
items = ["a", "b"]
iterator = iter(items)
print(next(iterator))
print(next(iterator))
```

Output:

```text
a
b
```

### Iterators are one-pass

```python
items = iter([1, 2])
print(list(items))
print(list(items))
```

Output:

```text
[1, 2]
[]
```

### `for` loops use iterators internally

```python
for item in [1, 2, 3]:
    print(item)
```

Output:

```text
1
2
3
```

## 3. Iterator protocol operations

- `iter(obj)` creates an iterator.
- `next(it)` returns the next item.
- `StopIteration` marks the end.

```python
items = iter(["x"])
print(next(items))
```

Output:

```text
x
```

## 4. Practical iteration

### Example 1: Manual iteration

```python
items = iter([10, 20])
print(next(items))
print(next(items))
```

Output:

```text
10
20
```

### Example 2: Use an iterator in a loop

```python
for value in iter([1, 2, 3]):
    print(value)
```

Output:

```text
1
2
3
```

### Example 3: Exhaustion

```python
items = iter([1])
print(next(items))
print(list(items))
```

Output:

```text
1
[]
```

- stream values from large inputs;
- consume file-like or data-source iterables;
- build generator pipelines later;
- stop early when you only need part of the data.

## 5. Iterator mistakes

### Mistake 1: Treating an iterator like a reusable list

Iterators are consumed as you read them.

### Mistake 2: Calling `next()` without handling the end

If there are no values left, Python raises `StopIteration`.

### Mistake 3: Confusing iterable with iterator

An iterable can produce an iterator, but it is not necessarily one itself.

## 6. Iteration decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Reusable collection | `list` | can be reused and indexed |
| One-pass traversal | iterator | memory-friendly |
| Lazy pipeline | generator/iterator | no intermediate list |

## 7. Performance and safety

- iterators are efficient for streaming;
- they are not reusable without recreating them;
- do not assume you can index them like a list.

## 8. Advanced iterator behavior

- custom iterator classes;
- iterator chaining;
- interaction with generator functions.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| Iterable | can be looped over |
| Iterator | yields one value at a time |
| `iter()` | creates iterator |
| `next()` | gets next value |
| Exhaustion | iterator is empty |

## 10. Iterable versus iterator ownership

An iterable normally creates a fresh iterator. An iterator returns itself and is
consumed in place.

```python
values = [10, 20]
first = iter(values)
second = iter(values)

print(first is second)
print(next(first), next(second))
```

Output:

```text
False
10 10
```

Returning a fresh iterator from `__iter__` makes a container reusable; returning
`self` makes a stateful iterator one-pass.

## 11. Callable-sentinel iteration

`iter(callable, sentinel)` repeatedly calls a zero-argument callable until the
returned value equals the sentinel.

```python
from io import StringIO

stream = StringIO("first\nsecond\n")
lines = [line.strip() for line in iter(stream.readline, "")]
print(lines)
```

Output:

```text
['first', 'second']
```

This form is useful for chunked reads without a manual `while True` loop.

## 12. Subtle iterator costs

- `itertools.tee()` may buffer all values consumed by the faster branch; it is
  not a free copy and is not generally thread-safe.
- `operator.length_hint()` is an optimization hint, not an exact-size contract.
- Mutating a source during iteration can skip values, duplicate work, or raise;
  iterate over a snapshot or redesign ownership.
- A `for` loop handles `StopIteration`; direct `next()` calls need a default or a
  specific exception boundary.
