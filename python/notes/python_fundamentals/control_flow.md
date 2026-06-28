# PYTHON - CONTROL FLOW

## 1. Core Mental Model

Control flow questions ask one thing: which statement runs next and why.

Simulate in this order:
1. Condition truth value
2. Branch or loop path
3. Jump statements (break, continue, return, raise)
4. Exception handling and finally guarantees

## 2. if/elif/else and Boolean Precedence

Operator precedence reminder:
- not > and > or

This explains tricky conditions like:
- a or b and not a

Use parentheses in real code when intent is not obvious.

## 3. Short-Circuit Behavior

Python short-circuits boolean expressions:
- and stops on first falsy value
- or stops on first truthy value

This affects:
- Safety (avoid divide-by-zero)
- Side effects in expressions

## 4. pass, break, continue

- pass: do nothing placeholder.
- break: exits nearest loop immediately.
- continue: skips to next loop iteration.

In nested loops, break/continue only affect the current loop unless you restructure logic.

## 5. for and while Execution Model

for loop:
- Iterates over iterable items.

while loop:
- Repeats while condition is true.
- Better when iteration count is not known upfront.

Common trap:
- Mutating a list while iterating over it can create surprising behavior.

## 6. Loop else Clause

Python loop else runs only if loop ends normally (no break).

Applies to both for and while.

- break prevents else.
- continue does not prevent else by itself.

## 7. Walrus Operator (:=)

Walrus assigns and returns value in expression context.

Useful in if/while when you need value and condition together.

Be careful with readability; overuse makes flow harder to follow.

## 8. Nested Loops and Early Exit Patterns

Without labels, Python common options for outer-loop exit:
- Flag variable
- Helper function with return
- Exception-based control (rare, usually avoid)

Understand inner break + outer else interactions for interview puzzles.

## 9. try/except/finally in Flow Control

- except handles matching exceptions.
- finally always executes before leaving try block.

In loops, finally still runs on continue/break/exception paths.

If finally changes state each iteration, it can affect loop termination.

## 10. match/case (Python 3.10+)

Structural pattern matching provides branch logic by shape/pattern.

Rules to remember:
- Cases checked top to bottom.
- First matching case wins.
- case _ is default wildcard.
- Guard (if condition) refines a match.

## 11. any/all and Truth Aggregation

- any(iterable): True if at least one truthy element.
- all(iterable): True only if all elements truthy.

Common combined condition:
- any(x) and all(x)

Evaluate carefully because first condition can short-circuit second.

## 12. Control Flow Quality Patterns

Good practice:
- Prefer clear guard clauses over deep nesting.
- Avoid magic values in conditions.
- Use clear loop boundaries and explicit intent.
- Avoid exceptions for normal expected branches in hot paths.
- Choose for vs while by problem shape, not habit.

## 13. Interview Solve Template

For any control-flow snippet:
1. Write initial values.
2. Evaluate each condition with precedence.
3. Trace iteration by iteration.
4. Mark where break/continue/return/raise happens.
5. Apply loop-else rule (did break occur?).
6. Apply try/except/finally effects before next step.
7. For match/case, test patterns in order.

## 14. Worksheet Concept Coverage Checklist

- if/elif/else path selection
- Boolean precedence with not/and/or
- continue and break behavior
- pass semantics
- while loop break patterns
- Nested loop break effects
- Loop else execution rules
- Walrus operator in if/while
- Mutation during iteration
- try/except/finally flow interactions
- match/case and guards
- any/all based branching
- Code-quality control-flow refactors

## 15. Exception Hierarchy and Re-raise Patterns (Critical Missing Concept)

Good exception handling is part of control flow design.

Core rules:
- Catch specific exceptions, not broad `except Exception` in business logic.
- Add context when re-raising using `raise ... from error`.
- Keep exception boundaries near I/O edges (API, file, DB, network).

```python
def load_user_age(raw: str) -> int:
    try:
        age = int(raw)
    except ValueError as error:
        raise ValueError("age must be integer text") from error

    if age < 0:
        raise ValueError("age cannot be negative")
    return age
```

Interview point:
- exceptions should represent exceptional paths, not regular branching in hot loops.

## 16. Context Manager Control Flow (`with`) and Cleanup Guarantees

`with` is structured control flow for resource safety.

```python
def first_line(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.readline().strip()
```

Why this matters:
- cleanup runs even when exceptions occur.
- avoids leak-prone manual `open()/close()` patterns.

Equivalent mental model:
- `with` internally behaves like `try/finally` for deterministic cleanup.

## 17. Iterator and Generator Flow Thinking

Generators are lazy control flow; values are produced on demand.

```python
def non_empty_lines(path: str):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                yield line
```

Benefits:
- memory-efficient for large files/streams.
- composes cleanly with `any`, `all`, `sum`, `list`.

## 18. Robust Retry Flow (Without Infinite Loops)

Production code often needs bounded retries with backoff.

```python
import time


def retry(operation, attempts: int = 3, delay: float = 0.2):
    last_error = None
    for i in range(attempts):
        try:
            return operation()
        except TimeoutError as error:
            last_error = error
            if i < attempts - 1:
                time.sleep(delay * (2 ** i))
    raise RuntimeError("operation failed after retries") from last_error
```

Checklist:
- bounded attempts
- explicit retryable exceptions
- backoff
- final propagated error

## 19. Critical Pitfalls Missing from Most Notes

- `return` inside `finally` suppresses original exception/return value.
- mutating collection while iterating can skip/duplicate processing.
- broad `except` can hide programming errors.
- `while True` without exit strategy creates reliability risk.

## 20. Interview Upgrade Template for Control Flow Answers

When explaining any flow-heavy code:
1. state branch rules and precedence.
2. trace normal path and exceptional path separately.
3. call out cleanup guarantees (`finally`/`with`).
4. mention failure policy (retry, timeout, fallback, fail-fast).
