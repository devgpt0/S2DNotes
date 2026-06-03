# Worksheet 2: Encapsulation + Abstraction 


## Interview-Oriented Weightage Strategy

### By question type
| Type | Range | Count | Weight |
| --- | --- | --- | --- |
| MCQ fundamentals | 1-40 | 40 | 20% |
| Code reading / output prediction | 41-90 | 50 | 25% |
| Debugging / refactoring / safe API fixes | 91-150 | 60 | 30% |
| Interview-style design and explanation | 151-200 | 50 | 25% |

### By concept focus
| Concept | Count | Weight |
| --- | --- | --- |
| Encapsulation | 110 | 55% |
| Abstraction | 90 | 45% |

---

## Section A: MCQ (1-40)

1. Encapsulation primarily helps to:
- **A.** Increase syntax complexity
- **B.** Protect object state and invariants
- **C.** Remove all methods
- **D.** Avoid class usage

2. Which rule is a valid invariant for `BankAccount`?
- **A.** `balance <= 0`
- **B.** `balance >= 0`
- **C.** `owner_name is None`
- **D.** `withdraw` always fails

3. In Python, `_balance` usually means:
- **A.** Fully private and inaccessible
- **B.** Protected by convention (internal use)
- **C.** Global constant
- **D.** Deprecated syntax

4. `__balance` is transformed internally by Python into:
- **A.** `balance__`
- **B.** `_ClassName__balance`
- **C.** `_balance_`
- **D.** `ClassName.balance`

5. Main benefit of `@property` is:
- **A.** Disabling validation
- **B.** Attribute-like access with method control
- **C.** Replacing constructors
- **D.** Making code procedural

6. Best place to validate input for `price` updates:
- **A.** In comments only
- **B.** In a property setter or domain method
- **C.** In random external script
- **D.** Never validate

7. Which API is safer?
- **A.** `account.balance -= 500`
- **B.** `account.withdraw(500)`
- **C.** `account._balance = -1`
- **D.** `account.__dict__["balance"] = -5`

8. Encapsulation is most closely related to:
- **A.** Preventing invalid state
- **B.** Increasing inheritance depth
- **C.** Replacing all functions
- **D.** Avoiding tests

9. Which class design is better?
- **A.** Public writable attributes for all business data
- **B.** Protected attributes + validated methods
- **C.** No methods, only fields
- **D.** Manual dictionary updates everywhere

10. A clean encapsulated class should:
- **A.** Trust every caller blindly
- **B.** Guard boundaries and enforce rules
- **C.** Expose internals by default
- **D.** Skip constructor validation

11. Abstraction means:
- **A.** Hiding syntax errors
- **B.** Showing essentials and hiding complexity
- **C.** Replacing classes with tuples
- **D.** Using only private methods

12. Best abstraction for coffee workflow:
- **A.** `heat_water(); grind_beans(); mix(); extract()`
- **B.** `make_coffee()`
- **C.** `do_step_1()`
- **D.** `process()`

13. Abstraction mainly reduces:
- **A.** CPU usage only
- **B.** Cognitive load for users of API
- **C.** Number of files
- **D.** Need for naming

14. Public methods of a class are often called:
- **A.** Stack frames
- **B.** API surface
- **C.** Bytecode
- **D.** Name manglers

15. Which method name is most intuitive?
- **A.** `do()`
- **B.** `handle()`
- **C.** `calculate_salary()`
- **D.** `process_data_2()`

16. In ABC, `@abstractmethod` indicates:
- **A.** Optional override
- **B.** Must be implemented by subclass
- **C.** Static-only function
- **D.** Private class method

17. Which statement is true for abstract classes?
- **A.** They can always be instantiated
- **B.** They define contracts for subclasses
- **C.** They cannot have methods
- **D.** They remove polymorphism

18. Better dependency choice:
- **A.** `UserService -> EmailNotification`
- **B.** `UserService -> Notification (ABC)`
- **C.** `UserService -> if/elif channel everywhere`
- **D.** `UserService -> global functions only`

19. Encapsulation vs Abstraction:
- **A.** Both are exactly same
- **B.** Encapsulation protects state; Abstraction hides complexity
- **C.** Encapsulation hides complexity; Abstraction protects memory only
- **D.** Neither matters in Python

20. Which is a better API for storage?
- **A.** `open_conn(); write_block(); flush(); close_conn()`
- **B.** `save(path, content)`
- **C.** `step1(); step2(); step3()`
- **D.** `raw_sql_write()`

21. Best invariant for `Student.marks`:
- **A.** `marks < 0`
- **B.** `0 <= marks <= 100`
- **C.** `marks >= 1000`
- **D.** `marks is str`

22. A class that allows `quantity = -50` likely violates:
- **A.** abstraction
- **B.** encapsulation
- **C.** polymorphism
- **D.** iteration

23. Name mangling is intended to:
- **A.** encrypt data
- **B.** avoid accidental access/collision
- **C.** speed up loops
- **D.** replace type hints

24. Which is an abstraction smell?
- **A.** clear method names
- **B.** API requiring users to remember internal sequence
- **C.** single entrypoint for common behavior
- **D.** strong contracts

25. A good property setter should:
- **A.** ignore invalid values
- **B.** silently coerce all data
- **C.** validate and raise meaningful errors
- **D.** write to global state

26. Which is a contract-first design?
- **A.** Start with concrete class only
- **B.** Define `PaymentProcessor(ABC)` then implementations
- **C.** Avoid interfaces entirely
- **D.** Use one huge class

27. Which is a poor API method name?
- **A.** `withdraw()`
- **B.** `transfer()`
- **C.** `process_user_payment()`
- **D.** `do_it_now()`

28. If user must know 8 internal methods to send email, this violates:
- **A.** readability only
- **B.** abstraction quality
- **C.** constructor rules
- **D.** import conventions

29. Encapsulation boundary checks usually happen in:
- **A.** constructors, property setters, domain methods
- **B.** only main function
- **C.** random print blocks
- **D.** comments

30. Which class is easier to misuse?
- **A.** only behavior methods exposed
- **B.** direct writable internals + no validation
- **C.** protected attributes + invariants
- **D.** explicit error handling

31. Abstraction in frameworks often looks like:
- **A.** low-level socket handling in user code
- **B.** declarative high-level API methods
- **C.** manual SQL and HTTP parsing in each handler
- **D.** no reuse

32. Why use abstraction in large teams?
- **A.** To increase accidental coupling
- **B.** To standardize usage and reduce mental overhead
- **C.** To remove module boundaries
- **D.** To avoid design reviews

33. Which is best for extensibility?
- **A.** giant `if/elif` in one service
- **B.** shared abstract contract + plugin implementations
- **C.** copy-paste classes
- **D.** hardcoded provider calls

34. A method named `handle()` usually:
- **A.** is perfectly clear always
- **B.** may hide intent and hurt API clarity
- **C.** replaces abstraction concerns
- **D.** enforces invariants

35. A safe transfer API should validate:
- **A.** amount sign only
- **B.** sender balance only
- **C.** amount positive + sufficient balance + valid receiver
- **D.** none

36. Which is true about abstraction and testing?
- **A.** Abstractions make tests impossible
- **B.** Abstractions can improve testability through contracts
- **C.** Only concrete classes can be mocked
- **D.** ABCs remove need for unit tests

37. Good abstraction should be:
- **A.** clever and cryptic
- **B.** minimal and intention-revealing
- **C.** deeply nested
- **D.** full of side effects

38. Which is the best interview answer for encapsulation?
- **A.** "It hides everything."
- **B.** "It protects state by controlling access and mutation."
- **C.** "It means inheritance."
- **D.** "It avoids methods."

39. Which is best interview answer for abstraction?
- **A.** "It removes classes."
- **B.** "It offers simple interfaces by hiding implementation details."
- **C.** "It only works in Java."
- **D.** "It avoids design."

40. Which pair is strongest for production OOP?
- **A.** public fields + unclear methods
- **B.** encapsulation + abstraction
- **C.** globals + long scripts
- **D.** no validation + no contracts

---

## Section B: Code Reading / Predict Output (41-90)

41.
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

print(BankAccount(500).balance)
```

42.
```python
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("invalid")
        self._price = value

print(Product(10).price)
```

43.
```python
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("invalid")
        self._price = value

Product(-1)
```

44.
```python
class Student:
    def __init__(self):
        self.__name = "Asha"

s = Student()
print(hasattr(s, "__name"), hasattr(s, "_Student__name"))
```

45.
```python
class Student:
    def __init__(self):
        self.__name = "Ravi"

s = Student()
print(s._Student__name)
```

46.
```python
class Wallet:
    def __init__(self, amount):
        self._amount = amount

    def spend(self, value):
        if value > self._amount:
            raise ValueError("insufficient")
        self._amount -= value

w = Wallet(100)
w.spend(40)
print(w._amount)
```

47.
```python
class Counter:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    def increment(self):
        self._value += 1

c = Counter()
c.increment()
c.increment()
print(c.value)
```

48.
```python
class Employee:
    def __init__(self, salary):
        self.salary = salary

e = Employee(50000)
e.salary = -100
print(e.salary)
```

49.
```python
class SafeEmployee:
    def __init__(self, salary):
        self.salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("negative")
        self._salary = value

e = SafeEmployee(50000)
e.salary = 60000
print(e.salary)
```

50.
```python
class SafeEmployee:
    def __init__(self, salary):
        self.salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("negative")
        self._salary = value

e = SafeEmployee(50000)
e.salary = -1
```

51.
```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("bad amount")
        if amount > self._balance:
            raise ValueError("insufficient")
        self._balance -= amount

a = Account(100)
a.withdraw(100)
print(a._balance)
```

52.
```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("bad amount")
        self._balance += amount

a = Account(50)
a.deposit(25)
print(a._balance)
```

53.
```python
class Profile:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name.title()

p = Profile("alex")
print(p.name)
```

54.
```python
class Product:
    def __init__(self, quantity):
        self._quantity = quantity

    def remove_stock(self, units):
        if units > self._quantity:
            raise ValueError("too much")
        self._quantity -= units

p = Product(5)
p.remove_stock(2)
print(p._quantity)
```

55.
```python
class Product:
    def __init__(self, quantity):
        self._quantity = quantity

    def remove_stock(self, units):
        if units > self._quantity:
            raise ValueError("too much")
        self._quantity -= units

p = Product(5)
p.remove_stock(8)
```

56.
```python
class User:
    def __init__(self):
        self._active = False

    @property
    def is_active(self):
        return self._active

u = User()
print(u.is_active)
```

57.
```python
class User:
    def __init__(self):
        self._active = False

    def activate(self):
        self._active = True

u = User()
u.activate()
print(u._active)
```

58.
```python
class A:
    def __init__(self):
        self.__x = 10

a = A()
print(a.__dict__)
```

59.
```python
class Bank:
    def transfer(self, sender_balance, amount):
        if amount <= 0:
            raise ValueError("bad amount")
        if amount > sender_balance:
            raise ValueError("insufficient")
        return sender_balance - amount

print(Bank().transfer(1000, 250))
```

60.
```python
class Config:
    def __init__(self):
        self._timeout = 30

    @property
    def timeout(self):
        return self._timeout

c = Config()
print(c.timeout)
```

61.
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        pass

PaymentProcessor()
```

62.
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class UPI(PaymentProcessor):
    def process(self, amount):
        return f"UPI:{amount}"

print(UPI().process(500))
```

63.
```python
from abc import ABC, abstractmethod

class N(ABC):
    @abstractmethod
    def send(self):
        pass

class Email(N):
    pass

Email()
```

64.
```python
from abc import ABC, abstractmethod

class N(ABC):
    @abstractmethod
    def send(self):
        pass

class SMS(N):
    def send(self):
        print("sms")

SMS().send()
```

65.
```python
class CoffeeMachine:
    def make_coffee(self):
        return self._heat() + self._brew()

    def _heat(self):
        return 1

    def _brew(self):
        return 2

print(CoffeeMachine().make_coffee())
```

66.
```python
class API:
    def run(self):
        return "simple"

api = API()
print(api.run())
```

67.
```python
class EmailService:
    def send_email(self):
        return "sent"

print(EmailService().send_email())
```

68.
```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def read(self, path):
        pass

class Local(Storage):
    def read(self, path):
        return f"read:{path}"

s = Local()
print(s.read("a.txt"))
```

69.
```python
class LocalStorage:
    def save(self, path, content):
        return f"saved:{path}:{len(content)}"

print(LocalStorage().save("x.txt", "hello"))
```

70.
```python
class Car:
    def start(self):
        return "engine_started"

print(Car().start())
```

71.
```python
class PaymentGateway:
    def pay(self, amount):
        return amount > 0

print(PaymentGateway().pay(0))
```

72.
```python
class Report:
    def generate(self):
        return "ok"

print(hasattr(Report(), "generate"))
```

73.
```python
from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def execute(self):
        pass

class FastProcessor(Processor):
    def execute(self):
        return "fast"

print(FastProcessor().execute())
```

74.
```python
class A:
    def do(self):
        return "A"

class B(A):
    pass

print(B().do())
```

75.
```python
class Notification:
    def send(self):
        return "base"

class Push(Notification):
    def send(self):
        return "push"

n = Push()
print(n.send())
```

76.
```python
class Builder:
    def build(self):
        return {"status": "done"}

print(Builder().build()["status"])
```

77.
```python
from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    def delete(self, path):
        pass

class S3Storage(FileStorage):
    def delete(self, path):
        return f"deleted:{path}"

print(S3Storage().delete("a"))
```

78.
```python
class Service:
    def step1(self):
        return 1

    def step2(self):
        return 2

    def run(self):
        return self.step1() + self.step2()

print(Service().run())
```

79.
```python
class HumanAPI:
    def speak(self):
        return "hello"

print(HumanAPI().speak().upper())
```

80.
```python
class Payment:
    def process(self, amount):
        if amount <= 0:
            raise ValueError("invalid")
        return "processed"

print(Payment().process(1))
```

81.
```python
class Payment:
    def process(self, amount):
        if amount <= 0:
            raise ValueError("invalid")
        return "processed"

Payment().process(0)
```

82.
```python
class Gateway:
    def connect(self):
        return True

    def send(self):
        return "sent"

print(Gateway().connect(), Gateway().send())
```

83.
```python
class UserRepo:
    def save(self, user):
        return f"saved:{user}"

print(UserRepo().save("tom"))
```

84.
```python
class Calculator:
    def add(self, a, b):
        return a + b

print(Calculator().add(10, -3))
```

85.
```python
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read(self):
        pass

class CsvReader(Reader):
    def read(self):
        return ["row1", "row2"]

print(len(CsvReader().read()))
```

86.
```python
class Facade:
    def execute(self):
        return self._a() + self._b()

    def _a(self):
        return "A"

    def _b(self):
        return "B"

print(Facade().execute())
```

87.
```python
class APIClient:
    def request(self):
        return {"ok": True}

print(APIClient().request()["ok"])
```

88.
```python
class AbstractLike:
    def process(self):
        raise NotImplementedError

class Impl(AbstractLike):
    def process(self):
        return 123

print(Impl().process())
```

89.
```python
class ImplOnly:
    def process(self):
        return "x"

obj = ImplOnly()
print(callable(obj.process))
```

90.
```python
class StorageFacade:
    def save(self, path):
        return f"ok:{path}"

print(StorageFacade().save("notes.txt"))
```

---

## Section C: Debug / Refactor / Improve Design (91-150)

91. Refactor to prevent negative balance:
```python
class Account:
    def __init__(self, balance):
        self.balance = balance
```

92. Refactor to prevent negative salary updates:
```python
class Employee:
    def __init__(self, salary):
        self.salary = salary
```

93. Replace direct mutation with safe API:
```python
account.balance -= amount
```

94. Add invariant checks for product price and quantity:
```python
class Product:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
```

95. Convert getter/setter style to property style:
```python
class Student:
    def get_name(self): ...
    def set_name(self, name): ...
```

96. Improve naming and safety:
```python
class A:
    def f(self, x):
        self.b = x
```

97. Refactor to protect internal list state:
```python
class Cart:
    def __init__(self):
        self.items = []
```

98. Make this API harder to misuse:
```python
order.status = "shipped"
```

99. Refactor with meaningful domain methods:
```python
inventory.quantity = inventory.quantity - n
```

100. Add validation to property setter:
```python
class User:
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value
```

101. Fix unsafe constructor:
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance
```

102. Improve encapsulation for transfer:
```python
sender._balance -= amount
receiver._balance += amount
```

103. Refactor to hide implementation:
```python
machine.heat()
machine.grind()
machine.extract()
```

104. Design a single high-level method for this workflow:
```python
service.connect()
service.authenticate()
service.send()
service.disconnect()
```

105. Replace vague method names with intent-revealing names:
```python
class UserService:
    def do(self): ...
```

106. Convert giant if/elif payment handler into abstraction:
```python
if mode == "upi": ...
elif mode == "card": ...
elif mode == "netbanking": ...
```

107. Create ABC contract from this incomplete class:
```python
class PaymentProcessor:
    pass
```

108. Fix subclass that forgot abstract method:
```python
class Email(Notification):
    pass
```

109. Refactor for dependency on abstraction, not concrete:
```python
class UserService:
    def __init__(self):
        self.notifier = EmailNotification()
```

110. Improve this API by reducing steps:
```python
storage.open()
storage.write()
storage.commit()
storage.close()
```

111. Refactor this abstraction smell:
```python
class Report:
    def step1(self): ...
    def step2(self): ...
    def step3(self): ...
```

112. Add template/facade method for clean usage:
```python
class Pipeline:
    def load(self): ...
    def clean(self): ...
    def export(self): ...
```

113. Protect invariant `0 <= marks <= 100`:
```python
class Student:
    def __init__(self, marks):
        self._marks = marks
```

114. Fix direct external state access:
```python
employee._salary = -5000
```

115. Refactor to avoid exposing internals:
```python
print(order._status_history)
```

116. Improve this constructor with boundary validation:
```python
class Coupon:
    def __init__(self, discount_percent):
        self.discount_percent = discount_percent
```

117. Add guarded API for stock removal:
```python
product.quantity -= units
```

118. Refactor to avoid external sequence dependency:
```python
payment.connect()
payment.prepare()
payment.execute()
payment.finalize()
```

119. Create a cleaner abstraction for login:
```python
auth.fetch_user()
auth.verify_password()
auth.create_session()
```

120. Replace magic `process()` with specific behavior names:
```python
class Payroll:
    def process(self): ...
```

121. Refactor to separate WHAT from HOW:
```python
invoice.write_sql()
invoice.commit()
```

122. Add abstraction for notification channels:
```python
send_email(message)
send_sms(message)
send_push(message)
```

123. Refactor this to hide networking details:
```python
client.create_socket()
client.send_bytes()
client.close_socket()
```

124. Improve with an interface-driven design:
```python
class LocalStorage:
    def save(self, path, content): ...
```

125. Design an ABC for analytics exporters (`csv`, `json`, `db`).

126. Refactor to avoid duplicated validation in three methods.

127. Introduce private helper methods behind one public API.

128. Replace public writable config with validated properties.

129. Refactor class with too many public internals into clean surface.

130. Create an abstraction for payment retry strategy.

131. Turn this into safer API with explicit method:
```python
loan.interest_rate = -3
```

132. Add an invariant for transaction amount (`> 0`) everywhere needed.

133. Refactor to avoid accidental misuse by method ordering.

134. Design a single method that orchestrates five private steps.

135. Replace concrete logger dependency with `Logger` abstraction.

136. Refactor this class to remove `send_email`, `send_sms`, `send_push` duplication.

137. Add property setter validation for non-empty customer ID.

138. Enforce valid status transitions (`CREATED -> PAID -> SHIPPED`) safely.

139. Move business rule checks from controller to domain object.

140. Refactor to prevent partial update states during transfer.

141. Introduce `Notification(ABC)` and make concrete channels implement it.

142. Refactor `FileManager` into `FileStorage` abstraction + implementations.

143. Replace `if provider == ...` with polymorphism.

144. Hide serialization details behind `serialize()` API.

145. Introduce `Repository` abstraction for data persistence operations.

146. Refactor code that leaks SQL details to service layer.

147. Design safe API for `close_account()` that checks pending dues.

148. Add abstraction for report generation with interchangeable formats.

149. Refactor with guard clauses and remove nested validation blocks.

150. Rewrite one messy class into:
- protected state
- validated setters/methods
- clear high-level API
- one ABC-based extension point

---

## Section D: Interview-Style Questions (151-200)

151. Define encapsulation in one line and give one production example.

152. Define abstraction in one line and give one framework example.

153. Explain encapsulation vs abstraction with one class example.

154. Why is direct public mutation of business fields risky?

155. What is an object invariant? Give three examples.

156. Where should invariant checks live and why?

157. When do you choose `@property` over explicit getter/setter methods?

158. Explain `_name` vs `__name` and name mangling.

159. Why is Python private "difficult" and not "impossible" access?

160. Design a safe `BankAccount` API for deposit, withdraw, transfer.

161. How would you prevent invalid state in constructor and during updates?

162. Give an interview-friendly example of "make incorrect usage difficult."

163. How do you decide what should be public vs protected/private?

164. What are signs that a class violates encapsulation?

165. What is cognitive load in API usage? Give one bad and one good API.

166. Why are vague method names (`do`, `handle`, `process`) harmful?

167. What makes an API intuitive for new team members?

168. Explain how abstraction improves onboarding speed in teams.

169. What is an abstract class in Python?

170. Why cannot abstract classes be instantiated?

171. What role does `@abstractmethod` play in architecture?

172. Give one example where ABC prevents runtime design drift.

173. Explain polymorphism using payment processors.

174. Refactor strategy: concrete dependency to abstraction dependency.

175. How does abstraction reduce coupling?

176. Give a real-world analogy for abstraction beyond coding.

177. Which is better and why: one huge class vs contract + implementations?

178. How do abstractions support open/closed design?

179. What are common anti-patterns while applying abstraction?

180. What are common anti-patterns while applying encapsulation?

181. Design question: Create an abstraction for multi-cloud storage API.

182. Design question: Build notification module supporting new channels.

183. Design question: Prevent invalid state in an order lifecycle.

184. Write a short interface for payment and three implementations.

185. How would you unit test encapsulation rules?

186. How would you unit test abstraction contracts?

187. What tests would you write for property setters?

188. How would you ensure transfer operation is atomic and safe?

189. Explain how to migrate from procedural workflow API to one façade method.

190. In review, how do you spot weak abstraction quickly?

191. In review, how do you spot missing invariants quickly?

192. Discuss trade-off: too much abstraction vs not enough abstraction.

193. Discuss trade-off: strict encapsulation vs developer convenience.

194. How can logs and error messages support safe encapsulated APIs?

195. Explain dependency inversion using `Notification(ABC)` example.

196. How would you add a new payment type without modifying old classes?

197. How do you document abstraction boundaries for teammates?

198. What metrics/signals indicate abstraction quality improved?

199. What metrics/signals indicate encapsulation quality improved?

200. Final interview prompt: Design a mini fintech core using both encapsulation and abstraction. Explain decisions and trade-offs.

---

## Capstone Project (Outside the 200 Questions)

### Project: Unified Payments and Notifications Core

Build a mini system that combines both **Encapsulation** and **Abstraction** strongly.

### Domain Modules
1. `BankAccount` (Encapsulation-heavy)
2. `PaymentProcessor` (ABC abstraction)
3. `Notification` (ABC abstraction)
4. `TransactionService` (orchestration layer)

### Functional Requirements
1. `BankAccount` must support:
   - `deposit(amount)`
   - `withdraw(amount)`
   - `transfer(amount, target_account)`
2. Invariants:
   - balance never negative
   - amount always positive
   - account id non-empty
3. `PaymentProcessor` abstraction:
   - `process_payment(amount, source, target)`
   - implementations: `UPIPayment`, `CardPayment`, `NetBankingPayment`
4. `Notification` abstraction:
   - `send(message, user_id)`
   - implementations: `EmailNotification`, `SMSNotification`, `PushNotification`
5. `TransactionService` should:
   - use abstractions (not concrete classes hardcoded)
   - perform payment
   - trigger notification
   - capture failures with meaningful errors

### Technical Constraints
1. Use `ABC` and `@abstractmethod`.
2. Use protected attributes and validated properties where meaningful.
3. Avoid direct field mutation outside domain methods.
4. Keep methods small and intent-revealing.
5. No giant `if/elif` chains for provider selection in core flow.

### Deliverables
1. `models.py` (`BankAccount`, value objects if any)
2. `payments.py` (ABC + implementations)
3. `notifications.py` (ABC + implementations)
4. `services.py` (`TransactionService`)
5. `test_*.py` with at least:
   - invariant tests
   - abstraction contract tests
   - failure path tests
6. `README.md` with:
   - API usage examples
   - design decisions
   - 5 interview talking points

### Evaluation Rubric (Interview Style)
- 30% encapsulation correctness (invariants and safety)
- 30% abstraction quality (contracts and extensibility)
- 20% API clarity and naming
- 20% test quality and edge-case handling

### Stretch Goals
1. Add `RefundProcessor` abstraction.
2. Add `AuditLogger` abstraction.
3. Add retry policy abstraction for transient failures.
