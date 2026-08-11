# PYTHON - FUNCTIONS

A function gives a name to reusable behavior.

## 1. Define and Call a Function

`def` creates a function object. The body runs only when the function is called.

```python
def greet():
    print("Hello")


print(type(greet).__name__)
greet()
```

Output:

```text
function
Hello
```

Why?

- `def` creates the function.
- `greet()` executes its body.

## 2. Parameters and Arguments

A parameter is a name in the function definition. An argument is the value passed during a call.

```python
def greet(name):
    print(f"Hello, {name}")


greet("Ravi")
```

Output:

```text
Hello, Ravi
```

`name` is the parameter. `"Ravi"` is the argument.

## 3. Return Values

`return` ends the function and sends a value to the caller.

```python
def add(left, right):
    return left + right


result = add(4, 6)
print(result)
```

Output:

```text
10
```

Code after `return` in the same path does not run.

## 4. Implicit `None`

A function with no `return` statement returns `None`.

```python
def show_message():
    print("running")


result = show_message()
print(result)
```

Output:

```text
running
None
```

## 5. Returning Multiple Values

Comma-separated return values are packed into a tuple.

```python
def divide_with_remainder(number, divisor):
    return number // divisor, number % divisor


result = divide_with_remainder(17, 5)
quotient, remainder = result

print(result)
print(quotient, remainder)
```

Output:

```text
(3, 2)
3 2
```

## 6. Positional and Keyword Arguments

Positional arguments use order. Keyword arguments use parameter names.

```python
def describe(name, role):
    print(name, role)


describe("Ana", "Developer")
describe(role="Designer", name="Mia")
```

Output:

```text
Ana Developer
Mia Designer
```

Keyword arguments make meaning explicit and can be reordered.

## 7. Default Arguments

A default is used when the caller omits that argument.

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}")


greet("Ana")
greet("Ravi", "Welcome")
```

Output:

```text
Hello, Ana
Welcome, Ravi
```

Required parameters must come before default parameters.

## 8. Mutable Default Trap

Defaults are evaluated once when `def` runs, not once per call.

```python
def add_item(item, items=[]):
    items.append(item)
    return items


print(add_item("A"))
print(add_item("B"))
```

Output:

```text
['A']
['A', 'B']
```

Both calls reuse the same list.

Use `None` when each call needs a new mutable object:

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item("A"))
print(add_item("B"))
```

Output:

```text
['A']
['B']
```

## 9. Positional-Only Parameters

Parameters before `/` cannot be passed by keyword.

```python
def divide(numerator, denominator, /):
    return numerator / denominator


print(divide(10, 2))
```

Output:

```text
5.0
```

This protects parameter names from becoming part of the public API.

## 10. Keyword-Only Parameters

Parameters after `*` must be passed by name.

```python
def connect(host, *, timeout=5):
    print(host, timeout)


connect("example.com", timeout=10)
```

Output:

```text
example.com 10
```

This makes important options clear at the call site.

## 11. Variable Positional Arguments: `*args`

`*args` collects extra positional arguments into a tuple.

```python
def total(*numbers):
    print(type(numbers).__name__)
    return sum(numbers)


print(total(2, 3, 5))
```

Output:

```text
tuple
10
```

`args` is only a convention; the `*` creates the behavior.

## 12. Variable Keyword Arguments: `**kwargs`

`**kwargs` collects extra keyword arguments into a dictionary.

```python
def show_profile(**details):
    print(type(details).__name__)
    print(details["name"], details["role"])


show_profile(name="Ana", role="Developer")
```

Output:

```text
dict
Ana Developer
```

`kwargs` is a convention; `**` creates the behavior.

## 13. Argument Unpacking

`*` unpacks positional values. `**` unpacks keyword values.

```python
def introduce(name, role):
    print(f"{name}: {role}")


person = ["Mia", "Designer"]
details = {"name": "Ravi", "role": "Tester"}

introduce(*person)
introduce(**details)
```

Output:

```text
Mia: Designer
Ravi: Tester
```

## 14. How Arguments Are Passed

Python binds a parameter to the same object passed by the caller.

### Mutation Is Visible

Mutating a shared object changes what the caller sees.

```python
def add_score(scores):
    scores.append(100)


results = [80, 90]
add_score(results)
print(results)
```

Output:

```text
[80, 90, 100]
```

### Rebinding Is Local

Assigning a new object to the parameter changes only the local name.

```python
def replace_scores(scores):
    scores = [100]
    print("inside", scores)


results = [80, 90]
replace_scores(results)
print("outside", results)
```

Output:

```text
inside [100]
outside [80, 90]
```

## 15. Scope: LEGB Rule

Python searches for a name in this order:

1. Local: current function.
2. Enclosing: outer function.
3. Global: current module.
4. Built-in: names such as `len` and `print`.

```python
label = "global"


def outer():
    label = "enclosing"

    def inner():
        label = "local"
        print(label)

    inner()
    print(label)


outer()
print(label)
```

Output:

```text
local
enclosing
global
```

Each assignment creates or updates a name in its own scope.

## 16. Local Scope

A name assigned inside a function is local by default.

```python
message = "outside"


def show():
    message = "inside"
    print(message)


show()
print(message)
```

Output:

```text
inside
outside
```

The local name shadows the global name; it does not replace it.

## 17. `global`

`global` makes assignment target a module-level name.

```python
count = 0


def increment():
    global count
    count += 1


increment()
print(count)
```

Output:

```text
1
```

Use global mutation sparingly because it creates hidden shared state.

## 18. `nonlocal`

`nonlocal` makes assignment target the nearest enclosing function scope.

```python
def make_counter():
    count = 0

    def increment():
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

The inner function keeps access to `count` after `make_counter()` finishes.

## 19. Unbound Local Error

If a function assigns to a name, Python treats that name as local throughout the function.

```python
count = 10


def show_error():
    try:
        print(count)
        count = 20
    except UnboundLocalError as error:
        print(type(error).__name__)


show_error()
```

Output:

```text
UnboundLocalError
```

The assignment makes `count` local, but it is read before receiving a local value.

## 20. Functions Are Objects

A function can be stored in another name or collection.

```python
def double(number):
    return number * 2


operation = double
print(operation(6))
print(operation is double)
```

Output:

```text
12
True
```

No parentheses means the function object itself. Parentheses call it.

## 21. Higher-Order Functions

A higher-order function accepts or returns another function.

```python
def apply(operation, value):
    return operation(value)


def square(number):
    return number**2


print(apply(square, 5))
```

Output:

```text
25
```

## 22. Lambda Functions

`lambda` creates a small anonymous function containing one expression.

```python
numbers = [3, 1, 2]
descending = sorted(numbers, key=lambda number: -number)

print(descending)
```

Output:

```text
[3, 2, 1]
```

Use `def` when logic needs a name, multiple statements, or documentation.

## 23. Closures

A closure is an inner function that remembers names from an enclosing scope.

```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor

    return multiply


triple = make_multiplier(3)
print(triple(4))
```

Output:

```text
12
```

`triple` retains access to `factor`.

### Late Binding Trap

Closures look up captured names when called.

```python
functions = []

for number in range(3):
    functions.append(lambda: number)

print([function() for function in functions])
```

Output:

```text
[2, 2, 2]
```

All lambdas read the final value of `number`.

Capture the current value with a default:

```python
functions = []

for number in range(3):
    functions.append(lambda number=number: number)

print([function() for function in functions])
```

Output:

```text
[0, 1, 2]
```

## 24. Recursion

Recursion occurs when a function calls itself.

A recursive function needs:

- a base case that stops recursion;
- a recursive case that moves toward the base case.

```python
def factorial(number):
    if number == 0:
        return 1
    return number * factorial(number - 1)


print(factorial(5))
```

Output:

```text
120
```

Call flow:

```text
factorial(5)
5 * factorial(4)
5 * 4 * factorial(3)
5 * 4 * 3 * factorial(2)
5 * 4 * 3 * 2 * factorial(1)
5 * 4 * 3 * 2 * 1 * factorial(0)
```

### Missing Base Case

Recursion without a reachable base case eventually raises `RecursionError`.

```python
def repeat():
    return repeat()


try:
    repeat()
except RecursionError as error:
    print(type(error).__name__)
```

Output:

```text
RecursionError
```

Prefer a loop when recursion does not make the problem clearer. Python does not optimize tail recursion.

## 25. Type Hints

Type hints document expected types and support static analysis. Python does not enforce them at runtime.

```python
def add(left: int, right: int) -> int:
    return left + right


print(add(2, 3))
print(add("Py", "thon"))
```

Output:

```text
5
Python
```

Runtime validation is separate from type hints.

## 26. Docstrings

A docstring explains a function's public purpose and contract.

```python
def area(width, height):
    """Return the area of a rectangle."""
    return width * height


print(area.__doc__)
```

Output:

```text
Return the area of a rectangle.
```

## 27. Pure Functions and Side Effects

A pure function depends only on inputs and does not change external state.

```python
def doubled(numbers):
    return [number * 2 for number in numbers]


original = [1, 2, 3]
result = doubled(original)

print(original)
print(result)
```

Output:

```text
[1, 2, 3]
[2, 4, 6]
```

Pure functions are easier to test. Side effects are sometimes necessary, but should be explicit.

## 28. Final Mental Model

When reading a function, ask:

1. What arguments bind to which parameters?
2. Which objects are shared with the caller?
3. Does the function mutate an object or rebind a local name?
4. Where does each name resolve under LEGB?
5. Is a default object reused?
6. Does a closure use late binding?
7. Does recursion have a reachable base case?
8. What value is returned, or is `None` returned implicitly?

| Concept | Rule |
| --- | --- |
| Call | creates a new local frame |
| Parameter | local name bound to an argument object |
| `return` | ends the call and sends a value back |
| Mutable default | reused across calls |
| `global` | rebinds a module name |
| `nonlocal` | rebinds an enclosing name |
| Closure | retains access to enclosing names |
| Recursion | self-call with a base case |
