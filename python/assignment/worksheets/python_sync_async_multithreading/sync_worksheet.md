# Worksheet: Synchronous Programming (Interview Level 3-5 Years)

Question mix:
- Print the Output: 20
- MCQ (Single Correct): 40
- MCQ (Multiple Correct): 40
- Total: 100

Coverage map:
- Sync execution model and blocking behavior
- Call stack, control flow, and error propagation
- CPU-bound vs I/O-bound decisions
- Timeout, retries, and backoff in sync systems
- Clean sync architecture and refactoring discipline
- Measurement, tradeoffs, and interview framing

---

## Section A: Print the Output (1-20)

1. What will be the output?
```python
import time

def fetch_user():
    print("user:start")
    time.sleep(0.01)
    print("user:end")

def fetch_orders():
    print("orders:start")
    time.sleep(0.01)
    print("orders:end")

fetch_user()
fetch_orders()
print("done")
```

2. Predict the output.
```python
def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b

try:
    print(divide(10, 2))
    print(divide(10, 0))
except ValueError as exc:
    print(f"error:{exc}")
```

3. What is printed?
```python
def service():
    try:
        print("try")
    finally:
        print("finally")

service()
```

4. What will be printed?
```python
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("no-break")
```

5. Predict the output.
```python
for i in range(3):
    if i == 10:
        break
    print(i)
else:
    print("no-break")
```

6. What is the output?
```python
i = 0
while i < 4:
    i += 1
    if i == 3:
        continue
    print(i)
```

7. Predict the call flow output.
```python
def c():
    print("C")

def b():
    print("B:start")
    c()
    print("B:end")

def a():
    print("A:start")
    b()
    print("A:end")

a()
```

8. What will be printed?
```python
def validate_age(age):
    if age < 18:
        return "blocked"
    return "allowed"

print(validate_age(16))
print(validate_age(21))
```

9. Predict the output.
```python
def fetch(timeout=3):
    print(f"timeout={timeout}")

fetch()
fetch(1)
```

10. What is printed?
```python
attempts = [False, False, True]
for idx, ok in enumerate(attempts, start=1):
    print(f"try-{idx}")
    if ok:
        print("success")
        break
```

11. Predict the output.
```python
def parse_user(data):
    if "id" not in data:
        raise KeyError("missing id")
    return data["id"]

try:
    print(parse_user({"id": 7}))
    print(parse_user({"name": "ria"}))
except KeyError as exc:
    print(exc)
```

12. What will be printed?
```python
settings = {"region": "IN"}
print(settings.get("timeout", 5))
print(settings.get("region", "US"))
```

13. Predict scope behavior.
```python
x = 10

def show():
    x = 20
    print(x)

show()
print(x)
```

14. What is printed?
```python
def subtotal(price, qty):
    return price * qty

def total_with_tax(price, qty, tax):
    return subtotal(price, qty) * (1 + tax)

print(total_with_tax(100, 2, 0.1))
```

15. Predict the output.
```python
base = 0.1
for i in range(1, 4):
    print(round(base * i, 2))
```

16. What will be printed?
```python
def process(amount):
    if amount <= 0:
        raise ValueError("bad amount")
    return f"ok:{amount}"

for amt in [50, -1]:
    try:
        print(process(amt))
    except ValueError as exc:
        print(f"failed:{exc}")
```

17. Predict the output.
```python
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

18. What is printed?
```python
nums = [1, 2, 3, 4]
out = [n * 2 for n in nums if n % 2 == 0]
print(out)
```

19. Predict the output (ignore actual duration value).
```python
import time

start = time.perf_counter()
value = sum(range(10))
elapsed = time.perf_counter() - start
print(value)
print(elapsed >= 0)
```

20. What will be printed?
```python
try:
    int("x")
except ValueError:
    print("value-error")
except Exception:
    print("generic-error")
```

---

## Section B: MCQ (Single Correct) (21-60)

21. Which statement is correct about sync execution model?
- A. Synchronous flow executes one step at a time, with caller waiting for callee.
- B. Synchronous programming always runs multiple operations at the same instant.
- C. Timeouts are unnecessary if code works on localhost.
- D. Retries should be infinite to guarantee success.

22. Which statement is correct about blocking behavior?
- A. Timeouts are unnecessary if code works on localhost.
- B. Clean code is only about making variable names shorter.
- C. Blocking operations in critical path can increase end-to-end latency.
- D. Blocking calls never impact latency in production.

23. Which statement is correct about call stack and control flow?
- A. Exceptions should usually be swallowed to keep systems stable.
- B. Good sync architecture is a strong base before introducing concurrency.
- C. All sync code should be converted to threads immediately.
- D. Clean code is only about making variable names shorter.

24. Which statement is correct about CPU-bound vs I/O-bound reasoning?
- A. Catching every exception in every helper is always best practice.
- B. All sync code should be converted to threads immediately.
- C. Measurement is optional; optimization should start from intuition only.
- D. time.sleep, file I/O, DB calls, and network calls are common blocking points.

25. Which statement is correct about timeouts and retries?
- A. Catching every exception in every helper is always best practice.
- B. In sync code, control returns to caller after callee finishes.
- C. CPU-bound and I/O-bound workloads are architecturally identical.
- D. Single long functions are easier to maintain than small cohesive ones.

26. Which statement is correct about error handling boundaries?
- A. Dependency injection makes testing harder and should be avoided.
- B. Boundary validation is unnecessary in production services.
- C. CPU-bound tasks spend most time in computation.
- D. CPU-bound and I/O-bound workloads are architecturally identical.

27. Which statement is correct about clean sync design?
- A. I/O-bound tasks spend most time waiting on external systems.
- B. Guard clauses always reduce readability.
- C. Dependency injection makes testing harder and should be avoided.
- D. Retries should be deep inside all utility functions.

28. Which statement is correct about refactoring strategy?
- A. Logging every line is always superior to boundary logging.
- B. Timeouts should be set at unstable boundaries to avoid indefinite hangs.
- C. One slow call cannot impact the full sync request path.
- D. Retries should be deep inside all utility functions.

29. Which statement is correct about measurement and optimization?
- A. Retries should be bounded and usually use backoff strategy.
- B. One slow call cannot impact the full sync request path.
- C. Sync code cannot be reliable in production.
- D. Call stack understanding is irrelevant for debugging.

30. Which statement is correct about interview tradeoff explanation?
- A. Call stack understanding is irrelevant for debugging.
- B. Catching errors at boundary layers is often cleaner than deep catches everywhere.
- C. Using no timeout is safer than using a small timeout.
- D. Tradeoff discussion is unnecessary in interviews.

31. Which statement is correct about sync execution model?
- A. Raising clear validation errors early improves maintainability.
- B. Pure functions are harder to test than side-effect-heavy functions.
- C. Using no timeout is safer than using a small timeout.
- D. Backoff should be random without any cap.

32. Which statement is correct about blocking behavior?
- A. Single-purpose functions generally improve readability and testability.
- B. Returning clear errors is worse than returning silent defaults.
- C. You should optimize first and measure later.
- D. Pure functions are harder to test than side-effect-heavy functions.

33. Which statement is correct about call stack and control flow?
- A. Layered design is overengineering for all sync services.
- B. Separating pure logic from I/O side effects improves design quality.
- C. Synchronous systems never need retries.
- D. You should optimize first and measure later.

34. Which statement is correct about CPU-bound vs I/O-bound reasoning?
- A. Validation should happen only at database level, never at service boundary.
- B. Synchronous systems never need retries.
- C. Readability has little impact on maintainability.
- D. Dependency injection can make sync services easier to test.

35. Which statement is correct about timeouts and retries?
- A. Code structure does not affect migration to async or threads.
- B. Readability has little impact on maintainability.
- C. Synchronous programming always runs multiple operations at the same instant.
- D. Measuring with perf_counter is better than relying on guesses.

36. Which statement is correct about error handling boundaries?
- A. Synchronous programming always runs multiple operations at the same instant.
- B. Retries should be infinite to guarantee success.
- C. Deterministic flow is one reason sync code is easier to reason about.
- D. Timeouts are unnecessary if code works on localhost.

37. Which statement is correct about clean sync design?
- A. Blocking calls never impact latency in production.
- B. Clean code is only about making variable names shorter.
- C. Timeouts are unnecessary if code works on localhost.
- D. One slow blocking call can delay the full request path in sync execution.

38. Which statement is correct about refactoring strategy?
- A. All sync code should be converted to threads immediately.
- B. Clean code is only about making variable names shorter.
- C. Retries belong near unstable dependencies, not in every helper.
- D. Exceptions should usually be swallowed to keep systems stable.

39. Which statement is correct about measurement and optimization?
- A. Measurement is optional; optimization should start from intuition only.
- B. Catching every exception in every helper is always best practice.
- C. Guard clauses can reduce deep nesting in sync code.
- D. All sync code should be converted to threads immediately.

40. Which statement is correct about interview tradeoff explanation?
- A. CPU-bound and I/O-bound workloads are architecturally identical.
- B. Catching every exception in every helper is always best practice.
- C. Single long functions are easier to maintain than small cohesive ones.
- D. Meaningful names reduce cognitive load in code reviews.

41. Which statement is correct about sync execution model?
- A. Boundary validation is unnecessary in production services.
- B. Dependency injection makes testing harder and should be avoided.
- C. Swallowing exceptions silently is usually a bad practice.
- D. CPU-bound and I/O-bound workloads are architecturally identical.

42. Which statement is correct about blocking behavior?
- A. Dependency injection makes testing harder and should be avoided.
- B. Guard clauses always reduce readability.
- C. Retries should be deep inside all utility functions.
- D. Clean sync boundaries make async/thread migration safer later.

43. Which statement is correct about call stack and control flow?
- A. Logging every line is always superior to boundary logging.
- B. Business rules should be explicit and not hidden in side effects.
- C. One slow call cannot impact the full sync request path.
- D. Retries should be deep inside all utility functions.

44. Which statement is correct about CPU-bound vs I/O-bound reasoning?
- A. One slow call cannot impact the full sync request path.
- B. Call stack understanding is irrelevant for debugging.
- C. Sync code cannot be reliable in production.
- D. Bounded retries with backoff are safer than infinite retries.

45. Which statement is correct about timeouts and retries?
- A. Sync systems still require reliability discipline (timeouts, retries, logging).
- B. Tradeoff discussion is unnecessary in interviews.
- C. Call stack understanding is irrelevant for debugging.
- D. Using no timeout is safer than using a small timeout.

46. Which statement is correct about error handling boundaries?
- A. Backoff should be random without any cap.
- B. Clear parse -> validate -> execute -> format stages improve maintainability.
- C. Pure functions are harder to test than side-effect-heavy functions.
- D. Using no timeout is safer than using a small timeout.

47. Which statement is correct about clean sync design?
- A. Pure functions are harder to test than side-effect-heavy functions.
- B. Returning clear errors is worse than returning silent defaults.
- C. You should optimize first and measure later.
- D. Not all workloads need concurrency; simple sync can be best for low scale.

48. Which statement is correct about refactoring strategy?
- A. Layered design is overengineering for all sync services.
- B. You should optimize first and measure later.
- C. Synchronous systems never need retries.
- D. Interviewers care about tradeoffs and correctness, not only syntax speed.

49. Which statement is correct about measurement and optimization?
- A. Readability has little impact on maintainability.
- B. Validation should happen only at database level, never at service boundary.
- C. Early returns for invalid data can improve readability.
- D. Synchronous systems never need retries.

50. Which statement is correct about interview tradeoff explanation?
- A. Synchronous programming always runs multiple operations at the same instant.
- B. Code structure does not affect migration to async or threads.
- C. Functions with fewer responsibilities are easier to evolve safely.
- D. Readability has little impact on maintainability.

51. Which statement is correct about sync execution model?
- A. Timeouts are unnecessary if code works on localhost.
- B. Performance tuning should come after correctness and measurement.
- C. Synchronous programming always runs multiple operations at the same instant.
- D. Retries should be infinite to guarantee success.

52. Which statement is correct about blocking behavior?
- A. Timeouts are unnecessary if code works on localhost.
- B. Blocking calls never impact latency in production.
- C. Exception messages should provide actionable context.
- D. Clean code is only about making variable names shorter.

53. Which statement is correct about call stack and control flow?
- A. All sync code should be converted to threads immediately.
- B. Clean code is only about making variable names shorter.
- C. Exceptions should usually be swallowed to keep systems stable.
- D. Consistent naming conventions help teams move faster.

54. Which statement is correct about CPU-bound vs I/O-bound reasoning?
- A. All sync code should be converted to threads immediately.
- B. Measurement is optional; optimization should start from intuition only.
- C. Separation of concerns reduces coupling and bug surface area.
- D. Catching every exception in every helper is always best practice.

55. Which statement is correct about timeouts and retries?
- A. CPU-bound and I/O-bound workloads are architecturally identical.
- B. Catching every exception in every helper is always best practice.
- C. A reliable sync baseline helps compare async/threaded alternatives fairly.
- D. Single long functions are easier to maintain than small cohesive ones.

56. Which statement is correct about error handling boundaries?
- A. Sync code can still be production-grade with good boundaries and error handling.
- B. Boundary validation is unnecessary in production services.
- C. Dependency injection makes testing harder and should be avoided.
- D. CPU-bound and I/O-bound workloads are architecturally identical.

57. Which statement is correct about clean sync design?
- A. Retries should be deep inside all utility functions.
- B. Guard clauses always reduce readability.
- C. Dependency injection makes testing harder and should be avoided.
- D. Blocking I/O without timeout is a common interview red flag.

58. Which statement is correct about refactoring strategy?
- A. Retries should be deep inside all utility functions.
- B. Logging every line is always superior to boundary logging.
- C. Refactoring large god-functions into smaller units improves testability.
- D. One slow call cannot impact the full sync request path.

59. Which statement is correct about measurement and optimization?
- A. Boundary logging is usually more useful than logging every line.
- B. One slow call cannot impact the full sync request path.
- C. Call stack understanding is irrelevant for debugging.
- D. Sync code cannot be reliable in production.

60. Which statement is correct about interview tradeoff explanation?
- A. Choosing sync first can be a valid architecture decision for low concurrency workloads.
- B. Using no timeout is safer than using a small timeout.
- C. Tradeoff discussion is unnecessary in interviews.
- D. Call stack understanding is irrelevant for debugging.

---

## Section C: MCQ (Multiple Correct) (61-100)

61. Select all correct statements about sync execution model.
Select all that apply.
- A. Retries should be infinite to guarantee success.
- B. Blocking operations in critical path can increase end-to-end latency.
- C. Synchronous flow executes one step at a time, with caller waiting for callee.
- D. Synchronous programming always runs multiple operations at the same instant.

62. Select all correct statements about blocking behavior.
Select all that apply.
- A. time.sleep, file I/O, DB calls, and network calls are common blocking points.
- B. Good sync architecture is a strong base before introducing concurrency.
- C. Blocking calls never impact latency in production.
- D. Timeouts are unnecessary if code works on localhost.

63. Select all correct statements about call stack and control flow.
Select all that apply.
- A. Clean code is only about making variable names shorter.
- B. Exceptions should usually be swallowed to keep systems stable.
- C. In sync code, control returns to caller after callee finishes.
- D. CPU-bound tasks spend most time in computation.

64. Select all correct statements about CPU-bound vs I/O-bound reasoning.
Select all that apply.
- A. Timeouts should be set at unstable boundaries to avoid indefinite hangs.
- B. Measurement is optional; optimization should start from intuition only.
- C. I/O-bound tasks spend most time waiting on external systems.
- D. All sync code should be converted to threads immediately.

65. Select all correct statements about timeouts and retries.
Select all that apply.
- A. Catching every exception in every helper is always best practice.
- B. Retries should be bounded and usually use backoff strategy.
- C. Single long functions are easier to maintain than small cohesive ones.
- D. Catching errors at boundary layers is often cleaner than deep catches everywhere.

66. Select all correct statements about error handling boundaries.
Select all that apply.
- A. Boundary validation is unnecessary in production services.
- B. Single-purpose functions generally improve readability and testability.
- C. Raising clear validation errors early improves maintainability.
- D. CPU-bound and I/O-bound workloads are architecturally identical.

67. Select all correct statements about clean sync design.
Select all that apply.
- A. Dependency injection makes testing harder and should be avoided.
- B. Dependency injection can make sync services easier to test.
- C. Guard clauses always reduce readability.
- D. Separating pure logic from I/O side effects improves design quality.

68. Select all correct statements about refactoring strategy.
Select all that apply.
- A. Measuring with perf_counter is better than relying on guesses.
- B. Logging every line is always superior to boundary logging.
- C. Deterministic flow is one reason sync code is easier to reason about.
- D. Retries should be deep inside all utility functions.

69. Select all correct statements about measurement and optimization.
Select all that apply.
- A. Retries belong near unstable dependencies, not in every helper.
- B. One slow call cannot impact the full sync request path.
- C. Sync code cannot be reliable in production.
- D. One slow blocking call can delay the full request path in sync execution.

70. Select all correct statements about interview tradeoff explanation.
Select all that apply.
- A. Tradeoff discussion is unnecessary in interviews.
- B. Guard clauses can reduce deep nesting in sync code.
- C. Call stack understanding is irrelevant for debugging.
- D. Meaningful names reduce cognitive load in code reviews.

71. Select all correct statements about sync execution model.
Select all that apply.
- A. Backoff should be random without any cap.
- B. Swallowing exceptions silently is usually a bad practice.
- C. Using no timeout is safer than using a small timeout.
- D. Clean sync boundaries make async/thread migration safer later.

72. Select all correct statements about blocking behavior.
Select all that apply.
- A. Returning clear errors is worse than returning silent defaults.
- B. Pure functions are harder to test than side-effect-heavy functions.
- C. Bounded retries with backoff are safer than infinite retries.
- D. Business rules should be explicit and not hidden in side effects.

73. Select all correct statements about call stack and control flow.
Select all that apply.
- A. Clear parse -> validate -> execute -> format stages improve maintainability.
- B. Sync systems still require reliability discipline (timeouts, retries, logging).
- C. Layered design is overengineering for all sync services.
- D. You should optimize first and measure later.

74. Select all correct statements about CPU-bound vs I/O-bound reasoning.
Select all that apply.
- A. Not all workloads need concurrency; simple sync can be best for low scale.
- B. Validation should happen only at database level, never at service boundary.
- C. Interviewers care about tradeoffs and correctness, not only syntax speed.
- D. Synchronous systems never need retries.

75. Select all correct statements about timeouts and retries.
Select all that apply.
- A. Functions with fewer responsibilities are easier to evolve safely.
- B. Readability has little impact on maintainability.
- C. Early returns for invalid data can improve readability.
- D. Code structure does not affect migration to async or threads.

76. Select all correct statements about error handling boundaries.
Select all that apply.
- A. Performance tuning should come after correctness and measurement.
- B. Exception messages should provide actionable context.
- C. Retries should be infinite to guarantee success.
- D. Synchronous programming always runs multiple operations at the same instant.

77. Select all correct statements about clean sync design.
Select all that apply.
- A. Blocking calls never impact latency in production.
- B. Timeouts are unnecessary if code works on localhost.
- C. Consistent naming conventions help teams move faster.
- D. Separation of concerns reduces coupling and bug surface area.

78. Select all correct statements about refactoring strategy.
Select all that apply.
- A. A reliable sync baseline helps compare async/threaded alternatives fairly.
- B. Exceptions should usually be swallowed to keep systems stable.
- C. Clean code is only about making variable names shorter.
- D. Sync code can still be production-grade with good boundaries and error handling.

79. Select all correct statements about measurement and optimization.
Select all that apply.
- A. Blocking I/O without timeout is a common interview red flag.
- B. Measurement is optional; optimization should start from intuition only.
- C. Refactoring large god-functions into smaller units improves testability.
- D. All sync code should be converted to threads immediately.

80. Select all correct statements about interview tradeoff explanation.
Select all that apply.
- A. Boundary logging is usually more useful than logging every line.
- B. Single long functions are easier to maintain than small cohesive ones.
- C. Catching every exception in every helper is always best practice.
- D. Choosing sync first can be a valid architecture decision for low concurrency workloads.

81. Select all correct statements about sync execution model.
Select all that apply.
- A. Blocking operations in critical path can increase end-to-end latency.
- B. Boundary validation is unnecessary in production services.
- C. Synchronous flow executes one step at a time, with caller waiting for callee.
- D. CPU-bound and I/O-bound workloads are architecturally identical.

82. Select all correct statements about blocking behavior.
Select all that apply.
- A. time.sleep, file I/O, DB calls, and network calls are common blocking points.
- B. Dependency injection makes testing harder and should be avoided.
- C. Guard clauses always reduce readability.
- D. Good sync architecture is a strong base before introducing concurrency.

83. Select all correct statements about call stack and control flow.
Select all that apply.
- A. Logging every line is always superior to boundary logging.
- B. Retries should be deep inside all utility functions.
- C. In sync code, control returns to caller after callee finishes.
- D. CPU-bound tasks spend most time in computation.

84. Select all correct statements about CPU-bound vs I/O-bound reasoning.
Select all that apply.
- A. Sync code cannot be reliable in production.
- B. One slow call cannot impact the full sync request path.
- C. Timeouts should be set at unstable boundaries to avoid indefinite hangs.
- D. I/O-bound tasks spend most time waiting on external systems.

85. Select all correct statements about timeouts and retries.
Select all that apply.
- A. Call stack understanding is irrelevant for debugging.
- B. Tradeoff discussion is unnecessary in interviews.
- C. Retries should be bounded and usually use backoff strategy.
- D. Catching errors at boundary layers is often cleaner than deep catches everywhere.

86. Select all correct statements about error handling boundaries.
Select all that apply.
- A. Single-purpose functions generally improve readability and testability.
- B. Raising clear validation errors early improves maintainability.
- C. Backoff should be random without any cap.
- D. Using no timeout is safer than using a small timeout.

87. Select all correct statements about clean sync design.
Select all that apply.
- A. Returning clear errors is worse than returning silent defaults.
- B. Separating pure logic from I/O side effects improves design quality.
- C. Pure functions are harder to test than side-effect-heavy functions.
- D. Dependency injection can make sync services easier to test.

88. Select all correct statements about refactoring strategy.
Select all that apply.
- A. You should optimize first and measure later.
- B. Layered design is overengineering for all sync services.
- C. Deterministic flow is one reason sync code is easier to reason about.
- D. Measuring with perf_counter is better than relying on guesses.

89. Select all correct statements about measurement and optimization.
Select all that apply.
- A. Synchronous systems never need retries.
- B. One slow blocking call can delay the full request path in sync execution.
- C. Validation should happen only at database level, never at service boundary.
- D. Retries belong near unstable dependencies, not in every helper.

90. Select all correct statements about interview tradeoff explanation.
Select all that apply.
- A. Readability has little impact on maintainability.
- B. Meaningful names reduce cognitive load in code reviews.
- C. Guard clauses can reduce deep nesting in sync code.
- D. Code structure does not affect migration to async or threads.

91. Select all correct statements about sync execution model.
Select all that apply.
- A. Clean sync boundaries make async/thread migration safer later.
- B. Synchronous programming always runs multiple operations at the same instant.
- C. Swallowing exceptions silently is usually a bad practice.
- D. Retries should be infinite to guarantee success.

92. Select all correct statements about blocking behavior.
Select all that apply.
- A. Timeouts are unnecessary if code works on localhost.
- B. Business rules should be explicit and not hidden in side effects.
- C. Bounded retries with backoff are safer than infinite retries.
- D. Blocking calls never impact latency in production.

93. Select all correct statements about call stack and control flow.
Select all that apply.
- A. Clear parse -> validate -> execute -> format stages improve maintainability.
- B. Sync systems still require reliability discipline (timeouts, retries, logging).
- C. Clean code is only about making variable names shorter.
- D. Exceptions should usually be swallowed to keep systems stable.

94. Select all correct statements about CPU-bound vs I/O-bound reasoning.
Select all that apply.
- A. Measurement is optional; optimization should start from intuition only.
- B. All sync code should be converted to threads immediately.
- C. Not all workloads need concurrency; simple sync can be best for low scale.
- D. Interviewers care about tradeoffs and correctness, not only syntax speed.

95. Select all correct statements about timeouts and retries.
Select all that apply.
- A. Catching every exception in every helper is always best practice.
- B. Functions with fewer responsibilities are easier to evolve safely.
- C. Single long functions are easier to maintain than small cohesive ones.
- D. Early returns for invalid data can improve readability.

96. Select all correct statements about error handling boundaries.
Select all that apply.
- A. Boundary validation is unnecessary in production services.
- B. Performance tuning should come after correctness and measurement.
- C. CPU-bound and I/O-bound workloads are architecturally identical.
- D. Exception messages should provide actionable context.

97. Select all correct statements about clean sync design.
Select all that apply.
- A. Consistent naming conventions help teams move faster.
- B. Dependency injection makes testing harder and should be avoided.
- C. Guard clauses always reduce readability.
- D. Separation of concerns reduces coupling and bug surface area.

98. Select all correct statements about refactoring strategy.
Select all that apply.
- A. Sync code can still be production-grade with good boundaries and error handling.
- B. Logging every line is always superior to boundary logging.
- C. Retries should be deep inside all utility functions.
- D. A reliable sync baseline helps compare async/threaded alternatives fairly.

99. Select all correct statements about measurement and optimization.
Select all that apply.
- A. Sync code cannot be reliable in production.
- B. Refactoring large god-functions into smaller units improves testability.
- C. One slow call cannot impact the full sync request path.
- D. Blocking I/O without timeout is a common interview red flag.

100. Select all correct statements about interview tradeoff explanation.
Select all that apply.
- A. Call stack understanding is irrelevant for debugging.
- B. Choosing sync first can be a valid architecture decision for low concurrency workloads.
- C. Tradeoff discussion is unnecessary in interviews.
- D. Boundary logging is usually more useful than logging every line.
