# PYTHON - CONTROL FLOW

Control flow decides which statement runs next.

## 1. Truthiness

Conditions convert values to `bool`.

Falsy values include `False`, `None`, numeric zero, and empty collections.

```python
values = [0, 1, "", "Python", [], [10], None]

for value in values:
    print(repr(value), bool(value))
```

Output:

```text
0 False
1 True
'' False
'Python' True
[] False
[10] True
None False
```

Why?

- Empty or zero-like values are falsy.
- Non-empty collections and non-zero numbers are truthy.

## 2. `if`, `elif`, and `else`

Python checks branches from top to bottom and runs the first true branch.

```python
score = 72

if score >= 90:
    grade = "A"
elif score >= 60:
    grade = "Pass"
else:
    grade = "Fail"

print(grade)
```

Output:

```text
Pass
```

Why?

- `score >= 90` is false.
- `score >= 60` is true, so later branches are skipped.

## 3. Nested Conditions

An `if` can contain another `if`. Keep nesting shallow when possible.

```python
age = 22
has_ticket = True

if age >= 18:
    if has_ticket:
        print("entry allowed")
```

Output:

```text
entry allowed
```

Why?

- Both conditions are true.

Prefer one clear condition when the checks belong together:

```python
age = 22
has_ticket = True

if age >= 18 and has_ticket:
    print("entry allowed")
```

Output:

```text
entry allowed
```

## 4. Conditional Expression

A conditional expression chooses one of two values.

```python
temperature = 31
label = "hot" if temperature > 30 else "comfortable"

print(label)
```

Output:

```text
hot
```

Use it for a small value choice, not complex branching.

## 5. Comparison Chaining

Python can combine ordered comparisons without repeating the middle value.

```python
age = 25

print(18 <= age < 60)
print(age >= 18 and age < 60)
```

Output:

```text
True
True
```

Both conditions mean the same thing.

## 6. Boolean Operators

Precedence is `not`, then `and`, then `or`.

```python
is_admin = False
is_active = True

print(is_admin or is_active and not is_admin)
```

Output:

```text
True
```

Why?

- Python evaluates `not is_admin` first.
- It then evaluates `and`, followed by `or`.

Use parentheses when the intended grouping is not obvious.

## 7. Short-Circuit Evaluation

`and` stops at the first falsy operand. `or` stops at the first truthy operand.

```python
def check() -> bool:
    print("check called")
    return True


print(False and check())
print(True or check())
```

Output:

```text
False
True
```

Why?

- `check()` is never called.
- The left operands already decide both results.

`and` and `or` return operands, not always `bool` values.

```python
print("" or "default")
print("Python" and 42)
```

Output:

```text
default
42
```

## 8. `for` Loop

A `for` loop takes one item at a time from an iterable.

```python
for language in ["Python", "Go", "Rust"]:
    print(language)
```

Output:

```text
Python
Go
Rust
```

## 9. `range()`

`range(start, stop, step)` generates integers. `stop` is excluded.

```python
for number in range(2, 7, 2):
    print(number)
```

Output:

```text
2
4
6
```

## 10. `enumerate()`

`enumerate()` provides each item with its index.

```python
languages = ["Python", "Go"]

for index, language in enumerate(languages, start=1):
    print(index, language)
```

Output:

```text
1 Python
2 Go
```

Prefer it to manually updating an index variable.

## 11. `zip()`

`zip()` iterates over multiple iterables together and stops at the shortest.

```python
names = ["Ana", "Ravi", "Mia"]
scores = [90, 85]

for name, score in zip(names, scores):
    print(name, score)
```

Output:

```text
Ana 90
Ravi 85
```

`Mia` has no matching score, so it is not produced.

## 12. `while` Loop

A `while` loop repeats while its condition remains true.

```python
count = 3

while count > 0:
    print(count)
    count -= 1
```

Output:

```text
3
2
1
```

The loop must eventually change something that makes the condition false.

## 13. `break`

`break` exits the nearest loop immediately.

```python
for number in range(1, 6):
    if number == 3:
        break
    print(number)

print("finished")
```

Output:

```text
1
2
finished
```

## 14. `continue`

`continue` skips the rest of the current iteration.

```python
for number in range(1, 6):
    if number % 2 == 0:
        continue
    print(number)
```

Output:

```text
1
3
5
```

## 15. `pass`

`pass` does nothing. It is a placeholder where syntax requires a statement.

```python
status = "pending"

if status == "pending":
    pass

print("program continues")
```

Output:

```text
program continues
```

## 16. Loop `else`

Loop `else` runs only when the loop finishes without `break`.

```python
numbers = [1, 3, 5]

for number in numbers:
    if number % 2 == 0:
        print("even found")
        break
else:
    print("no even number")
```

Output:

```text
no even number
```

`continue` does not prevent the `else`; only `break` does.

## 17. Nested Loops

The inner loop completes for every outer-loop iteration.

```python
for row in range(1, 3):
    for column in range(1, 3):
        print(row, column)
```

Output:

```text
1 1
1 2
2 1
2 2
```

`break` affects only the nearest loop.

## 18. `match` and `case`

`match` checks patterns from top to bottom. The first match wins.

```python
status_code = 404

match status_code:
    case 200:
        message = "success"
    case 400 | 404:
        message = "client error"
    case _:
        message = "unknown"

print(message)
```

Output:

```text
client error
```

`case _` is the fallback pattern.

### Pattern Guard

A guard adds a condition to a matched pattern.

```python
point = (4, 0)

match point:
    case (x, 0) if x > 0:
        print("positive x-axis")
    case (0, y):
        print("y-axis")
    case _:
        print("other")
```

Output:

```text
positive x-axis
```

## 19. `any()` and `all()`

`any()` needs at least one truthy value. `all()` needs every value to be truthy.

```python
checks = [True, True, False]

print(any(checks))
print(all(checks))
print(any([]))
print(all([]))
```

Output:

```text
True
False
False
True
```

Both functions short-circuit.

## 20. Final Mental Model

When reading control flow, ask:

1. What condition is evaluated first?
2. Which branch is the first match?
3. Does short-circuiting skip an expression?
4. What changes on each loop iteration?
5. Does `break`, `continue`, or `return` alter the path?
6. Did a loop finish normally or through `break`?

| Tool | Meaning |
| --- | --- |
| `if` / `elif` / `else` | choose a branch |
| `for` | iterate over items |
| `while` | repeat while true |
| `break` | exit nearest loop |
| `continue` | skip current iteration |
| loop `else` | run when no `break` occurs |
| `match` | choose by pattern |
| `any` / `all` | combine truth checks |
