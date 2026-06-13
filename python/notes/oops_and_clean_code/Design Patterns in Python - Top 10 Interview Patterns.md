# Design Patterns in Python - Top 10 Interview Patterns

## 1. How to Use This Note

For each pattern, you get:
1. when to use
2. where to use
3. how to use
4. an interview-style refactor question
5. a Python snippet with `print` so behavior is visible

---

## 1.1 All Practical Ways to Write Patterns in Python

Python allows multiple implementation styles for the same pattern.

### Way A: Classic OOP (ABC + classes)
- Best for interview clarity and large teams.
- Strong contracts and explicit structure.

```python
from abc import ABC, abstractmethod


class TaxStrategy(ABC):
    @abstractmethod
    def apply(self, amount):
        pass


class IndiaTax(TaxStrategy):
    def apply(self, amount):
        print("ABC strategy used")
        return amount * 1.18


print("Total:", IndiaTax().apply(100))
```

### Way B: Duck Typing (no inheritance, same method shape)
- Best when you want flexibility and less boilerplate.
- Pythonic for internal code where team discipline is good.

```python
class FlatTax:
    def apply(self, amount):
        print("Duck-typed strategy used")
        return amount + 20


def bill(amount, strategy):
    total = strategy.apply(amount)
    print("Total:", total)


bill(100, FlatTax())
```

### Way C: Function-Based Style (higher-order functions)
- Best for small algorithms and lightweight strategy/command.
- Less ceremony than classes.

```python
def weekend_discount(amount):
    print("Function strategy used")
    return amount * 0.9


def checkout(amount, discount_fn):
    final_amount = discount_fn(amount)
    print("Final amount:", final_amount)


checkout(500, weekend_discount)
```

### Way D: Data-Driven Registry (dict mapping)
- Best when types map to handlers and you want easy extension.
- Great for Factory/Command/Strategy lookups.

```python
def send_email(msg):
    print("EMAIL:", msg)


def send_sms(msg):
    print("SMS:", msg)


registry = {
    "email": send_email,
    "sms": send_sms,
}

registry["email"]("Welcome")
registry["sms"]("OTP 1234")
```

### Way E: Decorator Registration Style
- Best when plugins auto-register themselves.
- Common in frameworks and extensible systems.

```python
handlers = {}


def register(name):
    def wrapper(func):
        handlers[name] = func
        print(f"Registered handler: {name}")
        return func
    return wrapper


@register("pdf")
def export_pdf(data):
    print("Exporting PDF:", data)


handlers["pdf"]("sales-report")
```

### Way F: Metaclass or `__new__` Control
- Best only for advanced creation control (Singleton, class registration).
- Use rarely; harder to read for beginners.

```python
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Config created once via __new__")
        return cls._instance


print("Same?", Config() is Config())
```

### Way G: Async Variant (`async`/`await`)
- Best when pattern participants do I/O (network, DB, APIs).
- Observer, Strategy, Command are common async patterns.

```python
import asyncio


async def async_task(name):
    await asyncio.sleep(0.05)
    print("Async handler executed:", name)


async def main():
    await asyncio.gather(async_task("A"), async_task("B"))


asyncio.run(main())
```

### Way H: Thread-Safe Variant (locks/queue)
- Best when shared state is touched by multiple threads.
- Singleton, Producer-Consumer, Observer need synchronization.

```python
import threading


counter = 0
lock = threading.Lock()


def increase():
    global counter
    with lock:
        counter += 1
        print("Counter now:", counter)


t1 = threading.Thread(target=increase)
t2 = threading.Thread(target=increase)
t1.start()
t2.start()
t1.join()
t2.join()
```

## 1.2 When to Choose Which Way

Use this quick rule:
1. Start with Way A (Classic OOP) for interviews and shared codebases.
2. Use Way B or C for small/internal modules needing speed and simplicity.
3. Use Way D or E when behavior must be extensible via config/plugins.
4. Use Way G if work is I/O-bound and async stack already exists.
5. Use Way H if threads share mutable state.
6. Use Way F only if simpler approaches cannot express the requirement.

---

## 2. Singleton Pattern

### When to use
Use when only one shared instance should exist (for example config, logger).

### Where to use
- app-wide logger
- configuration loader
- connection registry

### How to use
1. hide direct multi-instance creation
2. keep one cached instance
3. return same instance every time

### Refactor interview question
Refactor this: "Multiple modules create multiple logger objects with inconsistent state."

### Python snippet
```python
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Creating Logger instance once")
        return cls._instance

    def log(self, message):
        print(f"[LOG] {message}")


logger1 = Logger()
logger2 = Logger()
print("Same instance?", logger1 is logger2)
logger1.log("Order created")
logger2.log("Payment received")
```

---

## 3. Factory Method Pattern

### When to use
Use when object creation depends on input type and caller should not know concrete class.

### Where to use
- parser selection by file type
- notification channel creation
- payment gateway selection

### How to use
1. define common interface
2. create concrete classes
3. centralize creation in factory

### Refactor interview question
Refactor this: "Code has many `if/elif` blocks creating different notification classes."

### Python snippet
```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailNotifier(Notifier):
    def send(self, message):
        print(f"EMAIL -> {message}")


class SmsNotifier(Notifier):
    def send(self, message):
        print(f"SMS -> {message}")


class NotifierFactory:
    @staticmethod
    def create(channel):
        if channel == "email":
            return EmailNotifier()
        if channel == "sms":
            return SmsNotifier()
        raise ValueError("Unsupported channel")


for ch in ["email", "sms"]:
    notifier = NotifierFactory.create(ch)
    notifier.send(f"Welcome via {ch}")
```

---

## 4. Strategy Pattern

### When to use
Use when one behavior has multiple interchangeable algorithms.

### Where to use
- discount engines
- tax calculation
- sorting/ranking modes

### How to use
1. create strategy interface
2. create algorithm classes
3. inject strategy into context

### Refactor interview question
Refactor this: "Checkout has `if user_type` for each discount rule."

### Python snippet
```python
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, amount):
        pass


class RegularDiscount(DiscountStrategy):
    def apply(self, amount):
        print("Applying 5% regular discount")
        return amount * 0.95


class PremiumDiscount(DiscountStrategy):
    def apply(self, amount):
        print("Applying 20% premium discount")
        return amount * 0.80


class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy

    def total(self, amount):
        final_amount = self.strategy.apply(amount)
        print("Final amount:", final_amount)


Checkout(RegularDiscount()).total(1000)
Checkout(PremiumDiscount()).total(1000)
```

---

## 5. Observer Pattern

### When to use
Use when one event should notify many dependent components.

### Where to use
- order placed event -> email, analytics, audit
- stock update -> UI refresh + cache update

### How to use
1. subject holds subscribers
2. subscribers implement update method
3. subject publishes event to all

### Refactor interview question
Refactor this: "OrderService directly calls email, sms, analytics one by one."

### Python snippet
```python
class Subject:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)
        print("Subscriber added:", observer.__class__.__name__)

    def notify(self, event):
        print("Notifying observers for event:", event)
        for observer in self._observers:
            observer.update(event)


class EmailObserver:
    def update(self, event):
        print(f"[EmailObserver] handled {event}")


class AnalyticsObserver:
    def update(self, event):
        print(f"[AnalyticsObserver] tracked {event}")


subject = Subject()
subject.subscribe(EmailObserver())
subject.subscribe(AnalyticsObserver())
subject.notify("order_placed")
```

---

## 6. Adapter Pattern

### When to use
Use when an existing class has incompatible interface but you must reuse it.

### Where to use
- integrating third-party SDK with different method name
- legacy APIs during migration

### How to use
1. keep target interface expected by app
2. wrap incompatible class in adapter
3. translate calls in adapter

### Refactor interview question
Refactor this: "New payment gateway exposes `make_payment()`, app expects `pay()`."

### Python snippet
```python
class LegacyGateway:
    def make_payment(self, amount):
        print(f"Legacy gateway paid: {amount}")


class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError


class LegacyGatewayAdapter(PaymentProcessor):
    def __init__(self, legacy_gateway):
        self.legacy_gateway = legacy_gateway

    def pay(self, amount):
        print("Adapter translating pay() -> make_payment()")
        self.legacy_gateway.make_payment(amount)


processor = LegacyGatewayAdapter(LegacyGateway())
processor.pay(2500)
```

---

## 7. Facade Pattern

### When to use
Use when subsystem is complex and you want one simple entry point.

### Where to use
- order placement workflow
- report generation pipeline
- deployment pipelines

### How to use
1. identify common workflow
2. create facade that calls subsystem steps in order
3. expose small API to client

### Refactor interview question
Refactor this: "Client manually calls inventory, payment, shipping in many places."

### Python snippet
```python
class InventoryService:
    def reserve(self, item_id):
        print(f"Inventory reserved for {item_id}")


class PaymentService:
    def charge(self, amount):
        print(f"Payment charged: {amount}")


class ShippingService:
    def ship(self, item_id):
        print(f"Shipment created for {item_id}")


class OrderFacade:
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()

    def place_order(self, item_id, amount):
        print("Order workflow started")
        self.inventory.reserve(item_id)
        self.payment.charge(amount)
        self.shipping.ship(item_id)
        print("Order workflow completed")


OrderFacade().place_order("ITEM-101", 1999)
```

---

## 8. Command Pattern

### When to use
Use when requests should be represented as objects (queue, undo, log).

### Where to use
- task queues
- undo/redo operations
- button click actions

### How to use
1. define command interface
2. create command objects
3. invoker executes command

### Refactor interview question
Refactor this: "UI button handler has huge `if action == ...` blocks."

### Python snippet
```python
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class Light:
    def on(self):
        print("Light turned ON")

    def off(self):
        print("Light turned OFF")


class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        print("Executing LightOnCommand")
        self.light.on()


class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        print("Executing LightOffCommand")
        self.light.off()


light = Light()
commands = [LightOnCommand(light), LightOffCommand(light)]
for cmd in commands:
    cmd.execute()
```

---

## 9. Template Method Pattern

### When to use
Use when algorithm steps are fixed but some steps vary by subclass.

### Where to use
- document export flow
- ETL pipeline steps
- report generation

### How to use
1. define base class with template flow
2. keep fixed steps in base
3. let subclasses override variable steps

### Refactor interview question
Refactor this: "CSV and JSON reports duplicate same workflow with small differences."

### Python snippet
```python
from abc import ABC, abstractmethod


class ReportTemplate(ABC):
    def generate(self, data):
        print("Step 1: validate data")
        self.validate(data)
        print("Step 2: format data")
        output = self.format_data(data)
        print("Step 3: save output")
        self.save(output)

    def validate(self, data):
        print("Common validation:", bool(data))

    @abstractmethod
    def format_data(self, data):
        pass

    def save(self, output):
        print("Saved output ->", output)


class CsvReport(ReportTemplate):
    def format_data(self, data):
        return ",".join(data)


class JsonReport(ReportTemplate):
    def format_data(self, data):
        return str({"items": data})


CsvReport().generate(["A", "B", "C"])
JsonReport().generate(["A", "B", "C"])
```

---

## 10. Decorator Pattern (Object Composition)

### When to use
Use when behavior should be added dynamically without changing original class.

### Where to use
- adding logging/caching/authorization around service
- feature toggles

### How to use
1. define component interface
2. keep base component
3. create wrappers that add behavior before/after delegate call

### Refactor interview question
Refactor this: "Base notifier class keeps growing with optional logging and encryption flags."

### Python snippet
```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass


class BasicNotifier(Notifier):
    def send(self, message):
        print("Basic send:", message)


class NotifierDecorator(Notifier):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def send(self, message):
        self.wrapped.send(message)


class LoggingDecorator(NotifierDecorator):
    def send(self, message):
        print("[LoggingDecorator] before send")
        super().send(message)
        print("[LoggingDecorator] after send")


class EncryptionDecorator(NotifierDecorator):
    def send(self, message):
        encrypted = f"enc({message})"
        print("[EncryptionDecorator] encrypted message created")
        super().send(encrypted)


notifier = LoggingDecorator(EncryptionDecorator(BasicNotifier()))
notifier.send("Payment done")
```

---

## 11. State Pattern

### When to use
Use when object behavior changes based on internal state and too many conditionals appear.

### Where to use
- order lifecycle: created, paid, shipped
- ticket workflow
- media player states

### How to use
1. create state interface
2. create concrete state classes
3. context delegates behavior to current state

### Refactor interview question
Refactor this: "Order class has large `if self.status == ...` in many methods."

### Python snippet
```python
from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def next(self, order):
        pass

    @abstractmethod
    def label(self):
        pass


class CreatedState(OrderState):
    def next(self, order):
        print("Transition: CREATED -> PAID")
        order.state = PaidState()

    def label(self):
        return "CREATED"


class PaidState(OrderState):
    def next(self, order):
        print("Transition: PAID -> SHIPPED")
        order.state = ShippedState()

    def label(self):
        return "PAID"


class ShippedState(OrderState):
    def next(self, order):
        print("Already SHIPPED, no next state")

    def label(self):
        return "SHIPPED"


class Order:
    def __init__(self):
        self.state = CreatedState()

    def advance(self):
        print("Current state:", self.state.label())
        self.state.next(self)
        print("New state:", self.state.label())


order = Order()
order.advance()
order.advance()
order.advance()
```

---

## 12. Fast Interview Revision

1. Singleton -> one shared instance
2. Factory Method -> centralize object creation
3. Strategy -> swap algorithms
4. Observer -> publish/subscribe notifications
5. Adapter -> interface conversion
6. Facade -> simplify complex subsystem
7. Command -> wrap requests as objects
8. Template Method -> fixed flow, variable steps
9. Decorator -> runtime behavior extension
10. State -> behavior changes by state

---

## 13. Pattern-by-Pattern: All Common Python Variants and Which One to Use

## 13.1 Singleton
- Variant 1: `__new__` singleton.
When: simple app-wide singleton.
- Variant 2: module-level singleton object.
When: easiest and most Pythonic for config/logging.
- Variant 3: metaclass singleton.
When: advanced framework-level control.
- Variant 4: thread-safe singleton with lock.
When: multithreaded access exists.

## 13.2 Factory Method
- Variant 1: class-based factory with `if/elif`.
When: few stable types, interview-friendly.
- Variant 2: registry factory (`dict` mapping).
When: many types and frequent extension.
- Variant 3: decorator auto-registration.
When: plugin architecture.

## 13.3 Strategy
- Variant 1: class strategies (ABC).
When: enterprise code, strict contracts.
- Variant 2: function strategies.
When: small algorithm swapping.
- Variant 3: async strategies.
When: API/network payment providers.

## 13.4 Observer
- Variant 1: sync observer list.
When: in-process immediate notifications.
- Variant 2: async observer (`asyncio.gather`).
When: I/O-bound subscribers.
- Variant 3: queue/message-bus observer.
When: decoupled services and reliability needs.

## 13.5 Adapter
- Variant 1: object adapter (composition).
When: safest default, wrap third-party object.
- Variant 2: class adapter (inheritance).
When: you control both classes and inheritance is safe.
- Variant 3: function adapter.
When: adapting simple callable signatures.

## 13.6 Facade
- Variant 1: thin facade (just ordering calls).
When: subsystem simple but repetitive.
- Variant 2: smart facade (validation/retry/logging).
When: orchestration logic is business-critical.
- Variant 3: async facade.
When: multiple service calls run concurrently.

## 13.7 Command
- Variant 1: command classes with `execute()`.
When: undo/redo, queue, audit required.
- Variant 2: function/lambda commands.
When: lightweight command dispatch.
- Variant 3: serialized commands.
When: distributed workers/process queues.

## 13.8 Template Method
- Variant 1: inheritance + overridable hooks.
When: fixed workflow and clear variation points.
- Variant 2: function pipeline steps.
When: simpler functional architecture preferred.
- Variant 3: mixin-assisted template.
When: shared optional hooks across templates.

## 13.9 Decorator Pattern
- Variant 1: object composition decorators.
When: add runtime behavior to objects.
- Variant 2: function decorators (`@decorator`).
When: cross-cutting function concerns (logging, timing).
- Variant 3: class decorators.
When: augment class capabilities at definition time.

## 13.10 State
- Variant 1: state classes.
When: many states/transitions and clean extension needed.
- Variant 2: enum + transition map.
When: small-medium workflows; lower complexity.
- Variant 3: table-driven state machine.
When: transitions loaded from config/rules.
