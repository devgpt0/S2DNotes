# Worksheet 3: Inheritance + Polymorphism + Composition vs Inheritance

## Interview-Oriented Weightage Strategy

### By question type
| Type | Range | Count | Weight |
| --- | --- | --- | --- |
| MCQ fundamentals | 1-40 | 40 | 20% |
| Code reading / output prediction | 41-90 | 50 | 25% |
| Debugging / refactoring / design fixes | 91-150 | 60 | 30% |
| Interview-style explanation and architecture | 151-200 | 50 | 25% |

### By concept focus
| Concept | Count | Weight |
| --- | --- | --- |
| Inheritance + MRO + `super()` | 70 | 35% |
| Polymorphism + LSP + contracts | 70 | 35% |
| Composition vs Inheritance + clean design | 60 | 30% |

---

## Section A: MCQ (1-40)

1. Inheritance should primarily be used when:
- **A.** two classes have similar method names
- **B.** there is a true `is-a` relationship
- **C.** we want fewer files
- **D.** we dislike constructors

2. Which statement best describes composition?
- **A.** one class extends another class
- **B.** one class hides all methods
- **C.** one class contains/uses another class
- **D.** one class must be abstract

3. `super()` in Python calls:
- **A.** only direct parent always
- **B.** next method in MRO order
- **C.** child method recursively
- **D.** random parent method

4. MRO stands for:
- **A.** Method Runtime Object
- **B.** Multiple Route Override
- **C.** Method Resolution Order
- **D.** Module Resolution Operator

5. In `class D(B, C)`, method lookup starts from:
- **A.** `A`
- **B.** `object`
- **C.** `D` then MRO sequence
- **D.** alphabetical order

6. Diamond problem in inheritance is handled in Python by:
- **A.** disabling multiple inheritance
- **B.** C3 linearization (MRO)
- **C.** static linking
- **D.** importing `diamond` module

7. Which is generally safer for changing behavior at runtime?
- **A.** deep inheritance
- **B.** composition
- **C.** global variable flags
- **D.** copy-paste classes

8. Child method that changes parent behavior is called:
- **A.** overloading
- **B.** overriding
- **C.** encapsulation
- **D.** composition

9. Which is an inheritance smell?
- **A.** shallow hierarchy
- **B.** deep class chain with fragile parent
- **C.** stable base contract
- **D.** contract tests

10. Best use of mixin:
- **A.** huge domain class replacement
- **B.** single reusable behavior
- **C.** database connection singleton
- **D.** replacing all composition

11. Polymorphism means:
- **A.** one class only one method
- **B.** same interface, different implementations
- **C.** no methods in child classes
- **D.** always using `if/elif`

12. Duck typing relies on:
- **A.** explicit inheritance only
- **B.** runtime behavior compatibility
- **C.** private attributes
- **D.** decorators only

13. `typing.Protocol` provides:
- **A.** SQL abstraction
- **B.** structural typing contract
- **C.** runtime encryption
- **D.** exception hierarchy

14. LSP means:
- **A.** child class must be larger than parent
- **B.** child should safely substitute parent
- **C.** parent should call child directly
- **D.** class names must match

15. Which likely violates LSP?
- **A.** child accepts broader input
- **B.** child preserves parent contract
- **C.** child adds stricter preconditions unexpectedly
- **D.** child keeps same return type behavior

16. Best way to remove `if type == ...` chains:
- **A.** add more `elif`
- **B.** move behavior into polymorphic classes
- **C.** use global flags
- **D.** avoid methods

17. Which dependency is better for extensibility?
- **A.** `OrderService -> CardPayment`
- **B.** `OrderService -> Payment(ABC/Protocol)`
- **C.** `OrderService -> if/elif provider`
- **D.** `OrderService -> global function`

18. Composition usually improves:
- **A.** coupling
- **B.** rigidity
- **C.** testability and replaceability
- **D.** inheritance depth

19. Which relationship is correct for inheritance?
- **A.** `Car is an Engine`
- **B.** `Car has an Engine`
- **C.** `Manager is an Employee`
- **D.** `Order has a PaymentService`

20. Which relationship is correct for composition?
- **A.** `Square is a Shape`
- **B.** `CardPayment is a Payment`
- **C.** `UserService has a Logger`
- **D.** `Dog is an Animal`

21. Why avoid calling overridable methods in parent `__init__`?
- **A.** it increases comments
- **B.** child state may be uninitialized
- **C.** Python forbids override
- **D.** it reduces speed

22. Which is true about `__private` attributes in Python?
- **A.** impossible to access
- **B.** transformed using name mangling
- **C.** same as `_protected`
- **D.** global by default

23. Best hierarchy design guideline:
- **A.** as deep as possible
- **B.** shallow and stable
- **C.** one base class for all domain concepts
- **D.** no testing needed

24. `singledispatch` is mainly used for:
- **A.** inheritance
- **B.** ad-hoc function polymorphism by type
- **C.** private methods
- **D.** constructors

25. Operator overloading (`__add__`, `__eq__`) is:
- **A.** inheritance only
- **B.** a form of polymorphic behavior
- **C.** impossible in Python
- **D.** unrelated to OOP

26. Which is a clean parent class?
- **A.** very large class with optional behavior for all children
- **B.** minimal stable contract-focused base
- **C.** class with random utility methods
- **D.** class with unknown side effects

27. In multiple inheritance, cooperative behavior requires:
- **A.** direct parent calls with class names everywhere
- **B.** consistent `super()` usage
- **C.** avoiding constructors
- **D.** avoiding method overrides

28. Which design is easiest to unit test?
- **A.** hardcoded concrete dependencies
- **B.** dependency injection with abstractions
- **C.** deep global state
- **D.** large static methods only

29. Composition vs inheritance default in business services should be:
- **A.** inheritance first always
- **B.** composition first, inheritance where true hierarchy exists
- **C.** no classes at all
- **D.** random choice

30. Which is a red flag?
- **A.** `PaymentService` takes `Payment` abstraction
- **B.** each child implementation tested
- **C.** parent changes frequently break all children
- **D.** clear method naming

31. Which line best reflects runtime polymorphism?
- **A.** `payment = CardPayment(); payment.pay(100)`
- **B.** `if payment_type == "card": ...`
- **C.** `print("pay")`
- **D.** `pass`

32. Which improves API clarity?
- **A.** `do()`
- **B.** `handle()`
- **C.** `process_payment()`
- **D.** `run2()`

33. LSP-safe child implementation should:
- **A.** break parent output expectations
- **B.** require extra mandatory arguments
- **C.** preserve parent behavior contract
- **D.** throw random new exceptions always

34. Which is best statement?
- **A.** inheritance and polymorphism are same thing
- **B.** polymorphism can exist via duck typing without inheritance
- **C.** composition removes need for abstractions
- **D.** LSP is optional for production

35. `Protocol` helps most with:
- **A.** runtime prevention of all errors
- **B.** static contract checking with structural typing
- **C.** replacing unit tests
- **D.** avoiding naming

36. Which is not a clean-code goal in these topics?
- **A.** lower coupling
- **B.** easier extension
- **C.** unclear method names
- **D.** safer contracts

37. Which is a good interview answer?
- **A.** "I always use inheritance"
- **B.** "I choose between composition and inheritance using IS-A vs HAS-A"
- **C.** "LSP is theoretical only"
- **D.** "MRO never matters"

38. A child class that throws error for previously valid parent input likely breaks:
- **A.** DRY
- **B.** LSP
- **C.** SRP
- **D.** naming conventions

39. Which approach best supports adding a new payment type?
- **A.** edit large if/elif block
- **B.** create new class implementing payment contract
- **C.** duplicate old class
- **D.** modify database schema first

40. Strongest combination for scalable OOP design:
- **A.** deep inheritance + concrete coupling
- **B.** composition + polymorphic contracts + LSP discipline
- **C.** global state + utility scripts
- **D.** no abstractions

---

## Section B: Code Reading / Predict Output (41-90)

41.
```python
class Animal:
    def speak(self):
        return "sound"

class Dog(Animal):
    def speak(self):
        return "bark"

print(Dog().speak())
```

42.
```python
class Employee:
    def __init__(self, name):
        self.name = name

class Manager(Employee):
    def __init__(self, name, team_size):
        super().__init__(name)
        self.team_size = team_size

m = Manager("Asha", 6)
print(m.name, m.team_size)
```

43.
```python
class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B"

class C(A):
    def who(self):
        return "C"

class D(B, C):
    pass

print(D().who())
```

44.
```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

print([cls.__name__ for cls in D.mro()])
```

45.
```python
class Base:
    role = "base"

class Child(Base):
    pass

c = Child()
print(c.role)
c.role = "local"
print(c.role, Base.role)
```

46.
```python
class Parent:
    def __init__(self):
        self._x = 10
        self.__y = 20

class Child(Parent):
    def show(self):
        return self._x

print(Child().show())
```

47.
```python
class Parent:
    def __init__(self):
        self.__y = 20

p = Parent()
print("_Parent__y" in p.__dict__)
```

48.
```python
class Logger:
    def log(self, msg):
        print("INFO", msg)

class AuditLogger(Logger):
    def log(self, msg):
        super().log(msg)
        print("AUDIT", msg)

AuditLogger().log("paid")
```

49.
```python
class A:
    def process(self):
        print("A")

class B(A):
    def process(self):
        print("B-start")
        super().process()
        print("B-end")

class C(A):
    def process(self):
        print("C-start")
        super().process()
        print("C-end")

class D(B, C):
    pass

D().process()
```

50.
```python
class Payment:
    def pay(self, amount):
        raise NotImplementedError

class CardPayment(Payment):
    def pay(self, amount):
        print(f"Card:{amount}")

def checkout(payment, amount):
    payment.pay(amount)

checkout(CardPayment(), 500)
```

51.
```python
class EmailNotifier:
    def send(self, msg):
        print("EMAIL", msg)

class SmsNotifier:
    def send(self, msg):
        print("SMS", msg)

def notify(n, msg):
    n.send(msg)

notify(EmailNotifier(), "hello")
notify(SmsNotifier(), "otp")
```

52.
```python
from typing import Protocol

class SupportsSend(Protocol):
    def send(self, message: str) -> None:
        ...

class PushNotifier:
    def send(self, message: str) -> None:
        print("PUSH", message)

def broadcast(n: SupportsSend, msg: str):
    n.send(msg)

broadcast(PushNotifier(), "build done")
```

53.
```python
class Payment:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("invalid")
        print("ok")

Payment().pay(1)
```

54.
```python
class Payment:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("invalid")
        print("ok")

Payment().pay(0)
```

55.
```python
class Engine:
    def start(self):
        return "engine started"

class Car:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        return "car -> " + self.engine.start()

print(Car(Engine()).start())
```

56.
```python
class ConsoleLogger:
    def log(self, msg):
        print("CONSOLE", msg)

class Service:
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        self.logger.log("running")

Service(ConsoleLogger()).run()
```

57.
```python
from functools import singledispatch

@singledispatch
def show(value):
    return str(value)

@show.register
def _(value: int):
    return f"int:{value}"

print(show(3))
print(show("x"))
```

58.
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v = Vector(1, 2) + Vector(3, 4)
print(v.x, v.y)
```

59.
```python
class ReportGenerator:
    def generate(self, data):
        raise NotImplementedError

class PdfReportGenerator(ReportGenerator):
    def generate(self, data):
        return f"PDF:{data}"

print(PdfReportGenerator().generate({"id": 1}))
```

60.
```python
class A:
    category = "A"

class B(A):
    pass

b1 = B()
b2 = B()
b1.category = "B1"
print(b1.category, b2.category, B.category)
```

61.
```python
class Base:
    def action(self):
        return "base"

class Child(Base):
    pass

print(Child().action())
```

62.
```python
class Parent:
    def __init__(self):
        self.value = 5

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.value += 2

print(Child().value)
```

63.
```python
class Parent:
    def greet(self):
        return "hello"

class Child(Parent):
    def greet(self):
        return super().greet() + " world"

print(Child().greet())
```

64.
```python
class Payment:
    def pay(self, amount):
        print(f"PAY {amount}")

class SpecialPayment(Payment):
    def pay(self, amount):
        if amount < 1000:
            raise ValueError("amount must be >= 1000")
        print(f"SPECIAL {amount}")

try:
    SpecialPayment().pay(500)
except ValueError as e:
    print(e)
```

65.
```python
class Payment:
    def pay(self, amount):
        print(f"PAY {amount}")

class CardPayment(Payment):
    def pay(self, amount):
        print(f"CARD {amount}")

class UpiPayment(Payment):
    def pay(self, amount):
        print(f"UPI {amount}")

for p in [CardPayment(), UpiPayment()]:
    p.pay(100)
```

66.
```python
class TimestampMixin:
    def touch(self):
        self.updated = True

class User(TimestampMixin):
    pass

u = User()
print(hasattr(u, "updated"))
u.touch()
print(hasattr(u, "updated"))
```

67.
```python
class Database:
    def connect(self):
        return "connected"

class UserService:
    def __init__(self, db):
        self.db = db

    def create(self, name):
        print(self.db.connect())
        print("created", name)

UserService(Database()).create("ravi")
```

68.
```python
class A:
    def __init__(self, **kwargs):
        self.a = 1
        super().__init__(**kwargs)

class B(A):
    def __init__(self, **kwargs):
        self.b = 2
        super().__init__(**kwargs)

class C:
    def __init__(self, **kwargs):
        self.c = 3
        super().__init__(**kwargs)

class D(B, C):
    pass

d = D()
print(d.a, d.b, d.c)
```

69.
```python
class A:
    def x(self):
        return "A"

class B(A):
    pass

class C(B):
    pass

print(C().x())
```

70.
```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

print(Rectangle(3, 4).area())
```

71.
```python
class ConsoleLogger:
    def log(self, msg):
        print("C", msg)

class JsonLogger:
    def log(self, msg):
        print(f'{{"msg":"{msg}"}}')

class Service:
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        self.logger.log("ok")

Service(JsonLogger()).run()
```

72.
```python
class A:
    def ping(self):
        return "A"

class B(A):
    def ping(self):
        return "B" + super().ping()

print(B().ping())
```

73.
```python
class Parent:
    def work(self):
        return "parent"

class Child(Parent):
    pass

obj = Child()
print(isinstance(obj, Parent), isinstance(obj, Child))
```

74.
```python
class Parent:
    pass

class Child(Parent):
    pass

print(issubclass(Child, Parent))
```

75.
```python
class Payment:
    pass

class CardPayment(Payment):
    pass

print(issubclass(CardPayment, Payment))
```

76.
```python
class Engine:
    def start(self):
        return "start"

class Bike:
    def __init__(self):
        self.engine = Engine()

print(Bike().engine.start())
```

77.
```python
class A:
    def who(self):
        return "A"

class B:
    def who(self):
        return "B"

class C(A, B):
    pass

print(C().who())
```

78.
```python
class A:
    pass

class B(A):
    pass

class C(B):
    pass

print([cls.__name__ for cls in C.mro()])
```

79.
```python
class FakeLogger:
    def __init__(self):
        self.messages = []

    def log(self, msg):
        self.messages.append(msg)

class BillingService:
    def __init__(self, logger):
        self.logger = logger

    def bill(self, amount):
        self.logger.log(f"Billed {amount}")

f = FakeLogger()
BillingService(f).bill(300)
print(f.messages)
```

80.
```python
class A:
    def run(self):
        print("A")

class B(A):
    def run(self):
        print("B")
        super().run()

B().run()
```

81.
```python
class Processor:
    def process(self, amount):
        return amount * 2

class FastProcessor(Processor):
    def process(self, amount):
        return super().process(amount) + 1

print(FastProcessor().process(10))
```

82.
```python
class Parent:
    def __init__(self):
        self._value = 10

class Child(Parent):
    def get(self):
        return self._value

print(Child().get())
```

83.
```python
class Parent:
    def __init__(self):
        self.__value = 10

class Child(Parent):
    def get(self):
        return hasattr(self, "_Parent__value")

print(Child().get())
```

84.
```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

print(first([9, 8, 7]))
print(first(["a", "b"]))
```

85.
```python
class Payment:
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("invalid")
        return "paid"

class ChildPayment(Payment):
    pass

print(ChildPayment().pay(10))
```

86.
```python
class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError

class NoDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount

class FestivalDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.9

print(NoDiscount().apply(1000))
print(FestivalDiscount().apply(1000))
```

87.
```python
class A:
    def __init__(self):
        self.tags = []

a1 = A()
a2 = A()
a1.tags.append("x")
print(a1.tags, a2.tags)
```

88.
```python
class A:
    tags = []

a1 = A()
a2 = A()
a1.tags.append("x")
print(a1.tags, a2.tags)
```

89.
```python
class Service:
    def __init__(self, processor):
        self.processor = processor

    def execute(self, amount):
        return self.processor.process(amount)

class P:
    def process(self, amount):
        return amount + 5

print(Service(P()).execute(10))
```

90.
```python
class A:
    def ping(self):
        return "A"

class B(A):
    def ping(self):
        return "B"

class C(B):
    pass

print(C().ping())
```

---

## Section C: Debug / Refactor / Improve Design (91-150)

91. Refactor this misuse of inheritance to composition:
```python
class UserService(Database):
    pass
```

92. Refactor to ensure child constructor properly initializes parent state:
```python
class Manager(Employee):
    def __init__(self, team_size):
        self.team_size = team_size
```

93. Refactor this fragile parent that mixes too many responsibilities.

94. Convert this `if/elif role` bonus logic into inheritance/polymorphism.

95. Refactor a deep hierarchy (`A -> B -> C -> D -> E`) into a cleaner design.

96. Add a safe abstract base contract for payment processors.

97. Fix this child signature mismatch with parent contract.

98. Refactor direct parent class calls to cooperative `super()`.

99. Fix potential MRO issues in a multiple inheritance constructor chain.

100. Refactor to avoid calling overridable methods inside parent `__init__`.

101. Convert this hardcoded dependency to composition + dependency injection:
```python
self.logger = ConsoleLogger()
```

102. Replace concrete dependency with abstraction (`ABC` or `Protocol`).

103. Refactor class with `do()`, `handle()`, `process()` into intent-revealing API.

104. Convert `if provider == ...` payment flow to polymorphic strategy objects.

105. Add LSP-safe behavior to child classes that currently reject valid parent inputs.

106. Refactor this class explosion into simpler composition where appropriate.

107. Add contract tests for all `Payment` implementations.

108. Refactor duck-typed module with no checks into Protocol-driven typed design.

109. Improve this code by replacing inheritance with strategy composition.

110. Add mixin correctly for reusable timestamp behavior.

111. Remove state-heavy constructor logic from mixin and redesign cleanly.

112. Refactor parent class to document extension points clearly.

113. Create a fake dependency for unit testing this service method.

114. Refactor mutable shared class attribute bug:
```python
class Student:
    tags = []
```

115. Improve this class to satisfy LSP without changing client code.

116. Split one broad interface into smaller role-focused abstractions.

117. Refactor to support runtime behavior swap without changing service code.

118. Convert inheritance-based logger hierarchy to composition where needed.

119. Refactor this pattern:
```python
if isinstance(x, A):
    ...
elif isinstance(x, B):
    ...
```
into polymorphism.

120. Improve MRO clarity in this multiple inheritance design.

121. Refactor method override that silently changes return type unexpectedly.

122. Introduce `Protocol` for structural typing in notifier module.

123. Refactor to eliminate fragile base class side effects.

124. Move parent helper utilities into composed helper/service object.

125. Rewrite this code to avoid hardcoded parent class name:
```python
Parent.__init__(self)
```

126. Refactor to preserve substitutability across all child classes.

127. Convert this inheritance design to composition because relationship is `has-a`.

128. Add proper guard clauses in child overrides to keep contract-safe behavior.

129. Create strategy classes for discount calculation.

130. Refactor large orchestration method into composition of small collaborators.

131. Replace direct field mutation with safe domain method calls.

132. Add integration test scenario for polymorphic service behavior.

133. Add unit tests for MRO-sensitive class behavior.

134. Refactor duplicate child methods by extracting reusable composed component.

135. Convert coupled service to use constructor-injected dependency.

136. Replace generic `manager`, `helper` naming with domain-specific class names.

137. Add explicit interface docs for preconditions and postconditions.

138. Refactor this LSP violation:
parent accepts positive amount, child accepts amount >= 1000.

139. Simplify this inheritance tree into one base + strategies.

140. Introduce `singledispatch` where overloaded behavior is function-based.

141. Refactor to avoid branching on format type for report generation.

142. Introduce clean polymorphic export pipeline for `csv/json/pdf`.

143. Move logging concern out of core business class using composition.

144. Refactor class with hidden side effects in overridden method.

145. Create minimal stable base class from overgrown parent class.

146. Redesign payment retries using composed `RetryPolicy`.

147. Refactor code to ensure all subclasses pass same contract tests.

148. Improve readability of multi-inheritance flow by clarifying MRO and method names.

149. Rewrite this to be open for extension, closed for modification.

150. Full rewrite prompt:
Take one inheritance-heavy module and redesign with:
- shallow hierarchy
- composition-first services
- contract-based polymorphism
- LSP-safe behavior
- testable dependency injection

---

## Section D: Interview-Style Questions (151-200)

151. Define inheritance in one line and give one good production example.

152. Define composition in one line and give one good production example.

153. Explain `is-a` vs `has-a` with two domain examples.

154. Why is "prefer composition over inheritance" a common guideline?

155. When is inheritance still the right choice?

156. Explain `super()` in Python with one multiple inheritance caveat.

157. What is MRO and why does it matter in real systems?

158. Explain the diamond problem with a class diagram.

159. How does C3 linearization prevent method ambiguity?

160. Why can calling overridable methods in parent `__init__` be risky?

161. Explain protected (`_x`) vs private (`__x`) in subclass design.

162. What makes a base class fragile?

163. How would you reduce fragility in a legacy inheritance hierarchy?

164. What is polymorphism and how is it different from inheritance?

165. Explain runtime polymorphism with one payment example.

166. Explain duck typing and when it is appropriate.

167. Explain `ABC` vs `Protocol` with trade-offs.

168. What is structural typing and why is it useful?

169. Define LSP in practical terms for code reviews.

170. Give one concrete LSP violation and how to fix it.

171. How do you design parent contracts to reduce LSP breaks?

172. What tests specifically validate LSP conformance?

173. How does polymorphism support Open/Closed Principle?

174. How does composition improve testability?

175. Explain dependency injection in one service example.

176. Why are `if/elif` type-switches a maintainability smell?

177. How do you refactor from type-switching to polymorphism safely?

178. How do you choose between inheritance and strategy pattern?

179. When can mixins be useful, and what are common mixin mistakes?

180. How do you keep class hierarchies shallow in growing projects?

181. What signals indicate an inheritance tree should be flattened?

182. How would you design a payment module supporting future channels?

183. How would you design logging so behavior can change at runtime?

184. How do abstractions reduce coupling in service layers?

185. How do you evaluate if an abstraction is too broad or too narrow?

186. What contract details should be documented for child implementers?

187. Why should method semantics stay consistent across polymorphic implementations?

188. How can operator overloading become harmful if misused?

189. When is `singledispatch` better than class hierarchies?

190. How do you create contract tests across multiple implementations?

191. What is the role of fake/mock dependencies in composition-based testing?

192. How do you migrate a tightly coupled module to composition-first architecture?

193. Compare runtime flexibility between inheritance and composition.

194. Explain one scenario where inheritance caused regressions in a team project.

195. Explain one scenario where composition reduced change risk significantly.

196. How would you explain MRO to a beginner in one minute?

197. What code review checklist would you use for LSP and substitution safety?

198. What metrics/signals show better design after refactor?

199. Final design prompt: build an extensible report generation engine (`pdf/csv/json`) using composition + polymorphism.

200. Final design prompt: redesign a legacy billing module to remove deep inheritance and enforce LSP-safe contracts.

---

## Capstone Project (Outside the 200 Questions)

### Project: Extensible Commerce Core (Inheritance + Polymorphism + Composition)

Build a mini system that applies all lecture concepts correctly.

### Modules
1. `payments.py`
2. `discounts.py`
3. `notifications.py`
4. `orders.py`
5. `tests/`

### Required Concepts
1. Inheritance with clear `is-a` hierarchy (where truly needed).
2. Polymorphism for interchangeable behavior.
3. Composition for service collaboration and runtime swapping.
4. LSP-safe contract behavior for all implementations.
5. Shallow hierarchy + clean naming + no giant type-switches.

### Functional Requirements
1. Payment contract with at least 3 implementations (`Card`, `UPI`, `Wallet`).
2. Discount strategy contract with at least 3 implementations.
3. Notification contract with at least 3 implementations (`Email`, `SMS`, `Push`).
4. `OrderService` composes payment + discount + notification dependencies.
5. Add one new provider in each module without changing core orchestration logic.

### Technical Constraints
1. No deep inheritance chains.
2. No hardcoded concrete classes inside service constructors.
3. Avoid `if/elif provider_type` in core business flow.
4. Include at least one `Protocol` or `ABC` per module contract.
5. Include tests for:
   - contract behavior
   - LSP-safe substitution
   - composition-based dependency injection
   - one MRO-related behavior if multiple inheritance is used

### Deliverables
1. source code files
2. test suite
3. short design note (1-2 pages) explaining:
   - where inheritance was used and why
   - where composition was preferred and why
   - how LSP was preserved
   - what was done to keep code maintainable

### Evaluation Rubric
- 25% contract clarity and API quality
- 25% LSP and substitution safety
- 25% composition-first architecture and low coupling
- 25% test quality and refactor-readiness

