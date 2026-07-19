# Exceptions and Error Handling Mastery

## 1) Error Handling Philosophy

Use exceptions to separate normal flow from failure flow.

Good design:
- validate early
- raise specific errors
- preserve context
- handle close to boundaries (CLI/API/DB/network/file)

## 2) Built-in Exception Families

Common families:
- `ValueError`, `TypeError`, `KeyError`, `IndexError`
- `FileNotFoundError`, `PermissionError`
- `TimeoutError`, `ConnectionError`
- `RuntimeError` for state violations when no better specific type exists

## 3) Specific Catching and Context Preservation

```python
def parse_price(raw: str) -> float:
    try:
        value = float(raw)
    except ValueError as error:
        raise ValueError("price must be numeric") from error
    if value < 0:
        raise ValueError("price cannot be negative")
    return value
```

Avoid:
- bare `except:`
- swallowing exceptions with `pass`

## 4) Custom Domain Exceptions

```python
class PaymentDeclinedError(Exception):
    pass


def charge(amount: float) -> None:
    if amount > 1000:
        raise PaymentDeclinedError("limit exceeded")
```

Benefits:
- business failures are catchable separately from infrastructure failures.

## 5) Retry Policy Patterns

Retry only retryable exceptions and cap attempts.

```python
import time


def retry(op, attempts=3, base_delay=0.2):
    last = None
    for i in range(attempts):
        try:
            return op()
        except TimeoutError as error:
            last = error
            if i < attempts - 1:
                time.sleep(base_delay * (2 ** i))
    raise RuntimeError("operation failed after retries") from last
```

## 6) Exception Safety with `finally`

`finally` is for cleanup, not business returns.

Pitfall:
- `return` inside `finally` can suppress original exceptions.

## 7) Error Taxonomy Template for Projects

1. Validation errors (caller input problems)
2. Domain errors (business rule failures)
3. Infrastructure errors (I/O, DB, network, external APIs)

This helps mapping to:
- HTTP status codes
- retry policies
- logging and alerting severity

## 8) Logging Errors Correctly

- log contextual ids (`request_id`, `user_id`, `job_id`)
- preserve stack traces for unexpected failures
- avoid logging secrets

## 9) Interview Questions You Must Handle

1. Difference between `raise`, `raise from`, and re-raising.
2. Why catching broad exceptions is dangerous.
3. When to convert low-level errors to domain-level errors.
4. Why exceptions should not drive normal hot-path branching.

## 10) Production Checklist

1. Catch only expected exceptions.
2. Re-raise with context where useful.
3. Retry only safe retryable operations.
4. Ensure cleanup paths run on error.
5. Test failure paths, not only success paths.
