# Composition vs Inheritance in Python: Clean Code Decision Guide

## 1. Why This Lecture Matters

Many design problems are not about syntax.  
They are about choosing the right relationship between classes.

The most common OOP mistake:
- using inheritance for every reuse case

This lecture helps you answer:
```text
Should I use Inheritance or Composition here?
```

---

## 2. Quick Definitions

### Inheritance
One class derives from another.

```text
Child IS-A Parent
```

Example:
- `Manager is an Employee`

### Composition
One class contains and uses another class.

```text
Class HAS-A dependency
```

Example:
- `Car has an Engine`

---

## 3. First Rule: IS-A vs HAS-A

If relation is `is-a`, inheritance may fit.
If relation is `has-a`, composition is usually correct.

Examples:
- `Dog is an Animal` -> inheritance
- `Dog has a Collar` -> composition
- `OrderService has a PaymentGateway` -> composition

---

## 4. Inheritance Example (Good Case)

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def annual_salary(self) -> float:
        return self.salary * 12


class Manager(Employee):
    def bonus(self) -> float:
        return self.salary * 0.20


manager = Manager("Asha", 100000)
print(manager.annual_salary())
print(manager.bonus())
```

Expected output:
```text
1200000
20000.0
```

Why inheritance works here:
- `Manager` is a specialized type of `Employee`
- shared core behavior is stable (`annual_salary`)

---

## 5. Composition Example (Good Case)

```python
class Engine:
    def start(self) -> str:
        return "Engine started"


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def start(self) -> str:
        return f"Car: {self.engine.start()}"


car = Car(Engine())
print(car.start())
```

Expected output:
```text
Car: Engine started
```

Why composition works:
- `Car` is not a type of `Engine`
- `Car` uses `Engine` as a part/dependency

---

## 6. Why "Prefer Composition Over Inheritance"

Composition is often safer because:
1. lower coupling between classes
2. behavior can be replaced at runtime
3. changes in one class usually affect fewer classes
4. testing is easier with fake/mock dependencies

Inheritance can become rigid when:
- hierarchy grows deep
- parent changes break many children
- children inherit behavior they do not need

---

## 7. Decision Matrix (Practical)

Use inheritance when:
- true `is-a` relationship exists
- parent behavior is stable and universal
- substitutability is natural (LSP)

Use composition when:
- relationship is `has-a` / `uses-a`
- behavior varies frequently
- runtime swapping is useful
- you want loose coupling

---

## 8. Hard Concept: Tight Coupling in Inheritance

Problem pattern:
- child depends on parent internals
- parent change causes side effects in child classes

```python
class FileLogger:
    def log(self, message: str) -> None:
        print(f"FILE: {message}")


class AuditFileLogger(FileLogger):
    def log(self, message: str) -> None:
        super().log(message)
        print("AUDIT ENTRY WRITTEN")


logger = AuditFileLogger()
logger.log("Payment success")
```

Expected output:
```text
FILE: Payment success
AUDIT ENTRY WRITTEN
```

If parent `log()` changes format or behavior, many child classes can break.

---

## 9. Hard Concept: Flexible Behavior with Composition

Composition allows swapping behavior easily.

```python
class ConsoleLogger:
    def log(self, message: str) -> None:
        print(f"CONSOLE: {message}")


class JsonLogger:
    def log(self, message: str) -> None:
        print(f'{{"message": "{message}"}}')


class PaymentService:
    def __init__(self, logger):
        self.logger = logger

    def pay(self, amount: float) -> None:
        self.logger.log(f"Paid {amount}")


service1 = PaymentService(ConsoleLogger())
service1.pay(500)

service2 = PaymentService(JsonLogger())
service2.pay(750)
```

Expected output:
```text
CONSOLE: Paid 500
{"message": "Paid 750"}
```

No class hierarchy change required. Only dependency changes.

---

## 10. Composition + Abstraction (Best of Both)

You can combine composition with interfaces/ABCs.

```python
from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"CONSOLE: {message}")


class OrderService:
    def __init__(self, logger: Logger):
        self.logger = logger

    def place_order(self, order_id: str) -> None:
        self.logger.log(f"Order placed: {order_id}")


OrderService(ConsoleLogger()).place_order("ORD-101")
```

Expected output:
```text
CONSOLE: Order placed: ORD-101
```

This gives:
- loose coupling (composition)
- contract clarity (abstraction)

---

## 11. Refactor Example: Wrong Inheritance -> Better Composition

### Before (misuse)
```python
class Database:
    def connect(self) -> str:
        return "DB connected"


class UserService(Database):  # wrong: UserService is not a Database
    def create_user(self, username: str) -> None:
        print(self.connect())
        print(f"Created user: {username}")


UserService().create_user("ravi")
```

Expected output:
```text
DB connected
Created user: ravi
```

### After (composition)
```python
class Database:
    def connect(self) -> str:
        return "DB connected"


class UserService:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, username: str) -> None:
        print(self.database.connect())
        print(f"Created user: {username}")


UserService(Database()).create_user("ravi")
```

Expected output:
```text
DB connected
Created user: ravi
```

Design gain:
- correct domain relation
- easier to replace database object in tests

---

## 12. Composition and Strategy Pattern

Strategy pattern is composition in action.
We move interchangeable logic into separate classes.

```python
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        return amount


class FestivalDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        return amount * 0.90


class Checkout:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def total(self, amount: float) -> float:
        return self.strategy.apply(amount)


print(Checkout(NoDiscount()).total(1000))
print(Checkout(FestivalDiscount()).total(1000))
```

Expected output:
```text
1000
900.0
```

---

## 13. Testing Benefit of Composition

With composition, testing gets simpler because you can inject fake dependencies.

```python
class FakeLogger:
    def __init__(self):
        self.messages = []

    def log(self, message: str) -> None:
        self.messages.append(message)


class BillingService:
    def __init__(self, logger):
        self.logger = logger

    def bill(self, amount: float) -> None:
        self.logger.log(f"Billed {amount}")


fake_logger = FakeLogger()
service = BillingService(fake_logger)
service.bill(300)
print(fake_logger.messages)
```

Expected output:
```text
['Billed 300']
```

---

## 14. Clean Code Guidelines

1. Start with composition by default.
2. Move to inheritance only when `is-a` is clearly true.
3. Keep inheritance hierarchies shallow.
4. Avoid parent classes with too many responsibilities.
5. Do not use inheritance only to reuse helper methods.
6. Depend on abstractions, not concrete classes.
7. Name classes by domain meaning, not technical convenience.

---

## 15. Common Smells and Fixes

Smell: `UserService` extends `Database`  
Fix: `UserService` should contain/use `Database`.

Smell: Deep hierarchy (`A -> B -> C -> D`)  
Fix: flatten hierarchy and compose behavior.

Smell: parent class has many optional methods children do not need  
Fix: split parent into smaller contracts or use strategies.

Smell: changing parent breaks all children  
Fix: reduce parent surface and stabilize contract.

---

## 16. Relation with LSP and OCP

### LSP (Liskov Substitution Principle)
If child cannot safely replace parent, inheritance is wrong.

### OCP (Open/Closed Principle)
Composition + interfaces makes extension easier:
- add new class
- avoid editing stable service code

---

## 17. Interview Quick Answers

1. Why prefer composition over inheritance?
Because it reduces coupling and improves flexibility/testability.

2. When should inheritance be used?
When relation is true `is-a` and parent contract is stable.

3. Can composition and inheritance be combined?
Yes. Often best architecture uses both, with composition dominant.

4. Is inheritance bad?
No. It is powerful when used for real hierarchy and stable abstraction.

---

## 18. One-Page Summary

- Inheritance = `is-a` relation.
- Composition = `has-a` / `uses-a` relation.
- For most business services, composition is safer and cleaner.
- Use inheritance for genuine specialization.
- Use composition for flexibility, swapping behavior, and testing.

---

## 19. Practice Assignment (Lecture 6)

Build notification module in two versions:

Version A (inheritance):
- `NotificationSender` base class
- child classes `EmailSender`, `SmsSender`, `PushSender`

Version B (composition + strategy):
- `NotificationService(channel_strategy)`
- strategies `EmailChannel`, `SmsChannel`, `PushChannel`

Tasks:
1. Compare both designs in a short note.
2. Add one new channel (`Slack`) in both designs.
3. Mention which design changed fewer existing files and why.

