# 🔹  PYTHON ASSIGNMENT - DATATYPES

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Variable as Reference

### Question

~~~python
a = [91, 92]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 2: Mutable Object Mutation

### Question

~~~python
x = [92, 93]
y = x
y.append(94)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 3: Immutable Rebinding

### Question

~~~python
a = 93
b = a
b = 96
print(a)
print(b)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 4: Function Mutation

### Question

~~~python
def f(v):
    v.append(94)

l = [95]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 5: Function Rebinding

### Question

~~~python
def f(v):
    v = [95, 96]

l = [97]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 6: Identity vs Equality

### Question

~~~python
a = [96]
b = a
c = [96]
print(a is b)
print(a == b)
print(a is c)
print(a == c)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 7: Shallow Copy Top Level

### Question

~~~python
x = [97, 98]
y = x[:]
y.append(99)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 8: Nested Shallow Copy Trap

### Question

~~~python
x = [[98], [99]]
y = x[:]
y[0].append(100)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 9: Tuple with Mutable Item

### Question

~~~python
t = ([99], 'k')
t[0].append(100)
print(t)
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 10: del One Name

### Question

~~~python
a = [100]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

## LEVEL 2 - Intermediate

## ASSIGNMENT 11

```python
x = [[0]] * 3
x[0].append(1)
print(x)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 12

```python
import copy

a = [[1, 2], [3, 4]]
b = a
c = a[:]
d = copy.deepcopy(a)

a[0].append(99)

print(b)
print(c)
print(d)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 13

```python
def f(x):
    x[0] = x[0] + 10

l = [5]
f(l)
print(l)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 14

```python
def f(val, lst=[]):
    lst.append(val)
    return lst

print(f(1))
print(f(2))
print(f(3))
```

**Predict the output and explain why:**

---

## ASSIGNMENT 15

```python
def f(x):
    x = x + [100]

l = [1, 2]
f(l)
print(l)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 16

```python
t1 = ([1, 2], [3, 4])
t2 = t1[:]

t2[0].append(99)

print(t1)
print(t2)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 17

```python
d = {"a": [1]}
x = d
y = d.copy()

d["a"].append(2)

print(x)
print(y)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 18

```python
def f(x):
    x.append(5)
    return x

a = [1]
b = f(a)

print(a is b)
print(a)
print(b)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 19

```python
x = [[1], [2]]
y = x

y[0] = [99]

print(x)
print(y)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 20

```python
x = [1, 2]
y = x

print(id(x), id(y))

y = y + [3]

print(id(x), id(y))
```

**Predict the output and explain why:**

---

## LEVEL 3 - Advanced

## ASSIGNMENT 21

```python
a = 256
b = 256

print(a is b)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 22

```python
a = 1000
b = 1000

print(a is b)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 23

```python
a = "hello"
b = "hello"

print(a is b)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 24

```python
a = "hello world"
b = "hello " + "world"

print(a is b)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 25

```python
x = [1, 2]
y = x

x += [3]

print(x)
print(y)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 26

```python
x = [1, 2]
y = x

x = x + [3]

print(x)
print(y)
```

**Predict the output and explain why:**

---

## ASSIGNMENT 27

```python
def f():
    x = []
    def g():
        x.append(1)
        return x
    return g

a = f()
print(a())
print(a())
```

**Predict the output and explain why:**

---

## ASSIGNMENT 28

```python
funcs = []

for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
```

**Predict the output and explain why:**

---

## ASSIGNMENT 29

```python
def f(x, cache={}):
    if x in cache:
        return cache[x]
    cache[x] = x * x
    return cache[x]

print(f(2))
print(f(2))
```

**Predict the output and explain why:**

---

## ASSIGNMENT 30

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)
print(a is b)
```

**Predict the output and explain why:**
