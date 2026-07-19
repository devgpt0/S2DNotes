# Python Memory Model - Beginner to Expert

Python variables do not contain objects. A variable is a name bound to an object.

## 1. Names Point to Objects

```python
course = ["python"]
alias = course

print(course is alias)
alias.append("memory")
print(course)
```

Output:

```text
True
['python', 'memory']
```

Both names refer to the same list. Mutation through either name is visible through the other.

```text
course ----+
           +----> ["python", "memory"]
alias  ----+
```

## 2. Identity, Type, and Value

Every object has:

- identity: `is` compares whether two references point to the same object;
- type: `type(value)` reports behavior and representation;
- value/state: `==` asks the type whether values are equal.

```python
first = [1, 2]
second = [1, 2]

print(first == second)
print(first is second)
print(type(first).__name__)
```

Output:

```text
True
False
list
```

Use `is` for identity, especially `value is None`. Use `==` for value equality.

## 3. Assignment Binds a Name

```python
left = [1, 2]
right = left
right = [3, 4]

print(left)
print(right)
```

Output:

```text
[1, 2]
[3, 4]
```

`right = left` binds a second name to the original list. `right = [3, 4]` later rebinds only `right`; it does not mutate the original.

## 4. Mutation Versus Rebinding

```python
values = [1]
same_values = values
values += [2]

print(values)
print(values is same_values)

title = "Py"
same_title = title
title += "thon"

print(title)
print(title is same_title)
```

Output:

```text
[1, 2]
True
Python
False
```

`list.__iadd__` mutates and returns the list. Strings are immutable, so string concatenation creates a new object and rebinds the name.

Do not memorize that `+=` always mutates or always copies; the type defines in-place behavior.

## 5. Mutable and Immutable Types

Common immutable types:

- `int`, `float`, `bool`, `complex`;
- `str`, `bytes`;
- `tuple` when considering tuple structure;
- `frozenset`;
- many user-defined value objects designed without mutation.

Common mutable types:

- `list`, `dict`, `set`, `bytearray`;
- most ordinary user-defined instances.

A tuple cannot replace its elements, but it can refer to a mutable object:

```python
record = ("python", ["typing"])
record[1].append("profiling")
print(record)
```

Output:

```text
('python', ['typing', 'profiling'])
```

The tuple structure did not change; the nested list changed.

## 6. Function Arguments Use Object Sharing

Python evaluates an argument to an object and binds the function parameter to that object. This is often called call by sharing.

```python
def add_topic(topics: list[str]) -> None:
    topics.append("memory")


def replace_topics(topics: list[str]) -> None:
    topics = ["replacement"]
    print(f"inside: {topics}")


original = ["python"]
add_topic(original)
print(original)

replace_topics(original)
print(original)
```

Output:

```text
['python', 'memory']
inside: ['replacement']
['python', 'memory']
```

Mutation affects the shared list. Rebinding the local parameter does not rebind the caller's name.

## 7. Shallow Copy

A shallow copy creates a new outer container but shares nested objects.

```python
from copy import copy

original = [["python"], ["rust"]]
duplicate = copy(original)

duplicate.append(["go"])
duplicate[0].append("typing")

print(original)
print(duplicate)
```

Output:

```text
[['python', 'typing'], ['rust']]
[['python', 'typing'], ['rust'], ['go']]
```

The outer lists differ. Their first nested list is shared.

## 8. Deep Copy

`deepcopy` recursively copies while preserving repeated-reference and cycle relationships through a memo table.

```python
from copy import deepcopy

original = [["python"], ["rust"]]
duplicate = deepcopy(original)
duplicate[0].append("typing")

print(original)
print(duplicate)
```

Output:

```text
[['python'], ['rust']]
[['python', 'typing'], ['rust']]
```

Deep copy is not automatically correct. Files, sockets, locks, database sessions, caches, and identity-based domain objects may not be meaningfully copyable. Prefer an explicit domain operation when copy semantics matter.

## 9. Mutable Default Argument Trap

Default arguments are evaluated once when the function is defined.

```python
def broken_add(topic: str, topics: list[str] = []) -> list[str]:
    topics.append(topic)
    return topics


print(broken_add("typing"))
print(broken_add("profiling"))
```

Output:

```text
['typing']
['typing', 'profiling']
```

Use `None` to request a new list:

```python
def add_topic(topic: str, topics: list[str] | None = None) -> list[str]:
    result = [] if topics is None else topics
    result.append(topic)
    return result


print(add_topic("typing"))
print(add_topic("profiling"))
```

Output:

```text
['typing']
['profiling']
```

This function deliberately mutates a provided list. Document that contract or copy the input if callers require isolation.

## 10. Closures Retain Objects

```python
from collections.abc import Callable


def make_reader() -> Callable[[], list[str]]:
    values = ["python", "memory"]

    def read() -> list[str]:
        return values.copy()

    return read


reader = make_reader()
print(reader())
```

Output:

```text
['python', 'memory']
```

The returned function's closure keeps `values` alive after `make_reader` returns. Closures, callbacks, task objects, and tracebacks can retain unexpectedly large object graphs.

## 11. Reference Counting in CPython

CPython tracks strong references to most objects. When a non-cyclic object's reference count reaches zero, CPython usually destroys it immediately.

```python
import sys

values: list[int] = []
alias = values

before = sys.getrefcount(values)
del alias
after = sys.getrefcount(values)

print(after < before)
```

Output:

```text
True
```

`getrefcount` adds a temporary reference for the call, so use it for learning rather than exact production assertions.

Other Python implementations may use different memory-management strategies. Immediate CPython cleanup is not a portable resource-management contract.

## 12. Cyclic Garbage Collection

Two objects can keep each other referenced even when the application can no longer reach them.

```python
import gc

first: list[object] = []
second: list[object] = [first]
first.append(second)

del first
del second

print(gc.collect() >= 2)
```

Typical CPython output:

```text
True
```

CPython's cyclic collector searches tracked container objects for unreachable cycles. Collection timing and counts can vary.

## 13. Finalizers and Cycles

`__del__` is difficult to reason about:

- execution time is not guaranteed across implementations;
- interpreter shutdown can remove dependencies first;
- object resurrection is possible;
- exceptions cannot be handled by the caller normally.

Use a context manager for deterministic cleanup. Use `weakref.finalize` only when a non-deterministic safety net is genuinely needed.

## 14. Weak References and Non-Ownership

```python
import weakref


class Course:
    pass


course = Course()
reference = weakref.ref(course)
print(reference() is course)

del course
print(reference())
```

Output:

```text
True
None
```

A weak reference does not own the object. The caller must handle the object disappearing between observations, especially with concurrency.

## 15. Why RSS May Stay High

Deleting Python objects does not guarantee the operating system immediately receives memory back. CPython and the platform allocator can retain arenas or pools for future allocations.

Distinguish:

- live Python objects;
- unused memory retained by allocators;
- native-library allocations;
- memory-mapped files;
- process RSS reported by the OS.

Use `tracemalloc` for Python allocation sources and an OS/native profiler for complete process memory.

## 16. Common Retention Causes

- unbounded dictionaries, lists, or caches;
- queues whose consumers cannot keep up;
- completed futures or tasks retained forever;
- event handlers that are never unregistered;
- global registries;
- closures retaining large context;
- tracebacks stored after failures;
- cycles containing long-lived objects;
- per-request data stored in thread-local or context state;
- native extensions with unclear ownership.

## 17. Diagnose Growth with Snapshots

```python
import tracemalloc

tracemalloc.start(10)
before = tracemalloc.take_snapshot()

values = [str(number) for number in range(10_000)]

after = tracemalloc.take_snapshot()
differences = after.compare_to(before, "lineno")

print(len(values))
print(len(differences) > 0)
```

Output:

```text
10000
True
```

Repeat the same workload and compare stable checkpoints. One snapshot tells you where allocations exist; repeated retained growth is stronger leak evidence.

## 18. Memory-Efficient Representations

Consider, based on evidence:

- generators for one-pass streams;
- `array`, NumPy arrays, or packed binary formats for large homogeneous numeric data;
- `__slots__` for very large numbers of simple instances;
- `memoryview` for zero-copy buffer slices;
- bounded caches and queues;
- database pagination or streaming cursors;
- processes when isolation and lifecycle reset are useful.

Every representation has API, dependency, and maintainability costs. Measure peak memory and end-to-end latency.

## 19. Resource Lifetime Is Not Object Lifetime

```python
from pathlib import Path


def read_first_line(path: Path) -> str:
    with path.open(encoding="utf-8") as stream:
        return stream.readline().rstrip("\n")
```

The `with` statement closes the file on success or failure. Do not wait for object destruction to release an external resource.

## 20. Review Checklist

- Which names and containers own this object?
- Is mutation visible through aliases?
- Is a copy shallow, deep, or domain-specific?
- Can a closure, callback, traceback, or cache retain it?
- Is a cycle possible?
- Is external-resource cleanup deterministic?
- Is the queue/cache/result set bounded?
- Are Python allocations or native allocations growing?
- Does the design depend on CPython-specific immediate destruction?

## Final Rules

- names bind to objects;
- assignment does not copy an object;
- distinguish mutation from rebinding;
- define copy semantics explicitly;
- avoid mutable default arguments;
- understand strong, weak, and cyclic references;
- use context managers for resources;
- diagnose retained objects with repeated evidence;
- optimize representation only after measuring real memory use.
