# CPython Runtime Internals

CPython is the reference implementation of Python and the implementation most people install from python.org. Python is the language specification; CPython is one program that implements that language.

## 1. First Mental Model

```text
source text
   -> tokenize and parse
   -> abstract syntax tree (AST)
   -> code object containing bytecode
   -> evaluation loop executes instructions in frames
   -> objects are allocated, referenced, and eventually reclaimed
```

CPython is often called interpreted, but it still compiles source into bytecode before executing it.

## 2. Confirm the Implementation

```python
import platform
import sys

print(platform.python_implementation())
print(sys.implementation.name)
print(sys.version_info[:2])
```

Example output on Python 3.12:

```text
CPython
cpython
(3, 12)
```

Do not assume implementation details apply to PyPy, GraalPy, MicroPython, or another runtime.

## 3. Parse Source into an AST

The AST represents language structure rather than machine instructions.

```python
import ast

tree = ast.parse("total = price * quantity")
print(ast.dump(tree, indent=2))
```

Shortened output:

```text
Module(
  body=[
    Assign(
      targets=[Name(id='total', ctx=Store())],
      value=BinOp(
        left=Name(id='price', ctx=Load()),
        op=Mult(),
        right=Name(id='quantity', ctx=Load())))])
```

Tools that analyze or transform Python source often work with `ast`. Never execute an untrusted AST or untrusted source merely because it parsed successfully.

## 4. Compile to a Code Object

```python
source = "result = 6 * 7"
code = compile(source, "<lesson>", "exec")

print(type(code).__name__)
print(code.co_names)
exec(code, {})
```

Output:

```text
code
('result',)
```

`compile` creates a code object. `exec` executes arbitrary code and must never receive untrusted input.

Useful code-object attributes include:

- `co_code`: encoded bytecode;
- `co_consts`: constants referenced by the code;
- `co_names`: global or attribute names;
- `co_varnames`: local variable names;
- `co_freevars`: variables captured from an enclosing scope;
- `co_filename` and `co_firstlineno`: debugging metadata.

These are CPython-facing diagnostic details, not an API for application business logic.

## 5. Inspect Bytecode

```python
import dis


def total(price: int, quantity: int) -> int:
    return price * quantity


dis.dis(total)
```

The exact instruction names and offsets depend on the Python version. You will see instructions that load the two local variables, perform multiplication, and return the result.

Use bytecode inspection to learn or diagnose. Do not build production logic around a bytecode sequence because CPython changes and specializes instructions across releases.

## 6. Frames Hold Active Execution State

Each active Python call has a frame containing its code, namespaces, instruction position, and links needed for execution and debugging.

```python
import sys


def inspect_frame(course: str) -> None:
    frame = sys._getframe()
    print(frame.f_code.co_name)
    print(frame.f_locals["course"])


inspect_frame("CPython")
```

Output:

```text
inspect_frame
CPython
```

`sys._getframe` is intentionally implementation-oriented. Holding frames can retain all objects referenced by their locals and create unexpected memory growth. Debuggers and profilers use frames carefully; application code rarely needs them.

## 7. Name Lookup Is Namespace Lookup

Python's common LEGB description means:

1. local namespace;
2. enclosing function namespaces;
3. module global namespace;
4. built-ins.

```python
label = "global"


def outer() -> None:
    label = "enclosing"

    def inner() -> None:
        print(label)

    inner()


outer()
```

Output:

```text
enclosing
```

The compiler decides whether a function name is local, free, cell, or global based on the function body. Assignment makes a name local unless `global` or `nonlocal` declares another scope.

## 8. Function Calls and Vectorcall

At the language level, a call evaluates the callable, evaluates arguments, binds parameters, executes the body, and returns or raises.

CPython uses optimized internal calling conventions, including vectorcall, to reduce temporary argument objects for many calls. Treat vectorcall as an extension-author concern. In normal Python, improve algorithms and remove needless calls only when profiling proves they matter.

## 9. Objects Have Identity, Type, and Value

Every Python object has:

- identity: observed with `id`;
- type: observed with `type`;
- value/state: defined by that type.

```python
first = [1, 2]
second = first
third = [1, 2]

print(first is second)
print(first is third)
print(first == third)
```

Output:

```text
True
False
True
```

In CPython's C implementation, most objects begin with a header containing a reference count and a pointer to their type object. The precise layout is internal and can vary by build or version.

## 10. Reference Counting

CPython normally reclaims a non-cyclic object as soon as its strong-reference count reaches zero.

```python
import sys

value = []
alias = value
print(sys.getrefcount(value) >= 3)

del alias
print(sys.getrefcount(value) >= 2)
```

Output:

```text
True
True
```

`getrefcount` temporarily adds a reference for its own argument, so it is useful for learning but not for asserting an exact production count.

Operations that create strong references include:

- assigning another name;
- placing the object in a container;
- storing it on another object;
- capturing it in a closure;
- caching it globally.

`del name` removes one binding. It does not mean "delete this object" if other references remain.

## 11. Cyclic Garbage Collection

Reference counting alone cannot reclaim an unreachable cycle:

```python
import gc

left: list[object] = []
right: list[object] = [left]
left.append(right)

del left
del right

collected = gc.collect()
print(collected >= 2)
```

Typical CPython output:

```text
True
```

The cyclic collector tracks containers that can participate in cycles and periodically searches generations of tracked objects. Collection timing and the returned count are implementation details; never use GC timing for required resource cleanup.

Use context managers for files, locks, sockets, and transactions.

## 12. Weak References

A weak reference observes an object without keeping it alive.

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

Weak references are useful for caches, observers, and parent links where ownership belongs elsewhere. Not every built-in type supports them.

## 13. CPython Memory Allocators

The conceptual layers are:

```text
Python object allocator
    -> small-object allocator (commonly pymalloc for suitable requests)
    -> platform allocator
    -> operating-system virtual memory
```

CPython can keep freed memory in pools or free lists for reuse. Therefore:

- an object can be destroyed without process RSS immediately falling;
- a stable RSS does not prove a leak;
- a growing RSS does not identify which Python objects are responsible.

Use `tracemalloc` for Python allocation traces and operating-system tools for total process memory.

## 14. `__slots__`

Instances normally store attributes in a dictionary. Slots can remove that per-instance dictionary when a fixed layout is appropriate.

```python
class Course:
    __slots__ = ("course_id", "title")

    def __init__(self, course_id: str, title: str) -> None:
        self.course_id = course_id
        self.title = title


course = Course("python", "Python Internals")
print(course.title)
print(hasattr(course, "__dict__"))
```

Output:

```text
Python Internals
False
```

Slots can reduce memory for very large numbers of instances, but they affect inheritance, weak references, dynamic attributes, and serialization. Measure before adopting them.

## 15. The GIL

In a traditional GIL-enabled CPython build, the Global Interpreter Lock ensures that one thread at a time executes Python bytecode in one interpreter.

It does not mean:

- threads are useless;
- a multi-step Python operation is an application-level transaction;
- shared mutable data needs no lock;
- native code can never run in parallel.

I/O operations and native extensions may release the GIL. Another thread can then run.

```python
import threading

counter = 0
lock = threading.Lock()


def increment() -> None:
    global counter
    for _ in range(10_000):
        with lock:
            counter += 1


threads = [threading.Thread(target=increment) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(counter)
```

Output:

```text
20000
```

The lock protects the application invariant. Do not depend on the GIL for compound shared-state correctness.

## 16. Free-Threaded CPython

Newer CPython releases provide a separately built free-threaded mode in which the GIL can be disabled. It changes implementation costs and exposes races previously hidden by serialized bytecode execution.

When supported by the running version, inspect the mode through its documented runtime API. Feature-detect rather than assuming that a version number means the GIL is disabled.

```python
import sys

is_gil_enabled = getattr(sys, "_is_gil_enabled", None)
if is_gil_enabled is None:
    print("This Python does not expose a GIL status API")
else:
    print(f"GIL enabled: {is_gil_enabled()}")
```

On CPython 3.12, output is:

```text
This Python does not expose a GIL status API
```

Third-party extensions must explicitly support free-threaded execution. Always test the exact interpreter build and dependency set.

## 17. Specializing Interpreter

Modern CPython can adapt frequently executed bytecode to observed runtime types. This reduces dispatch overhead while preserving Python behavior.

Consequences:

- warm code may behave differently in a microbenchmark from its first calls;
- exact bytecode can change while a process runs;
- disassembly is diagnostic evidence, not a stable application contract.

## 18. `.pyc` Cache Files

CPython may cache compiled bytecode under `__pycache__` to avoid recompiling unchanged modules.

The cache:

- is an optimization, not source protection;
- is invalidated according to cache metadata;
- is safe to remove when the interpreter is not using it;
- should not be treated as a portable deployment artifact across arbitrary versions and platforms.

## 19. Import Execution

Import roughly performs:

1. check `sys.modules`;
2. find a module specification;
3. create a module object;
4. place it in `sys.modules` before execution completes;
5. execute top-level code;
6. return the cached module.

Step 4 explains partially initialized modules during circular imports. Keep import-time work small and design dependency direction to avoid cycles.

## 20. Internals Debugging Toolkit

```powershell
python -m dis module.py
python -X dev module.py
python -X tracemalloc=10 module.py
python -m cProfile -o profile.prof module.py
```

Useful standard modules include `ast`, `dis`, `gc`, `inspect`, `sys`, `tracemalloc`, and `weakref`.

## Final Rules

- distinguish Python language behavior from CPython implementation details;
- use `dis` and frames for diagnosis, not business logic;
- track strong references when debugging lifetime;
- use cyclic GC only as a collector, not a cleanup contract;
- measure Python allocations and process memory separately;
- protect shared invariants explicitly even on GIL-enabled builds;
- test free-threaded mode and extension compatibility deliberately;
- optimize only after a representative profile identifies a bottleneck.

