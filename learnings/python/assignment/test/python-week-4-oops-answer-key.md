# PYTHON WEEK 4 TEST - ANSWER KEY

Format: MCQ -> Option | Predict -> Exact output | Refactor -> One clean sample solution

## Section A: MCQ (1-40)

- Q1: **B**
- Q2: **B**
- Q3: **C**
- Q4: **B**
- Q5: **B**
- Q6: **B**
- Q7: **B**
- Q8: **B**
- Q9: **B**
- Q10: **A**
- Q11: **B**
- Q12: **B**
- Q13: **B**
- Q14: **B**
- Q15: **B**
- Q16: **B**
- Q17: **B**
- Q18: **B**
- Q19: **A**
- Q20: **B**
- Q21: **B**
- Q22: **B**
- Q23: **B**
- Q24: **B**
- Q25: **B**
- Q26: **B**
- Q27: **B**
- Q28: **B**
- Q29: **B**
- Q30: **B**
- Q31: **B**
- Q32: **A**
- Q33: **B**
- Q34: **B**
- Q35: **B**
- Q36: **B**
- Q37: **B**
- Q38: **B**
- Q39: **B**
- Q40: **B**

## Section B: Predict the Output (41-95)

### Q41
```text
base
```

### Q42
```text
100
```

### Q43
```text
B>A
```

### Q44
```text
['C', 'B', 'A', 'object']
```

### Q45
```text
Q1 P P
```

### Q46
```text
True
```

### Q47
```text
INFO ok
AUDIT ok
```

### Q48
```text
done
```

### Q49
```text
TypeError: Can't instantiate abstract class Broken without an implementation for abstract method 'run'
```

### Q50
```text
PUSH deploy
```

### Q51
```text
EMAIL x
SMS y
```

### Q52
```text
car-engine
```

### Q53
```text
500
400.0
```

### Q54
```text
{"m":"go"}
```

### Q55
```text
True True
```

### Q56
```text
BC
```

### Q57
```text
1 2 3
```

### Q58
```text
ok
```

### Q59
```text
bad
```

### Q60
```text
False
True
```

### Q61
```text
['x'] ['x']
```

### Q62
```text
['x'] []
```

### Q63
```text
csv
```

### Q64
```text
base
```

### Q65
```text
4 6
```

### Q66
```text
i:5
x
```

### Q67
```text
FILE cfg
```

### Q68
```text
True
```

### Q69
```text
C
```

### Q70
```text
['D', 'C', 'B', 'A', 'object']
```

### Q71
```text
saved neo
```

### Q72
```text
CBA
```

### Q73
```text
v=7
```

### Q74
```text
P-01
```

### Q75
```text
parent child
```

### Q76
```text
ok
```

### Q77
```text
B
```

### Q78
```text
x y
```

### Q79
```text
X
```

### Q80
```text
B
C
A
```

### Q81
```text
user missing
```

### Q82
```text
SLACK build
MAIL release
```

### Q83
```text
>=100 only
```

### Q84
```text
118.0
107.0
```

### Q85
```text
csv
```

### Q86
```text
True False
```

### Q87
```text
True
```

### Q88
```text
True
```

### Q89
```text
B
```

### Q90
```text
B A
```

### Q91
```text
ABC
```

### Q92
```text
TypeError
```

### Q93
```text
False True
```

### Q94
```text
['charge:300']
```

### Q95
```text
M1
```

## Section C: Quick Refactor (96-100)

### Q96
```python
from typing import Protocol, Any

class DatabasePort(Protocol):
    def connect(self) -> None: ...
    def insert(self, user: Any) -> None: ...

class UserService:
    def __init__(self, db: DatabasePort):
        self.db = db

    def create_user(self, u: Any) -> None:
        self.db.connect()
        self.db.insert(u)
```

### Q97
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> float: ...

class CardPayment(PaymentProcessor):
    def process(self, amount: float) -> float:
        return amount * 1.02

class UpiPayment(PaymentProcessor):
    def process(self, amount: float) -> float:
        return amount * 1.00

class WalletPayment(PaymentProcessor):
    def process(self, amount: float) -> float:
        return amount * 0.98

def process_payment(processor: PaymentProcessor, amount: float) -> float:
    return processor.process(amount)
```

### Q98
```python
class Payment:
    def pay(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("invalid")
        self._after_validation(amount)

    def _after_validation(self, amount: float) -> None:
        pass

class SpecialPayment(Payment):
    def __init__(self, min_for_offer: float = 1000):
        self.min_for_offer = min_for_offer

    def _after_validation(self, amount: float) -> None:
        if amount >= self.min_for_offer:
            # Extensible business behavior without tightening base preconditions
            self.apply_offer(amount)

    def apply_offer(self, amount: float) -> None:
        pass
```

### Q99
```python
from typing import Protocol

class Logger(Protocol):
    def log(self, message: str) -> None: ...

class OrderService:
    def __init__(self, logger: Logger):
        self.logger = logger

    def place(self, order_id: str) -> None:
        self.logger.log(order_id)
```

### Q100
```python
class Cart:
    def __init__(self):
        self.items = []

    def add(self, x):
        self.items.append(x)
```
