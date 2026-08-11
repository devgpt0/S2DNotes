# PYTHON - EXECUTION MODEL

This chapter explains what Python does when it reads a module, resolves a name, calls a function, raises an exception, imports another module, or pauses an async task.

## 1. Source to Execution

For CPython:

```text
.py source -> tokens and AST -> code object and bytecode -> frame execution
```

```python
source = "answer = 6 * 7"
code = compile(source, "<lesson>", "exec")
namespace: dict[str, object] = {}
exec(code, namespace)

print(namespace["answer"])
```

Output:

```text
42
```

`exec` runs arbitrary code. Never pass it untrusted input.

## 2. Module Execution

Python executes a module's top-level statements from top to bottom.

```python
print("first")

course = "Python"

print(f"second: {course}")
```

Output:

```text
first
second: Python
```

A `def` statement creates a function object. The function body runs only when called.

```python
print("before definition")


def teach() -> None:
    print("inside function")


print("before call")
teach()
```

Output:

```text
before definition
before call
inside function
```

## 3. Names and Objects

```python
topics = ["typing"]
alias = topics
alias.append("profiling")

print(topics)
```

Output:

```text
['typing', 'profiling']
```

Execution binds names to objects. Assignment does not create a deep copy.

## 4. Execution Frames

Each active Python function call has an execution frame. Conceptually, a frame contains:

- the code being executed;
- local variables;
- access to global and built-in namespaces;
- the current instruction position;
- exception-handling state;
- links needed for calls and debugging.

```python
def inner(value: int) -> int:
    return value * 2


def outer() -> int:
    result = inner(21)
    return result


print(outer())
```

Output:

```text
42
```

Flow:

```text
module frame -> call outer -> outer frame -> call inner -> inner frame
             <- return 42  <- outer returns 42
```

## 5. LEGB Name Resolution

For a normal name lookup inside nested functions, Python searches:

1. local;
2. enclosing function scopes;
3. module globals;
4. built-ins.

```python
label = "global"


def outer() -> None:
    label = "enclosing"

    def inner() -> None:
        label = "local"
        print(label)

    inner()


outer()
```

Output:

```text
local
```

Class-body name lookup has additional details and should not be reduced blindly to the nested-function LEGB diagram.

## 6. Local Variables Are Determined by the Function Body

```python
count = 10


def broken() -> None:
    print(count)
    count = 11


try:
    broken()
except UnboundLocalError as error:
    print(type(error).__name__)
```

Output:

```text
UnboundLocalError
```

Because the body assigns `count`, the compiler treats it as local throughout that function. The read occurs before the local binding.

Fix the design by passing and returning data:

```python
def increment(count: int) -> int:
    return count + 1


count = increment(10)
print(count)
```

Output:

```text
11
```

Prefer explicit data flow over mutable globals.

## 7. `nonlocal` Rebinds an Enclosing Name

```python
from collections.abc import Callable


def make_counter() -> Callable[[], int]:
    count = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


counter = make_counter()
print(counter())
print(counter())
```

Output:

```text
1
2
```

The closure keeps the enclosing cell alive. Hidden closure state can be useful but should not replace an explicit object when lifecycle and inspection matter.

## 8. Function Call Order

Python evaluates the callable and argument expressions before entering the function body.

```python
def make_value(label: str, value: int) -> int:
    print(label)
    return value


def add(left: int, right: int) -> int:
    print("inside add")
    return left + right


print(add(make_value("left", 20), make_value("right", 22)))
```

Output:

```text
left
right
inside add
42
```

Do not put order-sensitive side effects inside argument expressions when a few explicit statements are clearer.

## 9. Parameter Binding

```python
def describe(course_id: str, *, active: bool = True) -> None:
    print(f"{course_id=}, {active=}")


describe("python", active=False)
```

Output:

```text
course_id='python', active=False
```

Before the body runs, Python binds positional, keyword, default, variadic, positional-only, and keyword-only parameters according to the signature. Invalid binding raises `TypeError` before the body begins.

## 10. Return and `finally`

```python
def example() -> str:
    try:
        return "result"
    finally:
        print("cleanup")


print(example())
```

Output:

```text
cleanup
result
```

The return value is prepared, `finally` runs, and then the function returns. A `return` or new exception inside `finally` can replace the earlier result or exception; avoid that confusing behavior.

## 11. Exception Propagation

```python
def parse_level(raw: str) -> int:
    return int(raw)


def load_level(raw: str) -> int:
    try:
        return parse_level(raw)
    except ValueError as error:
        raise ValueError("level must be an integer") from error


try:
    load_level("advanced")
except ValueError as error:
    print(error)
    print(type(error.__cause__).__name__)
```

Output:

```text
level must be an integer
ValueError
```

An unhandled exception unwinds frames until a matching handler is found. `finally` blocks and context-manager exits run during unwinding.

## 12. Context Manager Execution

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

Conceptually, `with` evaluates the manager, calls `__enter__`, executes the body, and always calls `__exit__`. Returning `True` from `__exit__` suppresses an exception; do that only when suppression is the explicit contract.

## 13. Iterator Execution

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

A `for` loop repeatedly calls `next` and handles `StopIteration` internally.

## 14. Generator Suspension

```python
from collections.abc import Iterator


def lessons() -> Iterator[str]:
    print("started")
    yield "fundamentals"
    print("resumed")
    yield "internals"


iterator = lessons()
print("created")
print(next(iterator))
print(next(iterator))
```

Output:

```text
created
started
fundamentals
resumed
internals
```

Calling a generator function creates a generator object without running its body. `next` resumes its saved frame until the next `yield`, return, or exception.

## 15. Decorator Execution Time

Decorators run when the decorated function or class is defined, usually during module import.

```python
from collections.abc import Callable


def announce(function: Callable[[], None]) -> Callable[[], None]:
    print(f"decorating {function.__name__}")
    return function


@announce
def teach() -> None:
    print("teaching")


print("before call")
teach()
```

Output:

```text
decorating teach
before call
teaching
```

Avoid decorators that perform network, database, or other expensive side effects at import time.

## 16. Class Statement Execution

A class statement executes its body in a namespace and then calls a class-creation mechanism, normally `type`.

```python
print("before class")


class Course:
    print("inside class body")
    category = "programming"


print(Course.category)
```

Output:

```text
before class
inside class body
programming
```

Methods are function objects placed in the class namespace. Descriptor binding later turns a function retrieved through an instance into a bound method.

## 17. Import Execution and Cache

On a normal import, Python:

1. checks `sys.modules`;
2. finds a module specification;
3. creates a module object;
4. caches it before execution finishes;
5. executes top-level code;
6. returns the module.

```python
import math
import sys

print("math" in sys.modules)
print(math.sqrt(81))
```

Output:

```text
True
9.0
```

The early cache insertion explains why circular imports can observe a partially initialized module. Fix dependency direction rather than scattering local imports as a default workaround.

## 18. Main-Module Guard

```python
def main() -> None:
    print("application started")


if __name__ == "__main__":
    main()
```

Output:

```text
application started
```

When executed as the main module, `__name__` is `"__main__"`. When imported, the guard prevents `main()` from running. Package console entry points are a cleaner installed-command mechanism.

## 19. Thread Execution

Threads in one process share objects. The OS and interpreter can switch execution between threads.

```python
from threading import Thread

items: list[str] = []


def worker() -> None:
    items.append("worker")


thread = Thread(target=worker)
thread.start()
thread.join()

print(items)
```

Output:

```text
['worker']
```

In a GIL-enabled CPython build, one thread executes Python bytecode at a time per interpreter, but I/O and native code can release the GIL. Shared multi-step invariants still need synchronization.

## 20. Async Execution

An `async def` call creates a coroutine object. Its body runs when awaited or scheduled.

```python
import asyncio


async def lesson() -> str:
    print("lesson started")
    await asyncio.sleep(0)
    print("lesson resumed")
    return "done"


async def main() -> None:
    coroutine = lesson()
    print("coroutine created")
    print(await coroutine)


asyncio.run(main())
```

Output:

```text
coroutine created
lesson started
lesson resumed
done
```

At `await`, the task may suspend so another ready task can run. Re-check shared-state assumptions after every await boundary.

## 21. Process Execution

Separate processes normally have separate Python runtimes and memory spaces. Arguments and results commonly cross process boundaries through serialization and inter-process communication.

```python
import subprocess
import sys

state = "parent"
result = subprocess.run(
    [sys.executable, "-c", "state = 'child'; print(state)"],
    capture_output=True,
    check=True,
    text=True,
)

print(state)
print(result.stdout.strip())
```

Output:

```text
parent
child
```

Use the `if __name__ == "__main__":` guard around process-starting application code, especially with spawn-based platforms.

## 22. CPython Bytecode Is Not a Stable API

The `dis` module can explain execution:

```python
import dis


def double(value: int) -> int:
    return value * 2


instructions = list(dis.Bytecode(double))
print(len(instructions) > 0)
print(all(isinstance(instruction.opname, str) for instruction in instructions))
```

Output:

```text
True
True
```

`dis.dis()` can print the instructions, but instruction names and specialization can change by Python version. Use bytecode for diagnosis and learning, not application branching.

## 23. Debugging Execution

Ask these questions:

1. Which statement executes now?
2. Which frame and namespace own each name?
3. Which objects do the names reference?
4. Is the operation mutation or rebinding?
5. Which call, yield, await, import, or exception changes control flow?
6. Which `finally` or context-manager cleanup must run?
7. Can another task, thread, or process observe or change state?

## Final Rules

- modules and class bodies execute top to bottom;
- function and coroutine bodies run only after call plus execution/await;
- parameters are local bindings to evaluated argument objects;
- name scope is determined from the code, not runtime guesswork;
- exceptions unwind frames and run cleanup;
- generators and coroutines preserve suspended execution state;
- imports execute code and cache partially initialized modules;
- every await or synchronization boundary can invalidate state assumptions;
- treat CPython bytecode and frame details as diagnostics, not business contracts.
