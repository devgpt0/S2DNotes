# Worksheet: Clean Code Foundations + Why OOP Exists - Classes and Objects


## Section A: MCQ (1-50)

1. What is the primary goal of clean code?
A. Reduce file size
B. Make code run only faster
C. Improve readability and maintainability
D. Use advanced syntax

2. Which variable name is best?
A. x
B. n1
C. student_total_marks
D. data

3. Which function name communicates intent best?
A. process
B. calc
C. do_task
D. calculate_average_score

4. Which is a magic number example?
A. TAX_RATE = 0.18
B. if marks >= 75
C. MIN_ATTENDANCE = 75
D. MAX_USERS = 100

5. DRY stands for:
A. Do Review Yourself
B. Do Repeat Yourself
C. Do not Repeat Yourself
D. Data Reuse Yield

6. A function that validates, saves, and emails in one place violates:
A. DRY
B. Single Responsibility
C. Encapsulation
D. Inheritance

7. Best use of comments in clean code is to explain:
A. obvious syntax
B. every line
C. why a non-obvious decision is made
D. variable declarations only

8. Which is best for boolean naming?
A. flag
B. status
C. is_active
D. value

9. Which is true about readable code?
A. Must be shortest possible
B. Must use one-liners
C. Should communicate intent clearly
D. Should avoid function extraction

10. Which function is easier to test?
A. Long function with many side effects
B. Small pure function with clear input-output
C. Function with global variables
D. Function with random print statements

11. A class is:
A. a single function
B. a blueprint for objects
C. always required in Python
D. same as a module

12. An object is:
A. a loop
B. an instance of class
C. a package
D. a comment

13. `self` refers to:
A. class itself always
B. current instance object
C. global namespace
D. file scope

14. `__init__` in Python is mainly used to:
A. delete object
B. initialize instance data
C. compile class
D. print class name

15. Which is a good class name?
A. DataHandler
B. Manager
C. Student
D. Utility

16. Which is better for adding two numbers?
A. class AddNumbers
B. def add_numbers(a, b)
C. class SumHelper
D. class MathManager

17. Which is state in OOP?
A. method body
B. object attributes
C. for loop
D. import statement

18. Which is behavior in OOP?
A. instance variables
B. constants
C. methods
D. comments

19. Why does procedural code often fail at scale?
A. Python cannot run it
B. duplication and scattered logic
C. classes are mandatory
D. syntax errors only

20. Best constructor practice:
A. no validation ever
B. include basic validity checks
C. make network calls every time
D. print debug by default

21. Which naming pair is best?
A. n, m
B. student_name, marks
C. a1, b1
D. temp, data

22. Which indicates hidden side effect?
A. returns computed value
B. modifies global variable silently
C. uses local variable
D. has type hint

23. Guard clauses help by:
A. increasing nesting
B. reducing readability
C. handling invalid cases early
D. replacing constructors

24. Which code is cleaner?
A. if x > 90: return "A"
B. if average_score > GRADE_A_THRESHOLD: return "A"
C. if m > 90: return "A"
D. if n > 90: return "A"

25. A class attribute is:
A. unique for each object
B. shared across all instances
C. local to function
D. same as parameter

26. An instance attribute is:
A. shared by all objects
B. attached to each object separately
C. always constant
D. only for static methods

27. Risk with `items=[]` in constructor default is:
A. syntax error
B. shared mutable state across instances
C. cannot append values
D. slower runtime only

28. Better constructor default pattern for list is:
A. items=[]
B. items={}
C. items=None then create new list
D. items=0

29. Which statement is true?
A. All code must be OOP
B. Everything should be a class
C. Use class when domain concept + state + behavior exist
D. Functions should be avoided

30. Which is not a clean code smell?
A. meaningful names
B. duplicated logic
C. long god function
D. magic numbers

31. Which is best method name?
A. do_it
B. handle
C. calculate_annual_tax
D. run

32. What makes refactoring safe?
A. big-bang rewrite
B. tiny changes + tests
C. changing behavior and style together blindly
D. skipping validation

33. Which is better comment strategy?
A. comment each assignment
B. remove all comments always
C. keep comments for business rules and trade-offs
D. write comments instead of clear code

34. Which class design is better?
A. Student with calculate_average()
B. Student data + global utility methods only
C. Student with unrelated 20 methods
D. StudentManagerProcessorHelper

35. `student.calculate_average()` internally maps to:
A. Student.calculate_average()
B. calculate_average(student)
C. Student.calculate_average(student)
D. student.self.calculate_average()

36. Which is true about clean code and interviews?
A. only syntax is tested
B. design reasoning is often tested
C. naming is never asked
D. refactoring is out of scope

37. Which violates one responsibility most?
A. determine_grade()
B. save_student()
C. send_grade_email()
D. process_everything_and_notify_and_store()

38. Better constant naming style:
A. taxrate
B. TaxRate
C. TAX_RATE
D. tax-Rate

39. Best choice for class modeling library system:
A. AddBookData
B. Book, Member, Library
C. GenericHandler
D. DataClassOnly

40. Which is better for output clarity?
A. print("x", a)
B. print(f"Average score: {average_score:.2f}")
C. print(avg)
D. print(data)

41. What does maintainability mean?
A. code never changes
B. easy to understand and modify safely
C. only fast runtime
D. fewer files

42. Which is a good clean code improvement?
A. rename `x` to `student_name`
B. add nested ifs
C. remove function boundaries
D. increase hidden globals

43. Which is true about abstraction level in a function?
A. mix UI + DB + business logic always
B. keep statements at similar abstraction level
C. always use one line
D. avoid helper methods

44. Which is an OOP-friendly definition?
A. objects group data + behavior
B. objects are only dictionaries
C. classes are optional syntax sugar without design value
D. OOP means inheritance only

45. Which is cleaner API?
A. car.inject_fuel(); car.fire_spark(); car.start_piston()
B. car.start()
C. car.do_everything_manually()
D. car.helper()

46. Good interview explanation for DRY includes:
A. remove all repeated words
B. remove repeated business logic
C. avoid loops
D. avoid functions

47. Which method should likely be in `Student` class?
A. deploy_server()
B. calculate_average()
C. parse_json_logs()
D. send_global_alert()

48. Which is better error handling?
A. except Exception: pass
B. catch specific exception and re-raise with context
C. always ignore errors
D. print only

49. Which concept best prevents confusion in teams?
A. clever code golf
B. consistent naming conventions
C. random style per file
D. heavy abbreviation

50. Why is this lecture before advanced OOP?
A. clean code reduces future OOP misuse
B. because Python requires it
C. because classes cannot be taught first
D. no reason

---

## Section B: Predict the Output (51-80)

51.
```python
TAX_RATE = 0.18
price = 100
print(price * TAX_RATE)
```

52.
```python
def add(a, b):
    return a + b

print(add(2, 3))
```

53.
```python
class Student:
    def __init__(self, name):
        self.name = name

s = Student("Asha")
print(s.name)
```

54.
```python
class Student:
    school = "ABC"

s1 = Student()
s2 = Student()
print(s1.school, s2.school)
```

55.
```python
class Student:
    def __init__(self, marks):
        self.marks = marks

    def avg(self):
        return sum(self.marks) / len(self.marks)

print(Student([80, 90]).avg())
```

56.
```python
def grade(avg):
    if avg > 90:
        return "A"
    if avg > 80:
        return "B"
    return "C"

print(grade(90))
```

57.
```python
def f(items=[]):
    items.append(1)
    print(items)

f()
f()
```

58.
```python
class Cart:
    def __init__(self, items=None):
        self.items = [] if items is None else items

c1 = Cart()
c2 = Cart()
c1.items.append("pen")
print(c1.items, c2.items)
```

59.
```python
class A:
    value = 10

a = A()
a.value = 99
print(a.value, A.value)
```

60.
```python
class A:
    value = []

a1 = A()
a2 = A()
a1.value.append(5)
print(a2.value)
```

61.
```python
def calculate_total(price, quantity):
    subtotal = price * quantity
    return subtotal

print(calculate_total(50, 3))
```

62.
```python
def check(attendance):
    MIN_ATTENDANCE = 75
    return attendance >= MIN_ATTENDANCE

print(check(74), check(75))
```

63.
```python
class Student:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

Student("Ravi").show()
```

64.
```python
class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

Counter()
Counter()
print(Counter.count)
```

65.
```python
x = 10

def update():
    x = 20
    print(x)

update()
print(x)
```

66.
```python
total = 0

def add(value):
    global total
    total += value

add(10)
add(5)
print(total)
```

67.
```python
def label(name, is_active):
    if is_active:
        return f"{name}-ACTIVE"
    return f"{name}-INACTIVE"

print(label("A", False))
```

68.
```python
class Student:
    def __init__(self, marks):
        self.marks = marks

    def add_mark(self, mark):
        self.marks.append(mark)

s = Student([80])
s.add_mark(90)
print(s.marks)
```

69.
```python
class Demo:
    def show(self):
        return "ok"

obj = Demo()
print(Demo.show(obj))
```

70.
```python
class Demo:
    def __init__(self, name):
        self.name = name

obj = Demo("Nina")
print(type(obj).__name__)
```

71.
```python
def get_discount(price):
    DISCOUNT_THRESHOLD = 1000
    if price > DISCOUNT_THRESHOLD:
        return 100
    return 0

print(get_discount(1000))
```

72.
```python
class Book:
    def __init__(self, title):
        self.title = title

b = Book("Clean Code")
print(hasattr(b, "title"), hasattr(b, "author"))
```

73.
```python
class User:
    role = "student"

u1 = User()
u2 = User()
u2.role = "admin"
print(u1.role, u2.role, User.role)
```

74.
```python
def compute(values):
    return sum(values) / len(values)

print(round(compute([1, 2, 3, 4]), 2))
```

75.
```python
class S:
    def __init__(self, n):
        self.n = n

    def set_n(self, n):
        self.n = n

s = S(5)
s.set_n(8)
print(s.n)
```

76.
```python
class A:
    def __init__(self):
        self.values = []

a = A()
b = A()
a.values.append(1)
print(a.values, b.values)
```

77.
```python
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b

print(safe_divide(10, 2), safe_divide(10, 0))
```

78.
```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

s = Student("Ana", [70, 80])
print(len(s.marks))
```

79.
```python
class Student:
    def __init__(self, marks):
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

s1 = Student([100, 90])
s2 = Student([50, 70])
print(s1.average() > s2.average())
```

80.
```python
class Profile:
    def __init__(self, name):
        self.name = name

p = Profile("Jay")
print(p.__dict__)
```

---

## Section C: Refactor the Code (81-100)

81. Refactor for meaningful naming and constants:
```python
def p(a, b):
    return a * b * 0.18
```

82. Refactor into single-responsibility functions:
```python
def process_student(student):
    validate(student)
    grade = calc(student["marks"])
    save(student)
    send_email(student["email"], grade)
    print("done")
```

83. Refactor to remove duplication:
```python
john_avg = sum(john_marks) / len(john_marks)
ravi_avg = sum(ravi_marks) / len(ravi_marks)
```

84. Refactor this vague class design:
```python
class S:
    def __init__(self, n, m):
        self.n = n
        self.m = m
```

85. Refactor this magic-number-heavy code:
```python
if score > 90:
    grade = "A"
elif score > 80:
    grade = "B"
else:
    grade = "C"
```

86. Refactor to avoid deep nesting (use guard clauses):
```python
def withdraw(account, amount):
    if account is not None:
        if amount > 0:
            if account.balance >= amount:
                account.balance -= amount
```

87. Refactor to avoid hidden side effects:
```python
total = 0

def add_price(price):
    global total
    total += price
```

88. Refactor this constructor default bug:
```python
class Cart:
    def __init__(self, items=[]):
        self.items = items
```

89. Refactor into better class/function choice:
```python
class AddNumbers:
    def add(self, a, b):
        return a + b
```

90. Refactor to improve method naming:
```python
class Employee:
    def f1(self):
        return self.salary * 12
```

91. Refactor this god function into cohesive methods:
```python
def run_order(order):
    validate(order)
    reserve_inventory(order)
    create_invoice(order)
    charge_payment(order)
    send_confirmation(order)
```

92. Refactor comments into self-documenting code where possible:
```python
# calculate average marks
avg = sum(marks) / len(marks)
```

93. Refactor for clearer domain modeling:
```python
student = {"n": "Ria", "m": [88, 92]}

def avg(s):
    return sum(s["m"]) / len(s["m"])
```

94. Refactor with constructor validation:
```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
```

95. Refactor this mixed abstraction method:
```python
def register(user):
    if "@" in user.email:
        db.save(user)
        print("saved")
        send_email(user.email)
```

96. Refactor to improve constant placement and naming:
```python
def allowed(att):
    return att >= 75
```

97. Refactor for better separation of concerns:
```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def process(self):
        avg = sum(self.marks)/len(self.marks)
        if avg > 90:
            g = "A"
        else:
            g = "B"
        with open("x.txt", "a") as f:
            f.write(self.name + g)
        print(g)
```

98. Refactor for cleaner API design:
```python
class Car:
    def inject_fuel(self): ...
    def start_piston(self): ...
    def fire_spark(self): ...
```

99. Refactor to remove broad exception handling:
```python
try:
    save_user(user)
except Exception:
    pass
```

100. Refactor this class with shared mutable attribute:
```python
class Student:
    marks = []

    def add_mark(self, mark):
        self.marks.append(mark)
```

---

## Project Exercises 

### Project 1: Clean Code Refactor Pack
Take a 150-200 line procedural script and refactor it using:
- meaningful names
- constants for magic values
- single-responsibility functions
- guard clauses
- zero duplicated business logic

Deliverables:
- before/after code
- short write-up of top 10 improvements

### Project 2: Student Management OOP Mini System
Build classes:
- `Student`
- `Course`
- `EnrollmentService`

Features:
- enroll student
- calculate course-wise average
- generate grade report

Constraints:
- constructor validation
- no shared mutable class lists
- methods should stay focused

### Project 3: Library Management (Interview Style)
Build classes:
- `Book`
- `Member`
- `Library`

Features:
- add/remove book
- register member
- borrow/return book
- print inventory summary

Interview focus:
- clean naming
- good class boundaries
- readable, testable methods

### Project 4: Employee Payroll Core
Build classes:
- `Employee`
- `PayrollCalculator`
- `TaxPolicy`

Features:
- monthly to annual salary conversion
- tax calculation via constants/policy
- salary slip text output

### Project 5: Interview Refactor Challenge
Given an intentionally messy script, perform 3 rounds of refactor:
- Round A: naming cleanup
- Round B: function extraction
- Round C: class modeling

Write a short "refactor log" for each round.

---

## Submission Recommendation
- Attempt MCQ first, then output prediction, then refactor.
- Time split: 40 min (MCQ) + 35 min (output) + 45 min (refactor) + project at home.
