# CPython Runtime Internals

## 1. CPython is an implementation

Python is a language; CPython is its most common implementation. Reference
counting, bytecode shape, object layout, and interpreter specialization are
CPython details, not portable language guarantees.

```python
import platform

print(platform.python_implementation() == "CPython")
```

Output on CPython:

```text
True
```

Other Python implementations may correctly print `False`.

## 2. Source becomes code objects

CPython parses source, compiles it to code objects, and executes their
instructions. The exact bytecode changes between Python releases.

```python
def double(value: int) -> int:
    return value * 2


code = double.__code__
print(code.co_name)
print(code.co_argcount)
print(isinstance(code.co_code, bytes))
```

Output:

```text
double
1
True
```

Use `dis.dis(double)` for diagnosis, but do not test exact bytecode text across
Python versions.

## 3. Names reference objects

Assignment binds a name to an object; it does not copy the object. Mutating a
shared mutable object is visible through every alias.

```python
primary = [1, 2]
alias = primary
alias.append(3)

print(primary)
print(primary is alias)
```

Output:

```text
[1, 2, 3]
True
```

Rebinding a name changes only that binding.

```python
primary = [1, 2]
alias = primary
alias = [9]

print(primary)
print(alias)
```

Output:

```text
[1, 2]
[9]
```

## 4. Object lifetime is implementation-sensitive

CPython normally combines reference counting with a cyclic garbage collector.
Never depend on an object being finalized immediately when its last visible
name disappears; use context managers for deterministic resource cleanup.

```python
from io import StringIO

buffer = StringIO("data")
with buffer:
    print(buffer.read())

print(buffer.closed)
```

Output:

```text
data
True
```

`sys.getrefcount()` is a diagnostic implementation detail and its raw value is
not stable enough for application logic or universal example output.

## 5. Function calls and objects have cost

Every Python-level call creates runtime work. Keep code readable first; remove
call or allocation overhead only after a profiler proves it matters.

```python
def square(value: int) -> int:
    return value * value


via_calls = [square(value) for value in range(4)]
inline = [value * value for value in range(4)]
print(via_calls == inline)
```

Output:

```text
True
```

Equivalent output does not prove equivalent speed. Benchmark the real workload.

## 6. Imports execute module code once per interpreter cache entry

The first normal import finds, loads, and executes a module. Later imports
usually reuse `sys.modules`.

```python
import json
import json as second
import sys

first = json

print(first is second)
print(sys.modules["json"] is first)
```

Output:

```text
True
True
```

Import-time side effects slow startup and make modules harder to test.

## 7. The GIL depends on the build

Traditional CPython builds use a Global Interpreter Lock (GIL) to protect
interpreter state. Free-threaded CPython builds are a separate configuration;
code must not infer the active mode from the Python version alone.

- Threads remain useful for blocking I/O.
- Processes remain a portable option for CPU parallelism.
- Free-threaded execution does not make shared mutable application state safe.
- Native extensions must explicitly support the interpreter build they run on.

See the concurrency notes for model selection and synchronization.

## 8. Safe inspection tools

| Tool | Use | Stability warning |
| --- | --- | --- |
| `dis` | inspect instructions | output is version-specific |
| `sys.getsizeof()` | shallow CPython object size | excludes referenced objects |
| `gc` | inspect cyclic-GC state | do not build business logic on it |
| `tracemalloc` | trace Python allocations | adds measurement overhead |
| `sys.modules` | inspect import cache | mutation can break imports |

## 9. Mental model

```text
source -> parser/compiler -> code object -> interpreter -> referenced objects
```

Treat the language reference as the contract. Use CPython internals to explain
measurements, not as an excuse to depend on unstable behavior.

## 10. Adaptive execution is deliberately unstable

Current CPython can specialize frequently executed instructions at runtime. The
specialized form may change with code behavior and Python releases; it is an
optimization, not a language guarantee.

Do not assert exact `dis` output or design code around a particular specialized
opcode. Profile application behavior instead.

## 11. Low-impact monitoring and isolated interpreters

`sys.monitoring` lets tools subscribe to selected interpreter events with lower
overhead than traditional all-event tracing. Tool identifiers and event masks
must be owned and released carefully; callbacks still add cost and must not
contain application business logic.

Subinterpreters isolate module and runtime state inside one process. On Python
3.14+, `concurrent.futures.InterpreterPoolExecutor` provides a high-level worker
interface. Objects do not become safely shared merely because workers occupy one
process; communication still needs an explicit serialization or supported
cross-interpreter channel.
