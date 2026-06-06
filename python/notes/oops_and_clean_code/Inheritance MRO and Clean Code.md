# Inheritance in Python: MRO and Clean Code

## 1. Why Inheritance Exists

Inheritance helps us avoid repeating shared behavior across related classes.

```text
Parent class = common behavior
Child class = common behavior + specialization
```

Real-world examples:
- `Employee` -> `Manager`, `Developer`
- `PaymentProcessor` -> `CardProcessor`, `UPIProcessor`

---

## 2. First Important Decision: Use or Not Use Inheritance

Use inheritance only when relation is a true `is-a`.

Good:
- `Manager is an Employee`
- `SavingsAccount is a BankAccount`

Bad:
- `Car is an Engine` (wrong)
- `Car has an Engine` (composition is correct)

Quick decision checklist:
1. Does child logically represent a specific kind of parent?
2. Should child be usable wherever parent is expected?
3. Is shared behavior stable enough to keep in parent?

If answer is mostly "no", use composition.

---

## 3. Basic Syntax and Flow

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "Some sound"


class Dog(Animal):
    def speak(self) -> str:
        return "Bark"


dog = Dog("Bruno")
print(dog.name)     # inherited state
print(dog.speak())  # overridden behavior
```

Expected output:
```text
Bruno
Bark
```

What happened:
1. `Dog` inherited all `Animal` members.
2. `Dog.speak()` replaced `Animal.speak()`.
3. `name` still came from parent constructor.

---

## 4. What Child Class Inherits

Child class can inherit:
- instance methods
- class methods
- static methods
- properties
- class attributes

It can also override any method for specialized behavior.

---

## 5. Types of Inheritance in Python

### Single inheritance
One child, one parent.

### Multilevel inheritance
Grandparent -> Parent -> Child.

### Hierarchical inheritance
One parent, many children.

### Multiple inheritance
One child, multiple parents.

### Hybrid inheritance
Combination of multiple patterns.

Production tip:
- single inheritance + composition is the most maintainable default.

---

## 6. `super()` Deep Dive (Very Important)

`super()` calls the next method in MRO, not always direct parent.

```python
class Employee:
    def __init__(self, employee_id: str, name: str):
        self.employee_id = employee_id
        self.name = name


class Manager(Employee):
    def __init__(self, employee_id: str, name: str, team_size: int):
        super().__init__(employee_id, name)
        if team_size < 0:
            raise ValueError("team_size cannot be negative")
        self.team_size = team_size


manager = Manager("E101", "Asha", 5)
print(manager.employee_id, manager.name, manager.team_size)
```

Expected output:
```text
E101 Asha 5
```

Why always prefer `super()`:
- safer when hierarchy changes
- enables cooperative multiple inheritance
- removes hardcoded parent dependency

---

## 7. Overriding: Replace vs Extend

### Replace parent behavior completely
```python
class Report:
    def render(self) -> str:
        return "Generic report"


class PdfReport(Report):
    def render(self) -> str:
        return "PDF report"


print(PdfReport().render())
```

Expected output:
```text
PDF report
```

### Extend parent behavior
```python
class Logger:
    def log(self, message: str) -> None:
        print(f"[INFO] {message}")


class AuditLogger(Logger):
    def log(self, message: str) -> None:
        super().log(message)
        print(f"[AUDIT] stored: {message}")


AuditLogger().log("Payment completed")
```

Expected output:
```text
[INFO] Payment completed
[AUDIT] stored: Payment completed
```

Rule:
- parent logic still valid -> extend
- parent logic invalid for child -> replace

---

## 8. Hard Concept: MRO (Method Resolution Order)

MRO decides which class method Python uses when same method appears in multiple classes.

Python uses C3 linearization, which gives:
- deterministic order
- no ambiguous lookup
- monotonic behavior

Example:
```python
class A:
    def who(self) -> str:
        return "A"


class B(A):
    def who(self) -> str:
        return "B"


class C(A):
    def who(self) -> str:
        return "C"


class D(B, C):
    pass


print(D().who())   # B
print(D.mro())     # [D, B, C, A, object]
```

Expected output:
```text
B
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

Read this as:
- Python checks `D`, then `B`, then `C`, then `A`.

---

## 9. Hard Concept: Diamond Problem

Diamond shape:
```text
    A
   / \
  B   C
   \ /
    D
```

If `B` and `C` both inherit `A`, and `D` inherits both, method ambiguity can happen.
MRO solves this by fixed order.

Debug command:
```python
print(D.mro())
```

Expected output:
```text
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

---

## 10. Cooperative Multiple Inheritance (Constructor Pattern)

If you use multiple inheritance, every class should call `super()`.

```python
class A:
    def __init__(self, **kwargs):
        self.a = True
        super().__init__(**kwargs)


class B(A):
    def __init__(self, **kwargs):
        self.b = True
        super().__init__(**kwargs)


class C(A):
    def __init__(self, **kwargs):
        self.c = True
        super().__init__(**kwargs)


class D(B, C):
    def __init__(self):
        super().__init__()
        self.d = True


obj = D()
print(obj.a, obj.b, obj.c, obj.d)
```

Expected output:
```text
True True True True
```

Why `**kwargs` pattern:
- allows each class to consume only what it needs
- keeps constructor chain cooperative

---

## 11. Attribute and Method Lookup Rules

For `obj.attr`, Python checks in this order:
1. instance attributes (`obj.__dict__`)
2. class attributes (`Class.__dict__`)
3. parent classes by MRO

For methods:
- method function is found on class/parent
- bound to instance at call time

---

## 12. Protected and Private in Inheritance

### `_name` (protected convention)
- meant for class and subclass use
- still accessible from outside by convention

### `__name` (name mangling)
- converted to `_ClassName__name`
- avoids accidental override collisions in subclasses

Use guideline:
- extension points: single underscore
- truly internal collision-prone fields: double underscore

---

## 13. Inheritance with Abstract Base Classes

This connects to abstraction lecture:
- parent defines contract
- children must implement required methods

```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> None:
        pass


class UpiProcessor(PaymentProcessor):
    def process(self, amount: float) -> None:
        print(f"UPI processed: {amount}")


UpiProcessor().process(2500)
```

Expected output:
```text
UPI processed: 2500
```

Benefits:
- clear API contract
- fail-fast for incomplete child classes
- easier code review and testing

---

## 14. Mixins vs Normal Base Classes

Mixin:
- small reusable behavior
- not a complete domain model

```python
class TimestampMixin:
    def touch(self) -> None:
        from datetime import datetime
        self.updated_at = datetime.utcnow()


class User(TimestampMixin):
    pass


user = User()
print(hasattr(user, "updated_at"))
user.touch()
print(hasattr(user, "updated_at"))
```

Expected output:
```text
False
True
```

Good mixin traits:
- single responsibility
- no heavy constructor dependency
- clear name like `SomethingMixin`

---

## 15. Clean Code Rules for Inheritance

1. Keep parent class minimal and stable.
2. Keep hierarchy shallow (usually 2-3 levels max).
3. Do not call overridable methods in parent `__init__`.
4. Keep method signatures compatible in child classes.
5. Document which methods are safe to override.
6. Avoid hidden side effects that surprise subclasses.
7. Prefer composition when behavior can vary independently.

---

## 16. Inheritance Smells and Refactoring

Smell: deep hierarchy (`A -> B -> C -> D -> E`)  
Refactor: flatten hierarchy + composition.

Smell: subclass exists only to share utility functions  
Refactor: extract helper/service class.

Smell: parent keeps changing and breaks many children  
Refactor: split parent responsibilities; stabilize contract.

Smell: many `if role == ...` in one class  
Refactor: move role behavior to subclasses.

---

## 17. Refactor Example: Conditional to Inheritance

Before:
```python
def calculate_bonus(role: str, salary: float) -> float:
    if role == "developer":
        return salary * 0.20
    if role == "manager":
        return salary * 0.30
    raise ValueError("Unsupported role")


print(calculate_bonus("developer", 100000))
print(calculate_bonus("manager", 100000))
```

Expected output:
```text
20000.0
30000.0
```

After:
```python
from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, salary: float):
        self.salary = salary

    @abstractmethod
    def calculate_bonus(self) -> float:
        pass


class Developer(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.20


class Manager(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.30


print(Developer(100000).calculate_bonus())
print(Manager(100000).calculate_bonus())
```

Expected output:
```text
20000.0
30000.0
```

Gain:
- easier extension
- cleaner caller code
- each rule isolated in one class

---

## 18. Testing Inheritance Properly

Test checklist:
1. Parent contract behavior tests.
2. Child-specific override tests.
3. Substitutability tests:
child object should work anywhere parent is expected.
4. MRO-sensitive tests if multiple inheritance exists.

Example idea:
- same `process_payment` tests for `CardProcessor`, `UPIProcessor`, `WalletProcessor`.

---

## 19. Common Beginner Mistakes

1. Using inheritance for every reuse problem.
2. Forgetting `super().__init__()` in child constructor.
3. Hardcoding parent class calls instead of `super()`.
4. Building very deep class trees too early.
5. Mixing unrelated responsibilities in parent class.

---

## 20. Quick Interview Revision

1. Inheritance means deriving specialized classes from a base class.
2. `super()` follows MRO.
3. MRO resolves method lookup deterministically.
4. Multiple inheritance is powerful but needs disciplined `super()` usage.
5. Prefer composition where relation is not true `is-a`.
6. ABCs enforce contracts.
7. Keep hierarchies small and clean.

---

## 21. One-Page Summary

- Inheritance is for hierarchy, not generic reuse.
- `super()` and MRO are central to correct behavior.
- Multiple inheritance is safe when classes cooperate.
- Clean code in inheritance means small parents, stable contracts, shallow trees.
- If inheritance feels forced, composition is probably better.

---

## 22. Practice Assignment

Build a shipping module:
- abstract base class `Shipment`
- child classes `StandardShipment`, `ExpressShipment`, `InternationalShipment`
- method `calculate_cost(weight)`
- common validation in parent
- no `if shipment_type == ...` in client code
- write tests for each subclass and one substitutability test
