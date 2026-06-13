# SOLID Principles in Python (Easy Notes + Interview Ready)

## 1. Why SOLID Matters

SOLID helps us write classes that are:
- easy to understand
- easy to test
- easy to extend without breaking old code

Think of SOLID as design guardrails for clean OOP.

---

## 2. S - Single Responsibility Principle (SRP)

One class should have one clear reason to change.

Example:
```python
class Invoice:
    def __init__(self, customer: str, amount: float):
        self.customer = customer
        self.amount = amount


class InvoiceCalculator:
    TAX_RATE = 0.18

    def total_with_tax(self, invoice: Invoice) -> float:
        return invoice.amount * (1 + self.TAX_RATE)


class InvoicePrinter:
    def print_invoice(self, invoice: Invoice, total: float) -> None:
        print(f"Invoice for {invoice.customer}: base={invoice.amount}, total={total}")


invoice = Invoice("Asha", 1000)
calculator = InvoiceCalculator()
printer = InvoicePrinter()

total = calculator.total_with_tax(invoice)
printer.print_invoice(invoice, total)
```

Expected output:
```text
Invoice for Asha: base=1000, total=1180.0
```

Why SRP here:
- calculation logic and printing logic are separated

---

## 3. O - Open/Closed Principle (OCP)

Open for extension, closed for modification.

Add new behavior by adding new classes, not by editing stable old logic.

Example:
```python
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CardPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Card payment processed: {amount}")


class UpiPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"UPI payment processed: {amount}")


def checkout(amount: float, method: PaymentMethod) -> None:
    print("Starting checkout...")
    method.pay(amount)
    print("Checkout complete")


checkout(1200, CardPayment())
checkout(1200, UpiPayment())
```

Expected output:
```text
Starting checkout...
Card payment processed: 1200
Checkout complete
Starting checkout...
UPI payment processed: 1200
Checkout complete
```

Why OCP here:
- new payment type = new class, `checkout` stays unchanged

---

## 4. L - Liskov Substitution Principle (LSP)

If child class is used instead of parent, program should still work correctly.

Example:
```python
from abc import ABC, abstractmethod


class DeliveryPartner(ABC):
    @abstractmethod
    def deliver(self, package_id: str) -> str:
        pass


class BikeDelivery(DeliveryPartner):
    def deliver(self, package_id: str) -> str:
        return f"Bike partner delivered package {package_id}"


class DroneDelivery(DeliveryPartner):
    def deliver(self, package_id: str) -> str:
        return f"Drone partner delivered package {package_id}"


def dispatch(partner: DeliveryPartner, package_id: str) -> None:
    status = partner.deliver(package_id)
    print(status)


dispatch(BikeDelivery(), "PKG101")
dispatch(DroneDelivery(), "PKG102")
```

Expected output:
```text
Bike partner delivered package PKG101
Drone partner delivered package PKG102
```

Why LSP here:
- `dispatch()` works with any `DeliveryPartner` child without special checks

---

## 5. I - Interface Segregation Principle (ISP)

Clients should not depend on methods they do not use.

Use small focused interfaces instead of one giant interface.

Example:
```python
from abc import ABC, abstractmethod


class Workable(ABC):
    @abstractmethod
    def work(self) -> str:
        pass


class Eatable(ABC):
    @abstractmethod
    def eat(self) -> str:
        pass


class HumanWorker(Workable, Eatable):
    def work(self) -> str:
        return "Human is coding"

    def eat(self) -> str:
        return "Human is eating lunch"


class RobotWorker(Workable):
    def work(self) -> str:
        return "Robot is assembling parts"


def start_shift(worker: Workable) -> None:
    print(worker.work())


def lunch_break(person: Eatable) -> None:
    print(person.eat())


human = HumanWorker()
robot = RobotWorker()

start_shift(human)
start_shift(robot)
lunch_break(human)
```

Expected output:
```text
Human is coding
Robot is assembling parts
Human is eating lunch
```

Why ISP here:
- robot is not forced to implement `eat()`

---

## 6. D - Dependency Inversion Principle (DIP)

High-level modules should depend on abstractions, not concrete classes.

Example:
```python
from abc import ABC, abstractmethod


class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailSender(MessageSender):
    def send(self, message: str) -> None:
        print(f"EMAIL -> {message}")


class SmsSender(MessageSender):
    def send(self, message: str) -> None:
        print(f"SMS -> {message}")


class OrderService:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    def place_order(self, order_id: str) -> None:
        print(f"Order placed: {order_id}")
        self.sender.send(f"Your order {order_id} is confirmed")


email_service = OrderService(EmailSender())
sms_service = OrderService(SmsSender())

email_service.place_order("ORD-5001")
sms_service.place_order("ORD-5002")
```

Expected output:
```text
Order placed: ORD-5001
EMAIL -> Your order ORD-5001 is confirmed
Order placed: ORD-5002
SMS -> Your order ORD-5002 is confirmed
```

Why DIP here:
- `OrderService` depends on `MessageSender` abstraction, not hardcoded email/sms class

---

## 7. Interview Memory Trick

- S: one class, one job
- O: add new class, do not edit stable old class
- L: child should safely replace parent
- I: small interfaces, no forced methods
- D: depend on abstraction, inject dependency

---

## 8. Mini Practice

Try redesigning a notification module with:
- channels: email, sms, slack
- user preferences
- retry policy

Goal:
- add new channel without changing existing business flow
- keep each class focused
