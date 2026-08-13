# Polymorphism in Python: LSP and Clean Code

## 1. What Polymorphism Means

Polymorphism means one interface can support many implementations.

```text
Same operation name, object-specific behavior.
```

Example:
- `payment.process(amount)` works for card, UPI, wallet.
- caller code stays same, behavior changes by object type.

---

## 2. Why Polymorphism Is Important

Without polymorphism:
- long `if/elif` chains
- frequent edits in existing logic
- high risk of regression

With polymorphism:
- each class owns its own behavior
- client code becomes simpler
- new features usually mean "add class", not "edit many places"

This supports:
- abstraction
- clean API design
- Open/Closed Principle

---

## 3. Core Runtime Polymorphism (Method Overriding)

```python
from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CardPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"Card payment: {amount}")


class UpiPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"UPI payment: {amount}")


def checkout(payment: Payment, amount: float) -> None:
    payment.pay(amount)


checkout(CardPayment(), 1000)
checkout(UpiPayment(), 1000)
```

Output:

```text
Card payment: 1000
UPI payment: 1000
```

Output:

```text
Card payment: 1000
UPI payment: 1000
```

Key learning:
- `checkout` depends on contract (`Payment`), not concrete class.
- polymorphism happens at runtime based on object passed.

---

## 4. Duck Typing: Pythonic Polymorphism

Duck typing idea:
```text
If object has required behavior, use it.
```

```python
class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsNotifier:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def notify(notifier, message: str) -> None:
    notifier.send(message)


notify(EmailNotifier(), "Welcome")
notify(SmsNotifier(), "OTP sent")
```

Output:

```text
Email: Welcome
SMS: OTP sent
```

Output:

```text
Email: Welcome
SMS: OTP sent
```

No inheritance needed.

Use when:
- behavior contract is tiny
- dynamic flexibility matters

---

## 5. Hard Concept: Duck Typing vs ABC vs Protocol

### Duck typing
- runtime behavior-based compatibility
- minimal ceremony

### ABC (`abc.ABC`)
- explicit runtime contract
- best when you want strict base API

### Protocol (`typing.Protocol`)
- static structural contract for type checkers
- class does not need explicit inheritance

Quick guide:
- scripts/prototypes: duck typing
- team architecture: ABC
- strong typing with flexibility: Protocol

---

## 6. Protocol Example (Structural Typing)

```python
from typing import Protocol


class SupportsSend(Protocol):
    def send(self, message: str) -> None:
        ...


class PushNotifier:
    def send(self, message: str) -> None:
        print(f"Push: {message}")


def broadcast(notifier: SupportsSend, message: str) -> None:
    notifier.send(message)


broadcast(PushNotifier(), "Build complete")
```

Output:

```text
Push: Build complete
```

Output:

```text
Push: Build complete
```

Important:
- `PushNotifier` satisfies the protocol by shape, not inheritance.

---

## 7. Other Polymorphism Forms in Python

### Parametric polymorphism (Generics)
```python
from typing import TypeVar

T = TypeVar("T")


def first_item(items: list[T]) -> T:
    return items[0]


print(first_item([10, 20, 30]))
print(first_item(["A", "B", "C"]))
```

Output:

```text
10
A
```

Output:

```text
10
A
```

### Ad-hoc polymorphism (`singledispatch`)
```python
from functools import singledispatch


@singledispatch
def to_text(value) -> str:
    return str(value)


@to_text.register
def _(value: int) -> str:
    return f"int:{value}"


print(to_text(7))
print(to_text("hello"))
```

Output:

```text
int:7
hello
```

Output:

```text
int:7
hello
```

### Operator polymorphism
```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)


v1 = Vector(2, 3)
v2 = Vector(4, 5)
v3 = v1 + v2
print(v3.x, v3.y)
```

Output:

```text
6 8
```

Output:

```text
6 8
```

---

## 8. Built-in Python Polymorphism (Everyday Use)

Polymorphism already appears in standard Python:
- `len(obj)` -> `obj.__len__()`
- `for x in obj` -> iterator protocol
- `with obj` -> context manager protocol
- `obj()` -> callable protocol

If class implements expected methods, generic Python APIs work naturally.

---

## 9. Hard Concept: LSP (Liskov Substitution Principle)

LSP says:
```text
If code expects parent type, any child should work safely.
```

Child class should not:
- require stricter input than parent promised
- return incompatible output
- break parent behavior expectations

---

## 10. LSP Example: Good vs Bad

### Good
Parent contract: `process(amount)` accepts positive amount.
All child classes process positive amount without surprise.

### Bad
One child suddenly rejects valid parent input.

```python
class Payment:
    def pay(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")


class SpecialPayment(Payment):
    def pay(self, amount: float) -> None:
        if amount < 1000:  # stricter than parent, can violate expectations
            raise ValueError("amount must be >= 1000")


try:
    SpecialPayment().pay(500)
except ValueError as error:
    print(error)
```

Output:

```text
amount must be >= 1000
```

Output:

```text
amount must be >= 1000
```

If caller expects parent behavior, this child may break workflow.

---

## 11. Contract Design for Safe Polymorphism

When designing parent interface:
1. define input rules clearly
2. define output/side-effect expectations
3. define error behavior
4. keep contract minimal and stable

When implementing child classes:
1. honor parent preconditions
2. keep return behavior compatible
3. avoid surprise side effects

---

## 12. Clean Code Rules for Polymorphic Design

1. Replace `if/elif type` logic with dispatch through objects.
2. Depend on abstraction (`ABC`/`Protocol`), not concrete classes.
3. Keep method names and semantics consistent across children.
4. Keep child classes focused and small.
5. Add feature via new class, avoid editing stable client code.
6. Document contract once at parent level.
7. Write contract tests for every implementation.

---

## 13. Refactor Pattern: Conditional Logic to Polymorphism

Before:
```python
def generate_report(kind: str, data: dict) -> str:
    if kind == "pdf":
        return f"PDF:{data}"
    if kind == "csv":
        return f"CSV:{data}"
    if kind == "json":
        return f"JSON:{data}"
    raise ValueError("Unsupported report type")


print(generate_report("pdf", {"id": 1}))
```

Output:

```text
PDF:{'id': 1}
```

Output:

```text
PDF:{'id': 1}
```

After:
```python
from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class PdfReportGenerator(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"PDF:{data}"


class CsvReportGenerator(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"CSV:{data}"


class JsonReportGenerator(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"JSON:{data}"


def export(generator: ReportGenerator, data: dict) -> str:
    return generator.generate(data)


print(export(PdfReportGenerator(), {"id": 1}))
print(export(CsvReportGenerator(), {"id": 1}))
print(export(JsonReportGenerator(), {"id": 1}))
```

Output:

```text
PDF:{'id': 1}
CSV:{'id': 1}
JSON:{'id': 1}
```

Output:

```text
PDF:{'id': 1}
CSV:{'id': 1}
JSON:{'id': 1}
```

---

## 14. Polymorphism + Composition (Real-World Pattern)

You often combine polymorphism with composition:
- service class accepts interface in constructor
- runtime decides implementation

```python
from typing import Protocol


class Payment(Protocol):
    def pay(self, amount: float) -> None: ...


class CardPayment:
    def pay(self, amount: float) -> None:
        print(f"Card payment: {amount}")


class OrderService:
    def __init__(self, payment: Payment):
        self.payment = payment

    def place_order(self, amount: float) -> None:
        self.payment.pay(amount)


service = OrderService(CardPayment())
service.place_order(2500)
```

Output:

```text
Card payment: 2500
```

Benefits:
- low coupling
- easy testing with fake/mock implementations

---

## 15. Testing Polymorphism Correctly

Test levels:
1. Contract tests for all implementations.
2. Child-specific edge case tests.
3. Integration tests through parent interface.

Contract test example idea:
- same test function runs for every payment implementation
- verifies behavior for valid/invalid input

---

## 16. Common Beginner Mistakes

1. Confusing inheritance with polymorphism.
2. Keeping type-check branches after creating subclasses.
3. Adding many tiny classes with unclear contract.
4. Violating LSP by changing child semantics.
5. Choosing inheritance where simple functions would do.
6. Forgetting to test all implementations against same contract.

---

## 17. When Not to Use Polymorphism

Avoid polymorphic hierarchy when:
- only one behavior exists and likely to stay one
- differences are tiny and not stable
- simple dictionary/map dispatch is enough
- hierarchy adds more complexity than value

Rule:
- prefer simplest design that remains extensible.

---

## 18. Interview Quick Revision

1. Polymorphism = one interface, many implementations.
2. Python supports it via overriding, duck typing, protocols, dunder methods.
3. LSP ensures safe substitution of child for parent.
4. ABC provides explicit contract; Protocol provides structural contract.
5. Best benefit: remove type-condition branches and improve extensibility.

---

## 19. One-Page Summary

- Polymorphism keeps client code clean and stable.
- Duck typing is flexible; ABC and Protocol add contract clarity.
- LSP is non-negotiable for safe design.
- Contract tests are key for reliability.
- Add new behavior by adding classes, not editing old branches.

---
