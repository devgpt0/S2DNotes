# PYTHON - FUNCTIONS

## 1. Core Mental Model

Python function questions are mostly about:
- Argument binding rules
- Default argument evaluation timing
- Mutability and aliasing
- Scope and closures (LEGB)
- Return behavior with try/finally

If you simulate these in order, most tricky outputs become predictable.

## 2. Argument Binding Order

Python binds call arguments in this practical sequence:
1. Positional arguments
2. Unpacked positional (*iterable)
3. Keyword arguments
4. Unpacked keyword (**mapping)
5. Remaining defaults

Conflict rules:
- Same parameter assigned twice -> TypeError.
- Too many positional args -> TypeError.
- Missing required args -> TypeError.

Keyword argument order in call does not matter for matching by name.

## 3. Positional-Only and Keyword-Only Parameters

Syntax markers:
- / : parameters before this are positional-only.
- * : parameters after this are keyword-only (unless captured by *args).

Examples of what these markers enforce are common interview traps.

## 4. Default Arguments: Evaluated Once

Default values are created at function definition time, not each call.

Mutable defaults (list, dict, set) persist across calls:
- Using append on a default list reuses same list.
- This causes state leakage between calls.

Safe pattern:
- Use None default, then create new object inside function.

## 5. Mutation vs Reassignment

Inside function:
- Mutation changes the same object (visible outside if shared).
- Reassignment binds local name to a new object (caller object unchanged).

Example distinction:
- x.append(4) mutates shared list.
- x = x + [4] creates new list and rebinds local x.

## 6. *args and **kwargs Unpacking

Unpacking expands data into call-site arguments.

Important rules:
- * provides positional arguments.
- ** provides keyword arguments.
- Multiple unpackings are merged left to right, but duplicate keys/targets raise error.

## 7. Closures and Late Binding

Closures capture variables by reference (name lookup at call time).

Classic trap:
- Lambdas created in loop all use final loop variable value.

Common fix:
- Bind current value as default parameter, e.g. lambda i=i: i

## 8. LEGB, nonlocal, global

Lookup order: Local -> Enclosing -> Global -> Builtins.

- Assigning to a name in function creates local binding unless declared otherwise.
- nonlocal updates variable from nearest enclosing function scope.
- global updates module-level variable.

## 9. Functions as First-Class Objects

In Python, functions can be:
- Passed as arguments
- Returned from other functions
- Stored in variables/collections
- Wrapped by decorators

Decorator mental model:
- @decorator replaces original function object with wrapper returned by decorator.

## 10. try/finally Return Behavior

finally always executes before function exits.

Critical rule:
- If finally has return, it overrides return from try/except.

This mirrors a common interview edge case and can hide errors.

## 11. Introspection and Callability

Useful internals often asked:
- f.__code__.co_varnames -> local variable names (including params)
- f.__code__.co_argcount -> positional parameter count
- callable(obj) -> whether object can be invoked with ()

## 12. Interview Solve Template

For any function snippet:
1. Bind arguments exactly (including *, **, /, and * markers).
2. Check for binding conflicts first.
3. Determine whether operations mutate or rebind.
4. Apply LEGB for each variable read/write.
5. For closures, decide if value is late-bound or fixed via default.
6. Apply try/finally return override last.

## 13. Worksheet Concept Coverage Checklist

- Mutable default argument pitfalls
- Positional vs keyword binding
- *args / **kwargs unpacking and conflicts
- Positional-only (/) and keyword-only (*) rules
- Mutation vs reassignment for lists
- Closure late binding and lambda fixes
- LEGB with nonlocal/global
- Functions as first-class objects
- Decorator wrapping behavior
- try/finally return override
- map/callable/code object basics

## 14. Decorators (Interview + Real Project Essential)

A decorator is a function that takes another function and returns a wrapped function.

Mental model:
```text
decorated_function = decorator(original_function)
```

`@decorator_name` is just shorthand for that replacement.

Example:
```python
from functools import wraps


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[BEFORE] calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[AFTER] {func.__name__} returned {result}")
        return result
    return wrapper


@log_call
def add(a, b):
    print("Inside add()")
    return a + b


total = add(10, 20)
print("Final total:", total)
print("Function name after decoration:", add.__name__)
```

Expected output:
```text
[BEFORE] calling add with args=(10, 20), kwargs={}
Inside add()
[AFTER] add returned 30
Final total: 30
Function name after decoration: add
```

Why `@wraps` matters:
- preserves original function metadata (`__name__`, docstring)
- helps debugging and tooling

## 15. Detailed Function Examples (Step by Step)

### 15.1 Argument Binding with `/` and `*`

```python
def build_url(protocol, /, host, *, port=80, path="/"):
    url = f"{protocol}://{host}:{port}{path}"
    print("Built URL:", url)
    return url


build_url("https", "example.com", port=443, path="/docs")

try:
    build_url(protocol="https", host="example.com")
except TypeError as error:
    print("Binding error:", error)
```

Expected output:
```text
Built URL: https://example.com:443/docs
Binding error: build_url() got some positional-only arguments passed as keyword arguments: 'protocol'
```

### 15.2 Mutable Default Trap vs Safe Pattern

```python
def add_tag_bad(tag, tags=[]):
    tags.append(tag)
    print("BAD tags now:", tags)
    return tags


def add_tag_good(tag, tags=None):
    tags = [] if tags is None else tags
    tags.append(tag)
    print("GOOD tags now:", tags)
    return tags


add_tag_bad("python")
add_tag_bad("django")

add_tag_good("python")
add_tag_good("django")
```

Expected output:
```text
BAD tags now: ['python']
BAD tags now: ['python', 'django']
GOOD tags now: ['python']
GOOD tags now: ['django']
```

### 15.3 Mutation vs Reassignment

```python
def mutate_list(values):
    values.append(99)
    print("Inside mutate_list:", values)


def reassign_list(values):
    values = values + [99]
    print("Inside reassign_list:", values)


numbers1 = [1, 2, 3]
numbers2 = [1, 2, 3]

mutate_list(numbers1)
print("After mutate_list:", numbers1)

reassign_list(numbers2)
print("After reassign_list:", numbers2)
```

Expected output:
```text
Inside mutate_list: [1, 2, 3, 99]
After mutate_list: [1, 2, 3, 99]
Inside reassign_list: [1, 2, 3, 99]
After reassign_list: [1, 2, 3]
```

### 15.4 Closures and Late Binding Fix

```python
bad_funcs = []
for i in range(3):
    bad_funcs.append(lambda: i)

print("Late binding result:", [func() for func in bad_funcs])

good_funcs = []
for i in range(3):
    good_funcs.append(lambda i=i: i)

print("Fixed closure result:", [func() for func in good_funcs])
```

Expected output:
```text
Late binding result: [2, 2, 2]
Fixed closure result: [0, 1, 2]
```

### 15.5 `try/finally` Return Override

```python
def tricky_return():
    try:
        print("Inside try block")
        return "TRY"
    finally:
        print("Inside finally block")
        return "FINALLY"


print("Function returned:", tricky_return())
```

Expected output:
```text
Inside try block
Inside finally block
Function returned: FINALLY
```

## 16. Decorator Usage Patterns (More Practical)

### 16.1 Parameterized Decorator

```python
from functools import wraps


def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for run in range(1, times + 1):
                print(f"Run {run}/{times}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def greet(name):
    print(f"Hello, {name}")


greet("Asha")
```

Expected output:
```text
Run 1/3
Hello, Asha
Run 2/3
Hello, Asha
Run 3/3
Hello, Asha
```

### 16.2 Stacked Decorators and Order

```python
from functools import wraps


def make_upper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        transformed = result.upper()
        print("make_upper applied")
        return transformed
    return wrapper


def add_exclamation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        transformed = result + "!"
        print("add_exclamation applied")
        return transformed
    return wrapper


@add_exclamation
@make_upper
def message():
    print("message() executed")
    return "python decorators"


print("Final message:", message())
```

Expected output:
```text
message() executed
make_upper applied
add_exclamation applied
Final message: PYTHON DECORATORS!
```

### 16.3 Real Use: Access Control Decorator

```python
from functools import wraps


def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(user_role, *args, **kwargs):
            if user_role != required_role:
                print(f"Access denied for role={user_role}")
                return None
            print(f"Access granted for role={user_role}")
            return func(user_role, *args, **kwargs)
        return wrapper
    return decorator


@require_role("admin")
def delete_user(user_role, username):
    print(f"Deleting user: {username}")
    return True


print("Admin attempt:", delete_user("admin", "ravi"))
print("Guest attempt:", delete_user("guest", "ravi"))
```

Expected output:
```text
Access granted for role=admin
Deleting user: ravi
Admin attempt: True
Access denied for role=guest
Guest attempt: None
```

### 16.4 Real Use: Timing Decorator

```python
import time
from functools import wraps


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {(end - start) * 1000:.2f} ms")
        return result
    return wrapper


@time_it
def compute_sum(n):
    total = sum(range(n + 1))
    print("Computed total:", total)
    return total


compute_sum(100000)
```

Expected output (time value will vary):
```text
Computed total: 5000050000
compute_sum took 1.23 ms
```

### 16.5 Async Function Decorator

```python
import asyncio
from functools import wraps


def async_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"[ASYNC BEFORE] {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"[ASYNC AFTER] {func.__name__} -> {result}")
        return result
    return wrapper


@async_log
async def fetch_profile(user_id):
    await asyncio.sleep(0.1)
    print(f"Fetching profile for user_id={user_id}")
    return {"user_id": user_id, "status": "ok"}


async def main():
    data = await fetch_profile(101)
    print("Final data:", data)


if __name__ == "__main__":
    asyncio.run(main())
```

Expected output:
```text
[ASYNC BEFORE] fetch_profile
Fetching profile for user_id=101
[ASYNC AFTER] fetch_profile -> {'user_id': 101, 'status': 'ok'}
Final data: {'user_id': 101, 'status': 'ok'}
```

## 17. Quick Practice Prompts

1. Write a decorator that retries a function 3 times on exception.
2. Write a decorator that caches function results for same arguments.
3. Write a decorator that validates all numeric arguments are positive.
4. Refactor one script in your notes to use a logging decorator.

## 18. Generators as Functions (Missing but Interview-Critical)

A generator function uses `yield` and returns an iterator.

```python
def read_chunks(data: list[int], size: int):
    for i in range(0, len(data), size):
        yield data[i : i + size]


for chunk in read_chunks([1, 2, 3, 4, 5], 2):
    print(chunk)
```

Why it matters:
- stream processing without loading everything at once.
- cleaner pipelines than manual index loops.

## 19. Function Contracts with Type Hints

Type hints make function intent explicit and tooling-friendly.

```python
from collections.abc import Iterable


def average(values: Iterable[float]) -> float:
    data = list(values)
    if not data:
        raise ValueError("values cannot be empty")
    return sum(data) / len(data)
```

Practical rule:
- prioritize hints on public APIs and shared utility functions first.

## 20. Callable Injection Pattern (Foundation for Clean Architecture)

Functions can be dependencies too, not only classes.

```python
from collections.abc import Callable


def process_order(
    amount: float,
    tax_fn: Callable[[float], float],
) -> float:
    return amount + tax_fn(amount)
```

Benefits:
- small, testable behavior injection.
- avoids unnecessary class ceremony.

## 21. `functools.singledispatch` for Controlled Ad-hoc Polymorphism

Useful when behavior varies by argument type.

```python
from functools import singledispatch


@singledispatch
def normalize(value):
    return str(value)


@normalize.register
def _(value: int):
    return value


@normalize.register
def _(value: list):
    return [normalize(v) for v in value]
```

Interview note:
- cleaner than long `isinstance` chains for type-based branching.

## 22. High-Value Function Pitfalls

- mutable default args retain state across calls.
- late binding in closures inside loops.
- forgetting to preserve metadata in decorators (`@wraps`).
- catching broad exceptions inside utility decorators and hiding failure.

## 23. Function Design Checklist (Production-Oriented)

1. one clear responsibility.
2. explicit input/output contract.
3. safe error behavior.
4. no hidden global side effects.
5. composable with other functions.
