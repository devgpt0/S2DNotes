# PYTHON - ERRORS, EXCEPTIONS, AND DEBUGGING

An error means Python cannot continue normally or the program produced the wrong result.

## 1. Three Error Categories

| Category | Meaning | Example |
| --- | --- | --- |
| Syntax error | code cannot be parsed | missing `:` |
| Runtime error | execution raises an exception | division by zero |
| Logical error | code runs but gives a wrong result | wrong formula |

```python
source = "if True print('hello')"

try:
    compile(source, "<example>", "exec")
except SyntaxError as error:
    print(type(error).__name__)
```

Output:

```text
SyntaxError
```

Syntax errors must be fixed before that code can run.

## 2. Runtime Exceptions

An exception is an object that reports a runtime failure.

```python
try:
    result = 10 / 0
except ZeroDivisionError as error:
    print(type(error).__name__)
```

Output:

```text
ZeroDivisionError
```

Without a matching handler, the exception propagates and stops the current operation.

## 3. Logical Errors

Logical errors do not raise automatically. Tests and debugging must expose them.

```python
def rectangle_area(width, height):
    return width + height  # Intentional bug


actual = rectangle_area(4, 3)
expected = 12

print(actual)
print(actual == expected)
```

Output:

```text
7
False
```

Correct formula:

```python
def rectangle_area(width, height):
    return width * height


print(rectangle_area(4, 3))
```

Output:

```text
12
```

## 4. `try` and `except`

Put only the operation that may fail inside `try`. Catch the specific expected exception.

```python
raw_age = "twenty"

try:
    age = int(raw_age)
except ValueError:
    print("age must be an integer")
```

Output:

```text
age must be an integer
```

The handler runs because `int()` cannot parse the text.

## 5. Accessing the Exception

`except ... as error` gives access to the exception object.

```python
try:
    int("abc")
except ValueError as error:
    print(type(error).__name__)
    print(str(error))
```

Output:

```text
ValueError
invalid literal for int() with base 10: 'abc'
```

The type identifies the category. The message explains this failure.

## 6. Multiple Expected Exceptions

Use separate handlers when failures need different responses.

```python
values = {"count": "zero"}

try:
    result = 10 / int(values["count"])
except KeyError:
    print("count is missing")
except ValueError:
    print("count is not an integer")
except ZeroDivisionError:
    print("count cannot be zero")
```

Output:

```text
count is not an integer
```

Python uses the first matching handler.

Use a tuple when several exceptions have the same response:

```python
try:
    value = int(None)
except (TypeError, ValueError) as error:
    print(type(error).__name__)
```

Output:

```text
TypeError
```

## 7. `else`

`else` runs only when `try` finishes without an exception.

```python
try:
    number = int("25")
except ValueError:
    print("invalid")
else:
    print(number * 2)
```

Output:

```text
50
```

Keep success-only code in `else` so the `try` block stays narrow.

## 8. `finally`

`finally` runs whether the operation succeeds or fails.

```python
try:
    print("work")
    raise ValueError("invalid")
except ValueError:
    print("handled")
finally:
    print("cleanup")
```

Output:

```text
work
handled
cleanup
```

Use `finally` for required cleanup. Avoid `return` inside it because that can hide an exception.

## 9. Raising an Exception

`raise` stops normal flow and reports invalid state.

```python
def set_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age


try:
    print(set_age(-1))
except ValueError as error:
    print(error)
```

Output:

```text
age cannot be negative
```

Fail as soon as an invalid value is known.

## 10. Re-Raising

Bare `raise` sends the current exception upward without replacing its traceback.

```python
def parse_count(raw_count):
    try:
        return int(raw_count)
    except ValueError:
        print("parse failed")
        raise


try:
    parse_count("many")
except ValueError as error:
    print(type(error).__name__)
```

Output:

```text
parse failed
ValueError
```

Re-raise when the current layer cannot fully handle the failure.

## 11. Exception Chaining

`raise NewError(...) from error` adds useful context while preserving the cause.

```python
def load_port(raw_port):
    try:
        return int(raw_port)
    except ValueError as error:
        raise ValueError("port must be numeric") from error


try:
    load_port("http")
except ValueError as error:
    print(error)
    print(type(error.__cause__).__name__)
```

Output:

```text
port must be numeric
ValueError
```

The new message explains the domain, and `__cause__` keeps the original failure.

## 12. Custom Exceptions

Create a custom exception when callers need to distinguish a domain failure.

```python
class InsufficientBalanceError(Exception):
    pass


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError("insufficient balance")
    return balance - amount


try:
    withdraw(100, 150)
except InsufficientBalanceError as error:
    print(type(error).__name__)
    print(error)
```

Output:

```text
InsufficientBalanceError
insufficient balance
```

Inherit directly from `Exception` unless a more specific parent is meaningful.

## 13. Exception Hierarchy

A handler catches its exception type and subclasses.

```python
error = ValueError("invalid")

print(isinstance(error, ValueError))
print(isinstance(error, Exception))
print(isinstance(error, BaseException))
```

Output:

```text
True
True
True
```

Catch specific exceptions before broad parent exceptions.

Do not normally catch `BaseException`; it includes `KeyboardInterrupt` and `SystemExit`.

## 14. Common Python Errors

### `NameError`

A name does not exist in the visible scopes.

```python
try:
    print(missing_name)
except NameError as error:
    print(type(error).__name__)
```

Output:

```text
NameError
```

### `TypeError`

An operation received an unsupported type or argument shape.

```python
try:
    print("age: " + 25)
except TypeError as error:
    print(type(error).__name__)
```

Output:

```text
TypeError
```

### `ValueError`

The type is acceptable, but the value is invalid.

```python
try:
    print(int("two"))
except ValueError as error:
    print(type(error).__name__)
```

Output:

```text
ValueError
```

### `IndexError`

A sequence index is outside its valid range.

```python
try:
    print([10, 20][5])
except IndexError as error:
    print(type(error).__name__)
```

Output:

```text
IndexError
```

### `KeyError`

A dictionary key does not exist.

```python
try:
    print({"name": "Ana"}["age"])
except KeyError as error:
    print(type(error).__name__)
```

Output:

```text
KeyError
```

### `AttributeError`

An object does not provide the requested attribute.

```python
try:
    print("Python".append("!"))
except AttributeError as error:
    print(type(error).__name__)
```

Output:

```text
AttributeError
```

### `FileNotFoundError`

A requested path does not exist.

```python
from pathlib import Path

missing_path = Path("file_that_does_not_exist_12345.txt")

try:
    missing_path.read_text(encoding="utf-8")
except FileNotFoundError as error:
    print(type(error).__name__)
```

Output:

```text
FileNotFoundError
```

### `ModuleNotFoundError`

Python cannot find the imported module.

```python
try:
    import module_that_does_not_exist_12345
except ModuleNotFoundError as error:
    print(type(error).__name__)
```

Output:

```text
ModuleNotFoundError
```

## 15. Assertions

`assert` checks internal assumptions during development.

```python
def percentage(part, whole):
    assert whole != 0, "whole must not be zero"
    return part / whole * 100


try:
    percentage(5, 0)
except AssertionError as error:
    print(error)
```

Output:

```text
whole must not be zero
```

Do not use `assert` for user input, security checks, or required runtime validation. Assertions can be disabled with optimization.

## 16. Reading a Traceback

Read a traceback from the last frame upward:

1. read the exception type and message at the bottom;
2. inspect the final file and line in your code;
3. move upward to understand how execution reached it.

Use small diagnostic prints to expose type, value, and path.

```python
raw_count = "many"

print("raw_count:", repr(raw_count))
print("type:", type(raw_count).__name__)

try:
    int(raw_count)
except ValueError as error:
    print("error:", type(error).__name__)
```

Output:

```text
raw_count: 'many'
type: str
error: ValueError
```

Remove temporary diagnostic prints after fixing the issue; use structured logging in production.

## 17. `breakpoint()` and `pdb`

`breakpoint()` pauses execution in an interactive debugger.

```python
def calculate_total(price, quantity):
    total = price * quantity
    print(total)
    return total


calculate_total(10, 3)
```

Output:

```text
30
```

Place `breakpoint()` before `print(total)` while debugging, then use:

| Command | Action |
| --- | --- |
| `p expression` | print an expression |
| `n` | run next line |
| `s` | step into a call |
| `c` | continue execution |
| `q` | quit debugger |

Remove the breakpoint before committing production code.

## 18. Command Execution Errors

External commands report success with exit code `0` and failure with a non-zero code.

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "raise SystemExit(2)"],
    check=False,
)

print(result.returncode)
```

Output:

```text
2
```

Use an argument list, not a shell-built string, when command input contains data.

### Fail Fast with `check=True`

`check=True` raises `CalledProcessError` for a non-zero exit code.

```python
import subprocess
import sys

try:
    subprocess.run(
        [sys.executable, "-c", "raise SystemExit(2)"],
        check=True,
    )
except subprocess.CalledProcessError as error:
    print(type(error).__name__)
    print(error.returncode)
```

Output:

```text
CalledProcessError
2
```

Do not ignore a failed command unless the failure is an expected, handled outcome.

## 19. Avoid Broad Exception Handling

This is too broad:

```python
try:
    value = int("abc")
except Exception:
    print("something failed")
```

Output:

```text
something failed
```

It hides the actual category. Catch what the code expects:

```python
try:
    value = int("abc")
except ValueError:
    print("value must be an integer")
```

Output:

```text
value must be an integer
```

## 20. Final Mental Model

When an error occurs, ask:

1. Is it syntax, runtime, or logic?
2. What exact exception type was raised?
3. Which line raised it?
4. Is this layer able to recover meaningfully?
5. Should the error propagate, be translated, or be handled?
6. Is required cleanup guaranteed?

| Tool | Use |
| --- | --- |
| `raise` | report invalid state |
| `except SpecificError` | handle an expected failure |
| `else` | run success-only code |
| `finally` | guarantee cleanup |
| bare `raise` | preserve and re-raise current error |
| `raise ... from ...` | translate while preserving cause |
| `breakpoint()` | inspect live state interactively |
| `subprocess.run(..., check=True)` | fail on command errors |
