# Clean Code Foundations

## 1. Why Clean Code Matters in Real Projects

### Core truth
Code is read many more times than it is written. Most maintenance cost comes from understanding old code.

### Business impact of poor code
- bug fixes take longer
- onboarding new developers becomes hard
- features break existing behavior
- code reviews become slow and subjective

### Interview angle
Interviewers often ask:
- "How do you make code maintainable?"
- "How do you refactor legacy code safely?"
- "What is your clean code checklist before merging?"

---

## 2. Readability Over Cleverness

### Bad (too clever)
```python
def f(x):
    return x * 0.18
```

### Good (intent-revealing)
```python
GST_RATE = 0.18

def calculate_tax(amount: float) -> float:
    return amount * GST_RATE
```

### Rule
If a new developer cannot explain your code in one read, rewrite it.

---

## 3. Meaningful Naming

Naming is the fastest way to improve code quality.

### 3.1 Variable naming
Bad:
```python
n = "Asha"
x = 70000
d = []
```

Good:
```python
employee_name = "Asha"
monthly_salary = 70000
invalid_emails = []
```

### 3.2 Function naming
Bad:
```python
def process(data):
    ...
```

Good:
```python
def calculate_final_price(cart_items):
    ...
```

### 3.3 Boolean naming
Bad:
```python
flag = True
```

Good:
```python
is_active = True
has_access = False
can_retry = True
```

### 3.4 Constant naming
```python
MAX_RETRY_COUNT = 3
DISCOUNT_PERCENTAGE = 10
DEFAULT_TIMEOUT_SECONDS = 30
```

### 3.5 Naming interview traps
- vague names: `manager`, `processor`, `helper`, `data`
- abbreviations without context
- inconsistent naming style in same file
- names that lie about units (e.g., `timeout` but value is milliseconds)

---

## 4. Functions Should Do One Thing

A function should have one clear purpose and one level of abstraction.

### Bad
```python
def register_student(student):
    validate_student(student)
    student.grade = calculate_grade(student.marks)
    save_to_database(student)
    send_welcome_email(student.email)
    print("Student registered")
```

This mixes validation, business logic, persistence, communication, and UI.

### Better
```python
def assign_grade(student):
    student.grade = calculate_grade(student.marks)


def register_student(student, student_repository, email_service):
    validate_student(student)
    assign_grade(student)
    student_repository.save(student)
    email_service.send_welcome_email(student.email)
```

### Interview follow-up
How to split long functions:
1. identify behavior clusters
2. extract each cluster into small function
3. rename extracted functions by intent
4. rerun tests after each extraction

---

## 5. Function Signatures and API Clarity

### Keep parameters manageable
If a function takes too many parameters, it often indicates missing abstraction.

Bad:
```python
def create_invoice(customer_name, customer_email, customer_phone, address, city, state, zip_code, country):
    ...
```

Better:
```python
def create_invoice(customer, billing_address):
    ...
```

### Prefer explicit return behavior
Bad:
```python
def calculate_discount(price):
    if price > 1000:
        return price * 0.1
```

Good:
```python
def calculate_discount(price: float) -> float:
    if price > 1000:
        return price * 0.1
    return 0.0
```

---

## 6. Avoid Magic Numbers and Hardcoded Values

Magic numbers hide business intent.

Bad:
```python
if attendance >= 75:
    print("Allowed")
```

Good:
```python
MIN_ATTENDANCE_PERCENTAGE = 75

if attendance >= MIN_ATTENDANCE_PERCENTAGE:
    print("Allowed")
```

### Where to keep constants
- module-level constants for local rules
- config files / environment variables for deploy-time values

### Interview trap
Not all literals are bad. `0`, `1`, and `-1` can be acceptable when mathematically obvious.

---

## 7. DRY Principle (Do Not Repeat Yourself)

Duplication is a long-term maintenance bug.

### Duplication types
- logic duplication
- validation duplication
- message/template duplication
- configuration duplication

### Bad
```python
def calculate_john_average(marks):
    return sum(marks) / len(marks)


def calculate_alice_average(marks):
    return sum(marks) / len(marks)
```

### Good
```python
def calculate_average(marks: list[int]) -> float:
    return sum(marks) / len(marks)
```

### Important nuance
Do not force abstraction too early. Repeat once, understand pattern, then extract.

---

## 8. Comments, Docstrings, and Self-Documenting Code

### Rule of thumb
- code should explain "what"
- comments should explain "why"

Bad comment:
```python
# increment i
i += 1
```

Useful comment:
```python
# Retry only on transient failures to avoid duplicate payments.
if is_transient_error(error):
    retry_payment()
```

### Docstrings for public functions
```python
def calculate_grade(marks: list[int]) -> str:
    """Return grade based on average marks using institute grading policy."""
    ...
```

### Interview question
"Are comments bad?"
Strong answer: comments are valuable for business rules, trade-offs, and non-obvious constraints, but weak comments should be replaced with better naming and structure.

---

## 9. Side Effects and Predictability

Side effects are changes outside a function's local scope.

### Hidden side effect (bad)
```python
total = 0

def add_price(price):
    global total
    total += price
```

### Better
```python
def add_price(current_total: float, price: float) -> float:
    return current_total + price
```

Predictable functions are easier to test and reason about.

---

## 10. Guard Clauses vs Deep Nesting

### Bad nesting
```python
def withdraw(account, amount):
    if account is not None:
        if amount > 0:
            if account.balance >= amount:
                account.balance -= amount
```

### Better with guard clauses
```python
def withdraw(account, amount):
    if account is None:
        raise ValueError("Account is required")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if account.balance < amount:
        raise ValueError("Insufficient balance")

    account.balance -= amount
```

Interview benefit: shows control-flow clarity and defensive coding.

---

## 11. Error Handling Basics for Clean Code

### Avoid silent failures
Bad:
```python
try:
    save_user(user)
except Exception:
    pass
```

Good:
```python
try:
    save_user(user)
except DatabaseConnectionError as error:
    logger.error("Unable to save user: %s", error)
    raise
```

### Rule
Catch specific exceptions, preserve useful context, and fail loudly when needed.

---

## 12. Refactoring Workflow (Interview-Ready)

Use safe micro-steps:
1. understand current behavior
2. write or identify tests
3. rename unclear identifiers
4. extract small functions
5. remove duplication
6. rerun tests after each step
7. stop when readability improves clearly

### Common refactoring smells
- function longer than a screen
- same if/elif pattern repeated in many places
- broad `except Exception`
- names like `temp`, `data`, `obj`, `manager`

---

## 13. Before vs After Refactor Example

### Before
```python
def p(student_name, marks, email):
    a = sum(marks) / len(marks)
    if a > 90:
        g = "A"
    elif a > 80:
        g = "B"
    else:
        g = "C"

    print(student_name, g)
    with open("results.txt", "a") as f:
        f.write(student_name + ":" + g + "\n")

    send_email(email, "Your grade is " + g)
```

### After
```python
GRADE_A_THRESHOLD = 90
GRADE_B_THRESHOLD = 80
RESULTS_FILE = "results.txt"


def calculate_average(marks: list[int]) -> float:
    return sum(marks) / len(marks)


def determine_grade(average_score: float) -> str:
    if average_score > GRADE_A_THRESHOLD:
        return "A"
    if average_score > GRADE_B_THRESHOLD:
        return "B"
    return "C"


def append_grade_to_file(student_name: str, grade: str) -> None:
    with open(RESULTS_FILE, "a", encoding="utf-8") as results_file:
        results_file.write(f"{student_name}:{grade}\n")


def send_grade_email(email_service, email: str, grade: str) -> None:
    email_service.send(email, f"Your grade is {grade}")


def publish_student_grade(email_service, student_name: str, marks: list[int], email: str) -> None:
    average_score = calculate_average(marks)
    grade = determine_grade(average_score)
    print(student_name, grade)
    append_grade_to_file(student_name, grade)
    send_grade_email(email_service, email, grade)
```

What improved:
- intent-revealing names
- no magic numbers
- one responsibility per function
- testable units

---

## 14. High-Probability Interview Questions (Lecture 1)

1. What is clean code?
2. Why is naming considered a design activity?
3. How do you decide if a function does too much?
4. DRY vs premature abstraction: what is the balance?
5. When should comments be added?
6. What are side effects and why avoid hidden ones?
7. How do you refactor safely in production code?
8. What is the difference between readability and cleverness?

### Quick interview answer template
- define the concept in one line
- give one bad and one good code example
- explain impact on maintainability and testing

---

## 15. In-Class 2-Hour Teaching Plan

- 0-15 min: Why maintainability fails
- 15-35 min: Naming workshop
- 35-60 min: Single-responsibility functions
- 60-75 min: Magic numbers and constants
- 75-95 min: DRY and duplication smells
- 95-110 min: Comments, side effects, guard clauses
- 110-120 min: live refactor + Q/A

---

## 16. Assignment (Post Lecture)
Build a Student Grade Management script with clean code rules:
- meaningful names only
- max 20 lines per function (target guideline)
- no duplicated grade logic
- no magic numbers
- one function for one responsibility

Deliverables:
- `student_grade_clean.py`
- short note: "3 clean code improvements I made"

---

## Final Recap
Clean code is not decoration. It is engineering discipline that reduces defects and improves delivery speed.

If students master this lecture well, OOP in the next lecture becomes natural and clean, not confusing and messy.
