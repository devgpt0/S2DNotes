# Encapsulation, Object State, Validation and Safe Classes

## 1. What Encapsulation Means

Encapsulation is the practice of:
- keeping data and behavior together inside a class
- protecting object state from unsafe direct changes
- exposing controlled operations instead of raw internal data

Core idea:
```text
Object = State + Behavior + Safety Rules
```

---

## 2. Why Encapsulation Is Needed

### Problem Without Encapsulation
```python
class BankAccount:
    def __init__(self, owner_name: str, balance: float):
        self.owner_name = owner_name
        self.balance = balance


account = BankAccount("John", 10000)
account.balance = -50000  # Invalid state
print(account.balance)
```
Issue:
- any code can break business rules
- invalid objects enter the system
- bugs appear later in unrelated parts of the app

Real-world invalid states:
- negative balance
- negative inventory
- empty customer ID
- invalid order status
- negative salary
---

## 3. Object State vs Behavior

Every object has:
- `state`: data it stores
- `behavior`: actions it performs

Example:
```python
class Product:
    def __init__(self, name: str, price: float):
        self.name = name      # state
        self.price = price    # state

    def apply_discount(self, percent: float) -> None:   # behavior
        self.price -= self.price * (percent / 100)
```

Rule:
- state should not be changed freely from outside
- behavior should enforce rules while changing state

---

## 4. Object Invariants (Most Important Concept)

Invariant = a rule that must always stay true for a valid object.

Examples:
- BankAccount: `balance >= 0`
- Product: `price > 0`
- Student: `0 <= marks <= 100`
- Employee: `salary >= 0`

### Bad Design
```python
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


product = Product("Laptop", -1000)  # invalid object created
```

### Better Design
```python
class Product:
    def __init__(self, name: str, price: float):
        if price <= 0:
            raise ValueError("Price must be positive")
        self.name = name
        self.price = price
```

Clean code rule:
```text
Never allow invalid objects to exist.
```

---

## 5. Public, Protected and Private in Python

### Public (`name`)
```python
class Student:
    def __init__(self):
        self.name = "John"
```

- accessible from anywhere
- safest only for truly public fields

### Protected (`_name`)
```python
class Student:
    def __init__(self):
        self._name = "John"
```

- convention: internal use
- still accessible, but should not be used directly outside the class

### Private (`__name`)
```python
class Student:
    def __init__(self):
        self.__name = "John"
```

Accessing `student.__name` raises `AttributeError`.

Why:
- Python applies name mangling  
- `__name` becomes `_Student__name`

Demo:
```python
student = Student()
print(student._Student__name)  # John
```

Important:
- private in Python means "harder to access"
- it does not mean "impossible to access"

---

## 6. Properties (`@property`) and Controlled Access

### Old Getter/Setter Style
```python
class Student:
    def __init__(self):
        self._name = ""

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value
```

Usage is verbose:
```python
student.set_name("Alice")
print(student.get_name())
```

### Pythonic Property Style
```python
class Student:
    def __init__(self, name: str):
        self.name = name  # calls setter

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value
```

Usage is clean:
```python
student = Student("Alice")
student.name = "Bob"  # validation runs automatically
print(student.name)
```

Why properties are powerful:
- attribute-like syntax for users
- method-level control for class designers
- validation can be added without breaking external API

---

## 7. Designing Safe APIs (Behavior Over Raw Mutation)

### Unsafe API
```python
account.balance -= 1000
product.quantity = -500
```

### Safe API
```python
account.withdraw(1000)
product.remove_stock(5)
```

Principle:
```text
Make correct usage easy. Make incorrect usage difficult.
```

### Example: Safe `BankAccount`
```python
class BankAccount:
    def __init__(self, owner_name: str, opening_balance: float):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")
        self.owner_name = owner_name
        self._balance = opening_balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount
```

---

## 8. Mini Project Pattern: Inventory Product Class

Requirements:
- attributes: `name`, `price`, `quantity`
- rules: `price > 0`, `quantity >= 0`
- methods: `add_stock`, `remove_stock`, `update_price`

Reference implementation:
```python
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

    def add_stock(self, units: int) -> None:
        if units <= 0:
            raise ValueError("Units must be positive")
        self._quantity += units

    def remove_stock(self, units: int) -> None:
        if units <= 0:
            raise ValueError("Units must be positive")
        if units > self._quantity:
            raise ValueError("Cannot remove more than available stock")
        self._quantity -= units

    def update_price(self, new_price: float) -> None:
        self.price = new_price
```

---

## 9. Refactoring Pattern (Before vs After)

### Before
```python
class Product:
    def __init__(self):
        self.price = 0
        self.quantity = 0
```

Issue:
- `product.price = -100` is allowed
- `product.quantity = -50` is allowed

### After
- use `_price` and `_quantity`
- enforce rules using properties
- expose safe methods for mutations

Result:
- object cannot easily enter invalid state
- class protects its own correctness

---

## 10. Encapsulation + Clean Code Principles

1. Protect invariants.
2. Hide implementation details.
3. Validate at boundaries (constructor, property setter, method input).
4. Keep methods small and intention-revealing.
5. Expose clear domain operations (`withdraw`, `transfer`, `remove_stock`) instead of direct field edits.

---

## 11. Interview Quick Notes

### What is encapsulation?
Protecting object state while exposing controlled behavior.

### Why use encapsulation?
To prevent invalid states and maintain object correctness.

### `_name` vs `__name`?
- `_name`: protected by convention
- `__name`: name mangled (`_ClassName__name`)

### What is a property?
A method pair (`getter/setter`) that behaves like an attribute and allows validation without changing public API usage.

---

## 12. Practice Task

Build a `BankAccount` system with:
- `deposit()`
- `withdraw()`
- `transfer()`

Rules:
- balance can never be negative
- all amounts must be positive
- use protected attributes
- use properties where needed
- keep methods small and meaningful
