# Dependency Injection and Testability
## 1. Core truth

Dependency injection means giving an object the things it depends on instead of creating those things inside the object.
It is like handing a worker the right tools instead of hiding the tools in a locked room.

```python
class OrderService:
    def __init__(self, payment_gateway, notifier) -> None:
        self.payment_gateway = payment_gateway
        self.notifier = notifier

    def place_order(self, amount: float) -> str:
        txn = self.payment_gateway.charge(amount)
        self.notifier.send(f"order confirmed: {txn}")
        return txn

class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-FAKE-1"

class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)

notifier = FakeNotifier()
service = OrderService(FakeGateway(), notifier)
print(service.place_order(25.0))
print(notifier.messages)
```

Output:

```text
TXN-FAKE-1
['order confirmed: TXN-FAKE-1']
```

The service does not create real external dependencies. It uses the fake gateway and notifier that were injected into it.

## 2. Injection foundations

### Constructor injection keeps services replaceable

```python
class OrderService:
    def __init__(self, payment_gateway, notifier) -> None:
        self.payment_gateway = payment_gateway
        self.notifier = notifier

    def place_order(self, amount: float) -> str:
        txn = self.payment_gateway.charge(amount)
        self.notifier.send(f"order confirmed: {txn}")
        return txn

class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-FAKE-1"

class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)

notifier = FakeNotifier()
service = OrderService(FakeGateway(), notifier)
print(service.place_order(25.0))
print(notifier.messages)
```

Output:

```text
TXN-FAKE-1
['order confirmed: TXN-FAKE-1']
```

Practical takeaway: inject the things that vary or talk to the outside world.

### Function injection is useful for small operations

```python
def send_receipt(send_message, order_id: str) -> str:
    message = f"receipt for {order_id}"
    send_message(message)
    return message

messages: list[str] = []

def fake_send_message(message: str) -> None:
    messages.append(message)

print(send_receipt(fake_send_message, "ORD-1"))
print(messages)
```

Output:

```text
receipt for ORD-1
['receipt for ORD-1']
```

Practical takeaway: inject functions when the behavior is small and direct.

### The composition root wires the system together

```python
def build_order_service() -> str:
    return "wired"

print(build_order_service())
```

Output:

```text
wired
```

Practical takeaway: create real dependencies in one place at the edge of the program.

## 3. Injection styles and test doubles

### Constructor injection

Pass dependencies through `__init__`.

### Function injection

Pass dependencies as function arguments.

### Fakes

Use a simple working implementation that behaves predictably in tests.

### Contract tests

Use the same test suite to verify every implementation of the same interface.

```python
class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-FAKE-1"

print(FakeGateway().charge(10.0))
```

Output:

```text
TXN-FAKE-1
```

## 4. Practical dependency boundaries

### Example 1: Testable payment flow

```python
class PaymentService:
    def __init__(self, gateway) -> None:
        self.gateway = gateway

    def pay(self, amount: float) -> str:
        return self.gateway.charge(amount)

class FakeGateway:
    def charge(self, amount: float) -> str:
        return "TXN-123"

print(PaymentService(FakeGateway()).pay(42.0))
```

Output:

```text
TXN-123
```

### Example 2: Inject a notifier

```python
class Notifier:
    def send(self, message: str) -> None:
        print(message)

class OrderService:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def confirm(self) -> None:
        self.notifier.send("order confirmed")

OrderService(Notifier()).confirm()
```

Output:

```text
order confirmed
```

### Example 3: Swap implementations without changing the service

```python
class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"email: {message}")

class SmsNotifier:
    def send(self, message: str) -> None:
        print(f"sms: {message}")

def notify_user(notifier, message: str) -> None:
    notifier.send(message)

notify_user(EmailNotifier(), "hello")
notify_user(SmsNotifier(), "hello")
```

Output:

```text
email: hello
sms: hello
```

- Inject database clients, HTTP clients, message senders, and payment gateways.
- Keep domain logic pure when possible.
- Put wiring in one place instead of scattering object creation everywhere.
- Use fakes in tests to avoid slow or flaky external calls.

## 5. Dependency-injection mistakes

### Mistake 1: Creating dependencies inside the service

That makes the class harder to test and harder to replace.

### Mistake 2: Using a hidden service locator

If the dependency comes from a global container, the code becomes less explicit.

### Mistake 3: Injecting too much

If every tiny thing is injected, the code becomes noisy and hard to read.

### Mistake 4: Mixing business rules and infrastructure setup

Keep the rule in the service and the setup in the composition root.

## 6. Injection decision guide

| Style | Best use | Why | Avoid when |
| --- | --- | --- | --- |
| Constructor injection | object-based services | explicit and testable | the dependency is a one-off function |
| Function injection | small helpers | very simple and direct | the logic is a large stateful object |
| Service locator | almost never | hides wiring | you want clear dependencies |
| Composition root | application startup | centralizes wiring | you are inside business logic |

Selection rule:

- Use constructor injection for most services.
- Use function injection for simple stateless helpers.
- Keep the composition root at the outer edge of the system.

## 7. Safety and maintainability

- DI improves testability and flexibility, but too much indirection adds noise.
- Keep external effects at the boundary of the system.
- Prefer explicit dependencies over hidden global state.
- Use the smallest design that makes the code easy to test.

Best practices:

- Inject what varies.
- Keep objects focused on one job.
- Use fakes for tests that would otherwise touch external systems.

## 8. Contract tests and boundaries

### Boundary segregation

Domain logic should stay as deterministic as possible.
Adapters for databases, files, and APIs should live at the edges.

### Contract tests

If several classes claim to implement the same behavior, run the same tests against all of them.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| Injection | pass dependencies in |
| Constructor injection | best default for services |
| Function injection | good for small helpers |
| Composition root | wire objects at the edge |
| Fake | predictable test replacement |
| Contract test | same behavior, many implementations |

## 10. Structural dependency contracts

A `Protocol` describes only the behavior the service needs and avoids forcing
infrastructure classes into a shared inheritance tree.

```python
from typing import Protocol


class Clock(Protocol):
    def now(self) -> int: ...


class FixedClock:
    def now(self) -> int:
        return 100


def expires_at(clock: Clock, ttl: int) -> int:
    return clock.now() + ttl


print(expires_at(FixedClock(), 30))
```

Output:

```text
130
```

Keep protocol methods minimal and domain-oriented. Verify real adapters and
fakes with the same contract tests; static compatibility does not prove matching
semantics.
