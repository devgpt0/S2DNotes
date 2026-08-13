# OOP and Clean Code Interview Case Studies
## 1. Core truth

Interview case studies are practice stories that show how to think about design, not just how to write code.
They are like rehearsing a real conversation before the interview happens.

```python
class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-1"

class PaymentService:
    def __init__(self, gateway) -> None:
        self.gateway = gateway

    def pay(self, amount: float) -> str:
        return self.gateway.charge(amount)

print(PaymentService(FakeGateway()).pay(25.0))
```

Output:

```text
TXN-1
```

The service depends on a gateway contract, so a fake gateway can stand in during testing or interview examples.

## 2. Case-study foundations

### Always start with clarification

Ask what must be true, what can change, and what the system must integrate with.

### Separate domain logic from infrastructure

Business rules should stay away from email, database, and HTTP details when possible.

### Describe the test strategy early

If the design is testable, that is usually a sign the boundaries are healthy.

## 3. Case-study method

### 8.1 Clarify invariants

Ask what the system must never allow.

### 8.2 Find variation points

Look for parts that may change often, such as providers, policies, or channels.

### 8.3 Pick contracts

Use small interfaces or protocols for replaceable behavior.

### 8.4 Choose composition

Prefer wiring objects together over deep inheritance when behavior differs.

### 8.5 Explain refactoring path

Show how a messy design could be improved without breaking behavior.

## 4. Practical design cases

### Example 1: Payment processing

```python
class FakeGateway:
    def charge(self, amount: float) -> str:
        return f"TXN-{int(amount)}"

class PaymentService:
    def __init__(self, gateway) -> None:
        self.gateway = gateway

    def pay(self, amount: float) -> str:
        return self.gateway.charge(amount)

print(PaymentService(FakeGateway()).pay(42.0))
```

Output:

```text
TXN-42
```

### Example 2: Notification system

```python
class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"email: {message}")

class PushNotifier:
    def send(self, message: str) -> None:
        print(f"push: {message}")

def notify(notifier, message: str) -> None:
    notifier.send(message)

notify(EmailNotifier(), "hello")
notify(PushNotifier(), "hello")
```

Output:

```text
email: hello
push: hello
```

### Example 3: Inventory domain

```python
class InventoryItem:
    def __init__(self, quantity: int) -> None:
        self.quantity = quantity

    def reserve(self, amount: int) -> None:
        if amount > self.quantity:
            raise ValueError("not enough stock")
        self.quantity -= amount

item = InventoryItem(5)
item.reserve(2)
print(item.quantity)
```

Output:

```text
3
```

- Payment systems often need gateway abstractions and retry policies.
- Notification systems often need channel selection and user preferences.
- Inventory systems often need explicit state transitions and invariants.
- Legacy systems often need gradual extraction instead of one huge rewrite.

## 5. Design-review mistakes

### Mistake 1: Jumping into classes before clarifying rules

Without invariants and boundaries, the design may solve the wrong problem.

### Mistake 2: Overusing inheritance

If behavior varies a lot, composition is usually easier to explain and test.

### Mistake 3: Ignoring testability

If the design is hard to fake or stub, the design is likely too coupled.

### Mistake 4: Refactoring the whole legacy system at once

Extract behavior step by step and keep the system working at each stage.

## 6. Design decision guide

| Situation | Strong choice | Why | Avoid when |
| --- | --- | --- | --- |
| Different providers with same action | composition + protocol | flexible and testable | the provider is the same forever |
| Shared behavior with real subtype meaning | inheritance | clear subtype relationship | behavior varies wildly |
| External dependency in tests | fake or stub | predictable tests | a real external call is needed |
| Messy legacy class | incremental extraction | safer than rewrite | the code path is trivial |

Selection rule:

- Design around invariants first.
- Use composition when behavior may vary.
- Use inheritance only when the subtype relationship is genuine.

## 7. Safety and maintainability

- In interviews, clarity matters more than fancy patterns.
- Keep the answer concrete and bounded.
- Mention tests and failure handling.
- Avoid promising abstractions that are not needed yet.

Best practices:

- State the domain rules first.
- Identify where real-world integrations happen.
- Explain how the design can grow without breaking the contract.

## 8. Advanced design tradeoffs

### Replace conditional with polymorphism

When many branches represent real business variation, a strategy object can be cleaner than a long `if/elif` chain.

### Incremental legacy refactoring

Extract pure logic first, then infrastructure, then presentation.

## 9. Mental model

| Case study | Main lesson |
| --- | --- |
| Payments | abstract the gateway |
| Notifications | separate channels and selection |
| Inventory | protect invariants |
| Legacy refactor | extract in small safe steps |

## 10. Put validation at the system boundary

Domain objects should receive already parsed values but still enforce their own
invariants. Transport adapters own JSON, HTTP, CSV, or database representation;
domain services own business decisions; infrastructure adapters own side effects.

Use this review order:

1. identify the external boundary and its strict schema;
2. identify the domain invariant that must always hold;
3. identify the side effect and the adapter that owns it;
4. inject the adapter through the composition root;
5. test the domain rule without the external system;
6. contract-test every real and fake adapter.

This prevents validation, retries, persistence, and business policy from being
mixed into one service class.
