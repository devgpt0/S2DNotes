# Synchronous Programming in Python

## 1. What "Synchronous" Means

Synchronous execution means:
- statements run one after another
- next step starts after current step finishes
- caller waits for callee

Simple model:
```text
Task A -> complete -> Task B -> complete -> Task C
```

---

## 2. Why We Start With Sync First

Even when systems use async or threads, core business logic is still mostly synchronous.

Interview point:
- strong synchronous design is required before concurrency
- bad sync code becomes bad async code faster

---

## 3. Basic Example

```python
import time


def fetch_user():
    print("Fetching user...")
    time.sleep(2)
    print("User fetched")


def fetch_orders():
    print("Fetching orders...")
    time.sleep(2)
    print("Orders fetched")


def main():
    start = time.perf_counter()
    fetch_user()
    fetch_orders()
    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
```

Expected output:
```text
Fetching user...
User fetched
Fetching orders...
Orders fetched
Total time: 4.00s
```

---

## 4. Blocking Calls (Interview Favorite)

A blocking call pauses progress of the current thread until completion.

Common blocking operations:
- `time.sleep`
- file I/O
- DB/network I/O
- heavy CPU loops

If interviewer asks "why slow?", often answer is "blocking happened in critical path."

---

## 5. Call Stack and Control Flow

In sync code:
- function call pushes frame
- function returns pops frame
- control returns to caller

Why interviewers care:
- helps explain recursion errors
- helps explain why exceptions bubble up
- helps explain why one slow call delays whole request path

---

## 6. CPU-bound vs I/O-bound in Sync Design

### CPU-bound
Mostly time spent in computation.
Examples:
- large numeric loops
- image transforms
- encoding/compression

### I/O-bound
Mostly waiting for external systems.
Examples:
- HTTP requests
- DB calls
- disk/network reads

Sync handles both, but I/O-heavy sync programs often waste time waiting.

---

## 7. Error Handling in Sync Code

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b


def main():
    try:
        print(divide(10, 2))
        print(divide(10, 0))
    except ValueError as exc:
        print(f"Validation error: {exc}")


if __name__ == "__main__":
    main()
```

Expected output:
```text
5.0
Validation error: b cannot be zero
```

Interview tip:
- raise early with clear message
- catch at boundary layers (API/UI/job runner)

---

## 8. Timeouts and Retries in Sync Systems

Pure sync code can still be production-safe with:
- request timeout
- bounded retries
- backoff

Example with `requests` (if installed):
```python
import requests


def fetch_json(url: str) -> dict:
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    return response.json()
```

Interview trap:
- no timeout means potential indefinite hang

---

## 9. Clean Code Rules for Sync Functions

1. Keep each function single-purpose.
2. Separate pure logic from I/O side effects.
3. Keep boundaries explicit (parse -> validate -> execute -> format).
4. Use dependency injection for clients (DB/HTTP) in testable services.
5. Log at boundaries, not every line.

---

## 10. Refactoring Example: Bad to Better Sync Design

Bad:
```python
def checkout(cart, db, payment_gateway, email_client):
    # validation, inventory, payment, db writes, notification all mixed
    ...
```

Better:
```python
def validate_cart(cart):
    ...


def reserve_inventory(cart, inventory_repo):
    ...


def charge_payment(cart, payment_service):
    ...


def complete_checkout(cart, services):
    validate_cart(cart)
    reserve_inventory(cart, services.inventory_repo)
    charge_payment(cart, services.payment_service)
```

Interview value:
- cleaner sync architecture makes async/thread migration easier later.

---

## 11. Performance Measurement Basics

Use `time.perf_counter()` for elapsed duration:

```python
import time

start = time.perf_counter()
# run work
elapsed = time.perf_counter() - start
print(f"{elapsed:.4f}s")
```

Do not rely on rough guesses in interview answers.  
Mention measurement first, optimization second.

---

## 12. Common Sync Interview Questions

1. Why is synchronous code easier to reason about?
2. What is blocking I/O?
3. How do you avoid hanging calls?
4. How do you structure sync code for later async migration?
5. Where should retries live and where should they not?

Short answers:
- deterministic flow
- one line waits on next
- always use timeouts
- isolate side effects
- retries near unstable boundary, not deep everywhere

---

## 13. Common Beginner Mistakes

1. Doing network call without timeout.
2. Mixing validation + persistence + rendering in one function.
3. Swallowing exceptions with empty `except`.
4. Prematurely adding threads/async before fixing sync design.
5. Not writing small tests for business logic.

---

## 14. One-Page Summary

- Sync code executes one step at a time.
- Blocking operations pause progress.
- Great sync design is foundation for any concurrency model.
- Timeouts, retries, and clear layers are key production habits.
- Interviewers care more about tradeoffs than syntax memorization.

---

## 15. Practice Assignment

Build a sync weather service module:
- `get_city_weather(city)`
- add request timeout and error handling
- parse and validate API response
- expose `format_weather_summary(data)`
- write 3 tests: success, timeout, bad response

