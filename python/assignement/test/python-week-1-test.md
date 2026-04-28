# PYTHON WEEK 1 TEST

Instructions:
- Write answers only.
- Predict output only.
- Questions are Level 1 and Level 2 only.
- Topics: Variable Model, Function, Execution Model, Data Types and Memory Model, Control Flow.

Total Questions: 60

---

## Variable Model (10)

### Q1
```python
a = 10
b = a
a = a + 5
print(a, b)
```
Predict output.
Answer: ______________________________

### Q2
```python
x = [1, 2]
y = x
y.append(3)
print(x)
```
Predict output.
Answer: ______________________________

### Q3
```python
p = [4, 5]
q = p
q = [9, 9]
print(p)
print(q)
```
Predict output.
Answer: ______________________________

### Q4
```python
a = {'k': 1}
b = a
b['k'] = 7
print(a['k'])
```
Predict output.
Answer: ______________________________

### Q5
```python
a = [1, 2, 3]
b = a[:]
a[0] = 100
print(a)
print(b)
```
Predict output.
Answer: ______________________________

### Q6
```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a)
```
Predict output.
Answer: ______________________________

### Q7
```python
s1 = "dev"
s2 = s1
s1 = s1 + "ops"
print(s1, s2)
```
Predict output.
Answer: ______________________________

### Q8
```python
a = None
b = a
a = []
print(b)
```
Predict output.
Answer: ______________________________

### Q9
```python
m = [0, 1]
n = m
k = n
k[1] = 42
print(m)
```
Predict output.
Answer: ______________________________

### Q10
```python
a = [[1, 2], [3, 4]]
r = a[1]
r[0] = 30
print(a[1][0])
```
Predict output.
Answer: ______________________________

---

## Function (14)

### Q11
```python
def add_one(n):
    n = n + 1

a = 4
add_one(a)
print(a)
```
Predict output.
Answer: ______________________________

### Q12
```python
def scale(lst):
    lst[0] = lst[0] * 3

a = [2]
scale(a)
print(a)
```
Predict output.
Answer: ______________________________

### Q13
```python
def reset(lst):
    lst = [100]

a = [5]
reset(a)
print(a)
```
Predict output.
Answer: ______________________________

### Q14
```python
def square(x):
    return x * x

print(square(5))
```
Predict output.
Answer: ______________________________

### Q15
```python
def show(x, y=10):
    print(x + y)

show(3)
```
Predict output.
Answer: ______________________________

### Q16
```python
def show(x, y=10):
    print(x + y)

show(3, 5)
```
Predict output.
Answer: ______________________________

### Q17
```python
def show(a, b, c):
    print(a, b, c)

show(c=3, a=1, b=2)
```
Predict output.
Answer: ______________________________

### Q18
```python
def show(*args):
    print(len(args), args[1])

show(5, 6, 7)
```
Predict output.
Answer: ______________________________

### Q19
```python
def show(**kwargs):
    print(sorted(kwargs.keys()))

show(z=1, a=2)
```
Predict output.
Answer: ______________________________

### Q20
```python
def f(x=[]):
    x.append(1)
    print(x)

f()
f()
```
Predict output.
Answer: ______________________________

### Q21
```python
def f(x=[]):
    x.append(1)
    return x

print(f([]))
print(f([]))
```
Predict output.
Answer: ______________________________

### Q22
```python
def f():
    try:
        return 1
    finally:
        print('F')

print(f())
```
Predict output.
Answer: ______________________________

### Q23
```python
def f():
    try:
        return 2
    finally:
        return 9

print(f())
```
Predict output.
Answer: ______________________________

### Q24
```python
def outer():
    x = 10
    def inner():
        print(x)
    inner()

outer()
```
Predict output.
Answer: ______________________________

---

## Execution Model (8)

### Q25
```python
print('S1')
print('MAIN')
```
Predict output.
Answer: ______________________________

### Q26
```python
x = 5

def show():
    print(x)

show()
```
Predict output.
Answer: ______________________________

### Q27
```python
x = 5

def show():
    x = 9
    print(x)

show()
print(x)
```
Predict output.
Answer: ______________________________

### Q28
```python
x = 1

def show():
    global x
    x = x + 2

show()
print(x)
```
Predict output.
Answer: ______________________________

### Q29
```python
def f():
    print(y)
    y = 1

f()
```
Predict output.
Answer: ______________________________

### Q30
```python
def g():
    a = 2
    return a

print(g())
print('done')
```
Predict output.
Answer: ______________________________

### Q31
```python
def f():
    print(z)

z = 3
f()
```
Predict output.
Answer: ______________________________

### Q32
```python
print(type(lambda n: n + 1).__name__)
```
Predict output.
Answer: ______________________________

---

## Data Types and Memory Model (14)

### Q33
```python
print(type(10).__name__)
```
Predict output.
Answer: ______________________________

### Q34
```python
print(type(2.5).__name__)
```
Predict output.
Answer: ______________________________

### Q35
```python
print(type(True).__name__)
```
Predict output.
Answer: ______________________________

### Q36
```python
print(type('7').__name__)
```
Predict output.
Answer: ______________________________

### Q37
```python
a = int('12')
print(a + 8)
```
Predict output.
Answer: ______________________________

### Q38
```python
a = float('3.5')
print(a * 2)
```
Predict output.
Answer: ______________________________

### Q39
```python
print(bool([]), bool([0]))
```
Predict output.
Answer: ______________________________

### Q40
```python
a = [1, 2]
b = [1, 2]
print(a == b)
print(a is b)
```
Predict output.
Answer: ______________________________

### Q41
```python
a = None
print(a is None)
```
Predict output.
Answer: ______________________________

### Q42
```python
t = (1, 2, 3)
print(t[1])
```
Predict output.
Answer: ______________________________

### Q43
```python
s = {1, 2, 2, 3}
print(s)
```
Predict output.
Answer: ______________________________

### Q44
```python
d = {'a': 1, 'b': 2}
print(d.get('c', 0))
```
Predict output.
Answer: ______________________________

### Q45
```python
a = [[1], [2]]
b = a[:]
b[1] = ['x']
print(a)
print(b)
```
Predict output.
Answer: ______________________________

### Q46
```python
a = [[1], [2]]
b = a[:]
b[0].append(9)
print(a)
print(b)
```
Predict output.
Answer: ______________________________

---

## Control Flow (14)

### Q47
```python
n = -1
if n > 0:
    print('P')
else:
    print('N')
```
Predict output.
Answer: ______________________________

### Q48
```python
x = 7
if x > 10:
    print('A')
elif x > 5:
    print('B')
else:
    print('C')
```
Predict output.
Answer: ______________________________

### Q49
```python
for i in range(3):
    print(i, end=' ')
```
Predict output.
Answer: ______________________________

### Q50
```python
i = 1
while i <= 3:
    print(i, end=' ')
    i += 1
```
Predict output.
Answer: ______________________________

### Q51
```python
for i in range(1, 6):
    if i == 3:
        continue
    if i == 5:
        break
    print(i, end=' ')
```
Predict output.
Answer: ______________________________

### Q52
```python
for i in range(2):
    for j in range(2):
        print(i, j, end=' | ')
```
Predict output.
Answer: ______________________________

### Q53
```python
x = 0
if x != 0 and 10 / x > 1:
    print('T')
else:
    print('F')
```
Predict output.
Answer: ______________________________

### Q54
```python
x = 0
if x != 0 or 10 / x > 1:
    print('T')
else:
    print('F')
```
Predict output.
Answer: ______________________________

### Q55
```python
for i in range(3):
    if i == 5:
        break
else:
    print('done')
```
Predict output.
Answer: ______________________________

### Q56
```python
for i in range(3):
    if i == 1:
        break
else:
    print('done')
```
Predict output.
Answer: ______________________________

### Q57
```python
x = 5
y = 'big' if x > 3 else 'small'
print(y)
```
Predict output.
Answer: ______________________________

### Q58
```python
a = True
b = False
if a or b and False:
    print('YES')
else:
    print('NO')
```
Predict output.
Answer: ______________________________

### Q59
```python
i = 0
while True:
    i += 1
    if i == 2:
        continue
    print(i, end=' ')
    if i == 3:
        break
```
Predict output.
Answer: ______________________________

### Q60
```python
for i in range(1, 4):
    if i % 2 == 0:
        print('E', end=' ')
    else:
        print('O', end=' ')
```
Predict output.
Answer: ______________________________

---
End of Test
