# Dependency Injection and Testability Mastery

## 1) Why DI Matters

Hardcoded dependencies make code rigid and hard to test.

Bad pattern:
- service creates DB/email/http clients internally.

Better:
- service receives dependencies through constructor/function params.

## 2) Constructor Injection Pattern

```python
class OrderService:
    def __init__(self, payment_gateway, notifier):
        self.payment_gateway = payment_gateway
        self.notifier = notifier

    def place_order(self, amount: float) -> None:
        txn = self.payment_gateway.charge(amount)
        self.notifier.send(f"order confirmed: {txn}")
```

## 3) Composition Root

Create and wire objects at one top-level location.

```python
def build_order_service():
    gateway = StripeGateway()
    notifier = EmailNotifier()
    return OrderService(gateway, notifier)
```

Core logic remains independent from wiring details.

## 4) Test Doubles

- fake: lightweight working implementation
- stub: predefined responses
- mock/spy: interaction verification

```python
class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-FAKE-1"
```

## 5) Boundary Segregation

Keep side effects at edges:
- domain logic: deterministic and pure where possible
- adapters: DB/API/file/email integrations

## 6) Contract Tests for Implementations

If multiple classes implement same contract:
- create shared behavior tests
- run against each implementation

This protects substitutability (LSP in practice).

## 7) DI Pitfalls

- over-injecting everything (noise)
- service-locator anti-pattern hidden global container
- unclear ownership/lifecycle of shared dependencies

## 8) Interview Questions

1. How DI improves unit testing?
2. Constructor vs function injection?
3. What is a composition root?
4. What are common DI anti-patterns?
