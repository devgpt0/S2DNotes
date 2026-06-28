# Abstraction, API Design and Abstract Classes

## 1. Why Abstraction Exists

Abstraction exists to manage complexity.

Example mindset:
- user wants one simple action
- system performs many hidden steps

Car example:
```python
car.start()
```

Internal details (hidden from user):
```python
car.inject_fuel()
car.activate_spark_plugs()
car.rotate_crankshaft()
car.start_combustion_cycle()
```

Core idea:
```text
Expose what users need. Hide what users do not need.
```

Real-world parallels:
- mobile phone: "make call" instead of radio/network internals
- ATM: "withdraw money" instead of database transaction workflow
- AI apps: simple `ask()` interface over complex model internals

---

## 2. What Is Abstraction

### Academic definition
Showing essential features while hiding implementation details.

### Engineering definition
Provide the simplest useful interface to users.

### Bad Example (User handles workflow)
```python
class CoffeeMachine:
    def heat_water(self):
        pass

    def grind_beans(self):
        pass

    def extract_coffee(self):
        pass

    def mix_milk(self):
        pass


machine = CoffeeMachine()
machine.heat_water()
machine.grind_beans()
machine.extract_coffee()
machine.mix_milk()
```

Problem:
- user must remember internal sequence
- easy to misuse

### Better Example (Single clear API)
```python
class CoffeeMachine:
    def make_coffee(self) -> None:
        self._heat_water()
        self._grind_beans()
        self._extract_coffee()
        self._mix_milk()

    def _heat_water(self) -> None:
        pass

    def _grind_beans(self) -> None:
        pass

    def _extract_coffee(self) -> None:
        pass

    def _mix_milk(self) -> None:
        pass


machine = CoffeeMachine()
machine.make_coffee()
```

Clean code rule:
```text
Users should care about WHAT happens, not HOW it happens.
```

---

## 3. Abstraction vs Encapsulation

These concepts work together but are not the same.

### Encapsulation
- focus: protect data and invariants
- goal: prevent invalid object state
- example: validate `balance`, hide direct mutation

### Abstraction
- focus: hide complexity behind simple operations
- goal: reduce mental burden for user
- example: `transfer_money()` instead of many internal steps

Comparison:

| Encapsulation | Abstraction |
| --- | --- |
| Protects state | Hides complexity |
| Data safety | API simplicity |
| Validation-heavy | Workflow simplification |
| Prevents misuse | Reduces cognitive load |

Combined example:
```python
class Car:
    def start(self) -> None:  # abstraction
        self._inject_fuel()
        self._activate_spark()
        self._start_engine()

    def _inject_fuel(self) -> None:  # encapsulated internals
        pass

    def _activate_spark(self) -> None:
        pass

    def _start_engine(self) -> None:
        pass
```

---

## 4. API Design Through Abstraction

In OOP, your public methods are your API.

Example:
```python
class BankAccount:
    def deposit(self, amount: float) -> None:
        ...

    def withdraw(self, amount: float) -> None:
        ...

    def transfer(self, amount: float, receiver: "BankAccount") -> None:
        ...
```

### Good API characteristics

1. Small
- avoid huge parameter lists
- use objects to group related data

2. Predictable
- method names should clearly tell behavior
- avoid vague names like `do()`, `handle()`, `process()`

3. Intuitive
- naming should match business language
- `calculate_salary()` is clearer than `employee.process()`

API smell:
```text
If method names need constant explanation, abstraction is weak.
```

---

## 5. Cognitive Load and Simplicity

Cognitive load = mental effort required to use code.

Bad:
```python
machine.step1()
machine.step2()
machine.step3()
machine.step4()
machine.step5()
```

Good:
```python
machine.start()
```

Another example:

Bad:
```python
email_service.connect()
email_service.authenticate()
email_service.validate()
email_service.send()
email_service.disconnect()
```

Good:
```python
email_service.send_email()
```

Engineering goal:
- reduce decisions
- reduce remembering
- reduce confusion

---

## 6. Abstract Base Classes (ABC) in Python

Use ABCs when multiple implementations must follow a shared contract.

### Define the contract
```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> None:
        pass
```

Cannot instantiate abstract class:
```python
# PaymentProcessor()  # TypeError
```

### Concrete implementations
```python
class UpiPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> None:
        print(f"UPI payment of {amount}")


class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> None:
        print(f"Credit card payment of {amount}")


class NetBankingPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> None:
        print(f"Net banking payment of {amount}")
```

### Polymorphic usage
```python
payments: list[PaymentProcessor] = [
    UpiPayment(),
    CreditCardPayment(),
    NetBankingPayment(),
]

for payment in payments:
    payment.process_payment(1000)
```

Key idea:
- abstract class defines what must happen
- child classes define how it happens

---

## 7. Abstraction and Low Coupling

Bad dependency:
```text
UserService -> EmailNotification
```

Better dependency:
```text
UserService -> Notification (abstraction)
```

Example:
```python
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


class UserService:
    def __init__(self, notifier: Notification):
        self._notifier = notifier

    def register_user(self, username: str) -> None:
        self._notifier.send(f"Welcome {username}")
```

Benefit:
- easier extension
- easier testing
- less change ripple across system

---

## 8. Framework-Level Abstraction Examples

Patterns seen in popular frameworks:

1. ORM style: `user.save()` hides SQL/query lifecycle.
2. Route decorators: simple endpoint declaration hides HTTP internals.
3. Agent invocation APIs: one call hides prompt/tool/model orchestration.
4. Workflow kickoff APIs: one method hides scheduling and dependency flow.

Takeaway:
```text
Most mature frameworks succeed because they provide strong abstractions.
```

---

## 9. Mini Project Pattern: File Storage Abstraction

Goal:
- common API for multiple storage providers
- caller should not care if backend is local disk, S3, or GCP

```python
from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def save(self, path: str, content: str) -> None:
        pass

    @abstractmethod
    def read(self, path: str) -> str:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        pass


class LocalStorage(FileStorage):
    def save(self, path: str, content: str) -> None:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    def read(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def delete(self, path: str) -> None:
        # replace with safe delete logic as needed
        print(f"Deleting local file: {path}")
```

Usage:
```python
def backup_config(storage: FileStorage) -> None:
    storage.save("config.txt", "mode=prod")


storage = LocalStorage()
backup_config(storage)
```

---

## 10. Refactoring Pattern with Abstraction

### Before
```python
class UserManager:
    def send_email(self):
        ...

    def send_sms(self):
        ...

    def send_push(self):
        ...
```

Problem:
- one class knows too many delivery mechanisms
- high coupling and poor extensibility

### After
- create `Notification` abstraction
- implement `EmailNotification`, `SMSNotification`, `PushNotification`
- make `UserManager` depend on `Notification` contract

Result:
- open for new channels
- closed for frequent edits in core workflow code

---

## 11. Interview Quick Notes

### What is abstraction?
Showing essential behavior while hiding implementation details.

### Why use abstraction?
To reduce complexity and improve usability of software components.

### Encapsulation vs abstraction?
- encapsulation protects state
- abstraction simplifies behavior and hides internal workflow

### What is an abstract class?
A non-instantiable class that defines required methods for subclasses.

### What is `@abstractmethod`?
A method declaration that subclasses must implement.

---

## 12. Key Takeaways

1. Abstraction simplifies complex systems.
2. Good APIs reduce cognitive load.
3. Public methods are abstractions.
4. ABCs define contracts and improve consistency.
5. Child classes provide implementation details.
6. Abstraction lowers coupling and supports extensibility.
7. Strong abstractions are foundation for scalable architecture and SOLID design.

---

## 13. Missing Critical Concept: Protocol-Based Abstraction

ABCs provide explicit inheritance contracts. Protocols provide structural contracts.

```python
from typing import Protocol


class Notifier(Protocol):
    def send(self, message: str) -> None:
        ...


class SlackNotifier:
    def send(self, message: str) -> None:
        print(f"SLACK: {message}")


def onboard(notifier: Notifier, username: str) -> None:
    notifier.send(f"welcome {username}")
```

Why this matters:
- lower coupling than forced class hierarchy.
- excellent fit for dependency injection and testing.

## 14. Composition Root (Where Dependencies Are Wired)

A common missing design idea:
- object creation and wiring should happen in one place (composition root).
- business classes should receive dependencies, not construct them internally.

```python
class UserService:
    def __init__(self, notifier):
        self.notifier = notifier


def build_user_service() -> UserService:
    notifier = SlackNotifier()
    return UserService(notifier)
```

Benefits:
- easier testing
- environment-specific wiring (dev/test/prod)
- cleaner change management

## 15. Ports and Adapters Mental Model (Practical Architecture)

Treat abstraction as "port":
- domain depends on port interfaces
- concrete adapters implement ports (db/email/http/etc.)

Interview-friendly line:
- "Core logic depends inward on abstractions; details stay at the edges."

## 16. Abstraction Smells and Fixes

Smells:
- abstraction leaked by exposing implementation-specific details.
- too many tiny interfaces with no stable purpose.
- base class with many optional/not-used methods.

Fixes:
- keep contracts minimal and behavior-focused.
- split interfaces by caller needs.
- move vendor-specific details to adapter layer.
