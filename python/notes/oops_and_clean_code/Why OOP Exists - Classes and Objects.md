# Why OOP Exists - Classes and Objects

## 1. Why OOP Exists

### Procedural pain at scale
Procedural code often spreads related data and logic across many files and functions.

Example:
```python
student1_name = "Asha"
student1_marks = [90, 85]

student2_name = "Ravi"
student2_marks = [80, 70]

# Similar functions repeated for each entity type
```

As data grows:
- duplication increases
- updates become risky
- behavior is hard to track

### OOP idea
Group data and behavior together in a single abstraction.

```text
Object = State (attributes) + Behavior (methods)
```

---

## 2. Core Terminology

### Class
Blueprint/template for creating objects.

```python
class Student:
    pass
```

### Object
Concrete instance of a class.

```python
student = Student()
```

### State
Data held by an object.

### Behavior
Actions an object can perform.

### Constructor (`__init__`)
Special method that initializes object state.

### `self`
Reference to the current instance.

---

## 3. Building a Real Class Step by Step

```python
class Student:
    def __init__(self, name: str, marks: list[int]):
        self.name = name
        self.marks = marks

    def calculate_average(self) -> float:
        return sum(self.marks) / len(self.marks)

    def determine_grade(self) -> str:
        average = self.calculate_average()
        if average > 90:
            return "A"
        if average > 80:
            return "B"
        return "C"
```

### Why this is good
- domain class (`Student`) maps to real concept
- state and behavior are colocated
- logic is reusable per object

---

## 4. Understanding `self` Deeply (Interview Favorite)

When we call:
```python
student.determine_grade()
```
Python internally does:
```python
Student.determine_grade(student)
```

So `self` is not a keyword like `if`; it is a parameter name by convention representing the current object.

### Common mistakes
- forgetting `self` in method definition
- using class name instead of `self` for instance data
- confusing instance attributes with local variables

Bad:
```python
class Student:
    def __init__(self, name):
        name = name
```

Good:
```python
class Student:
    def __init__(self, name):
        self.name = name
```

---

## 5. Constructor (`__init__`) Deep Dive

Constructor responsibilities:
- initialize required state
- enforce basic object validity

```python
class BankAccount:
    def __init__(self, account_number: str, initial_balance: float):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.account_number = account_number
        self.balance = initial_balance
```

### Interview trap
Do not put heavy external side effects in constructor (network calls, file writes) unless unavoidable.

---

## 6. State vs Behavior Design

Strong class design answer:
- attributes represent what object knows
- methods represent what object does

Bad design (anemic + utility style):
```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks


def calculate_student_average(student):
    return sum(student.marks) / len(student.marks)
```

Better:
```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def calculate_average(self):
        return sum(self.marks) / len(self.marks)
```

---

## 7. Class Attributes vs Instance Attributes

### Instance attribute
Unique per object.

```python
self.name = name
```

### Class attribute
Shared by all objects.

```python
class Student:
    school_name = "ABC Public School"
```

### Interview tricky concept
Mutating class-level mutable data affects all instances.

```python
class Student:
    tags = []  # shared mutable object - risky
```

Better:
```python
class Student:
    def __init__(self):
        self.tags = []
```

---

## 8. Common OOP Mistakes Asked in Interviews

1. Creating classes for simple utility operations
2. Overusing getters/setters without behavior
3. Using vague class names (`Manager`, `Helper`)
4. Storing unrelated responsibilities in one class
5. Confusing inheritance with reuse for everything
6. Mutable default arguments in constructors

### Mutable default argument trap
Bad:
```python
class Cart:
    def __init__(self, items=[]):
        self.items = items
```

Good:
```python
class Cart:
    def __init__(self, items=None):
        self.items = [] if items is None else items
```

---

## 9. When to Create a Class (Decision Framework)

Create a class if:
- there is a real domain concept (Student, Invoice, Product)
- data and behavior belong together
- you need multiple objects with same structure
- object invariants need protection

Do not create a class if:
- one simple stateless function is enough
- there is no meaningful state
- class exists only to wrap one function

Example:
- Good function-only: `add_numbers(a, b)`
- Good class-based: `BankAccount.withdraw(amount)`

---

## 10. Clean Code Inside OOP

### Naming rules
- class names: nouns (`Student`, `Order`, `Invoice`)
- method names: verbs (`calculate_total`, `send_email`)
- boolean methods: `is_eligible`, `has_access`

### Keep methods focused
Bad:
```python
def generate_report(self):
    fetch_data()
    clean_data()
    save_data()
    email_report()
```

Better:
```python
def generate_report(self):
    report_data = self._build_report_data()
    self._save_report(report_data)
    self._notify_users(report_data)
```

---

## 11. Real Example: Employee Class

```python
class Employee:
    TAX_RATE = 0.1

    def __init__(self, employee_id: str, name: str, monthly_salary: float):
        if monthly_salary < 0:
            raise ValueError("Salary cannot be negative")

        self.employee_id = employee_id
        self.name = name
        self.monthly_salary = monthly_salary

    def calculate_annual_salary(self) -> float:
        return self.monthly_salary * 12

    def calculate_annual_tax(self) -> float:
        return self.calculate_annual_salary() * self.TAX_RATE

    def __repr__(self) -> str:
        return (
            "Employee("
            f"employee_id={self.employee_id!r}, "
            f"name={self.name!r}, "
            f"monthly_salary={self.monthly_salary!r}"
            ")"
        )
```

Why interviewers like this example:
- validation in constructor
- clear methods
- reusable business rules
- readable debug representation

---

## 12. `__repr__` vs `__str__` (Basic Interview Mention)

- `__repr__`: developer-facing, unambiguous representation
- `__str__`: user-facing readable text

If `__str__` is absent, Python may use `__repr__`.

---

## 13. Mini Refactor: Procedural to OOP

### Procedural version
```python
def create_student(name, marks):
    return {"name": name, "marks": marks}


def calculate_average(student):
    return sum(student["marks"]) / len(student["marks"])
```

### OOP version
```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def calculate_average(self):
        return sum(self.marks) / len(self.marks)
```

### Design gain
State and operations stay together. Less dictionary-key mistakes, better discoverability.

---

## 14. High-Probability Interview Questions (Lecture 2)

1. Why do we need OOP if functions already exist?
2. Difference between class and object?
3. What does `self` represent in Python?
4. Why is `__init__` not a constructor in memory-allocation sense, but initializer?
5. Difference between class attribute and instance attribute?
6. Why avoid mutable default arguments?
7. When should a class be replaced by a function?
8. How do you design a good beginner-friendly class?

### Strong answer pattern
- define concept
- show mini code example
- explain real project 

---

## 16. Assignment (Post Lecture)
Build a Library Management mini-model with clean OOP:

Classes:
- `Book`
- `Member`
- `Library`

Minimum features:
- add book
- register member
- borrow book
- return book

Clean code requirements:
- meaningful naming
- constructor validation where required
- no long god-methods
- no shared mutable class-level lists

---

## Final Recap
This lecture is the bridge from Python syntax to software design thinking.

Students who master these fundamentals can learn Encapsulation, Abstraction, Inheritance, Polymorphism, and SOLID much faster and with fewer misconceptions.
