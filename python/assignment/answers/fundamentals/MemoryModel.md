# 🐍 PYTHON ASSIGNMENT - MEMORY MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Variable as Reference

### Question

~~~python
a = [61, 62]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[61, 62]
[61, 62]
~~~

### 🧠 Reasoning

* `a` creates one list object in heap
* `b = a` copies reference, not list object
* Both names point to same object

👉 **Variables are references (labels), not containers**

---
## 🔹 ASSIGNMENT 2: Mutable Object Mutation

### Question

~~~python
x = [62, 63]
y = x
y.append(64)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[62, 63, 64]
[62, 63, 64]
~~~

### 🧠 Reasoning

* `x` and `y` alias same list
* append mutates shared object
* Both names see change

👉 **Mutation affects all aliases**

---
## 🔹 ASSIGNMENT 3: Immutable Rebinding

### Question

~~~python
a = 63
b = a
b = 66
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
63
66
~~~

### 🧠 Reasoning

* Integers are immutable
* Reassignment binds b to a new int object
* a remains unchanged

👉 **Rebinding is not mutation**

---
## 🔹 ASSIGNMENT 4: Function Mutation

### Question

~~~python
def f(v):
    v.append(64)

l = [65]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[65, 64]
~~~

### 🧠 Reasoning

* Function gets reference to same list
* append mutates object in place
* caller sees mutation

👉 **Call-by-sharing + mutation changes original object**

---
## 🔹 ASSIGNMENT 5: Function Rebinding

### Question

~~~python
def f(v):
    v = [65, 66]

l = [67]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[67]
~~~

### 🧠 Reasoning

* Parameter name is local
* local rebinding does not touch caller binding
* original list remains

👉 **Local rebinding has no external effect**

---
## 🔹 ASSIGNMENT 6: Identity vs Equality

### Question

~~~python
a = [66]
b = a
c = [66]
print(a is b)
print(a == b)
print(a is c)
print(a == c)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
True
False
True
~~~

### 🧠 Reasoning

* `is` checks identity
* `==` checks value
* c is different object with same content

👉 **Identity and value equality are different**

---
## 🔹 ASSIGNMENT 7: Shallow Copy Top Level

### Question

~~~python
x = [67, 68]
y = x[:]
y.append(69)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[67, 68]
[67, 68, 69]
~~~

### 🧠 Reasoning

* slice creates new outer list
* mutation on y does not touch x
* top-level independence achieved

👉 **Shallow copy separates only outer container**

---
## 🔹 ASSIGNMENT 8: Nested Shallow Copy Trap

### Question

~~~python
x = [[68], [69]]
y = x[:]
y[0].append(70)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[68, 70], [69]]
[[68, 70], [69]]
~~~

### 🧠 Reasoning

* outer list copied
* inner list shared
* nested mutation appears in both

👉 **Shallow copy does not clone nested objects**

---
## 🔹 ASSIGNMENT 9: Tuple with Mutable Item

### Question

~~~python
t = ([69], 'k')
t[0].append(70)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([69, 70], 'k')
~~~

### 🧠 Reasoning

* tuple is immutable container
* list element is mutable
* element mutation is allowed

👉 **Container immutability is not deep immutability**

---
## 🔹 ASSIGNMENT 10: del One Name

### Question

~~~python
a = [70]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[70]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---

## Level 2 (Assignments 11-20)

## 🔹 ASSIGNMENT 11: Variable as Reference

### Question

~~~python
a = [71, 72]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[71, 72]
[71, 72]
~~~

### 🧠 Reasoning

* `a` creates one list object in heap
* `b = a` copies reference, not list object
* Both names point to same object

👉 **Variables are references (labels), not containers**

---
## 🔹 ASSIGNMENT 12: Mutable Object Mutation

### Question

~~~python
x = [72, 73]
y = x
y.append(74)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[72, 73, 74]
[72, 73, 74]
~~~

### 🧠 Reasoning

* `x` and `y` alias same list
* append mutates shared object
* Both names see change

👉 **Mutation affects all aliases**

---
## 🔹 ASSIGNMENT 13: Immutable Rebinding

### Question

~~~python
a = 73
b = a
b = 76
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
73
76
~~~

### 🧠 Reasoning

* Integers are immutable
* Reassignment binds b to a new int object
* a remains unchanged

👉 **Rebinding is not mutation**

---
## 🔹 ASSIGNMENT 14: Function Mutation

### Question

~~~python
def f(v):
    v.append(74)

l = [75]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[75, 74]
~~~

### 🧠 Reasoning

* Function gets reference to same list
* append mutates object in place
* caller sees mutation

👉 **Call-by-sharing + mutation changes original object**

---
## 🔹 ASSIGNMENT 15: Function Rebinding

### Question

~~~python
def f(v):
    v = [75, 76]

l = [77]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[77]
~~~

### 🧠 Reasoning

* Parameter name is local
* local rebinding does not touch caller binding
* original list remains

👉 **Local rebinding has no external effect**

---
## 🔹 ASSIGNMENT 16: Identity vs Equality

### Question

~~~python
a = [76]
b = a
c = [76]
print(a is b)
print(a == b)
print(a is c)
print(a == c)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
True
False
True
~~~

### 🧠 Reasoning

* `is` checks identity
* `==` checks value
* c is different object with same content

👉 **Identity and value equality are different**

---
## 🔹 ASSIGNMENT 17: Shallow Copy Top Level

### Question

~~~python
x = [77, 78]
y = x[:]
y.append(79)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[77, 78]
[77, 78, 79]
~~~

### 🧠 Reasoning

* slice creates new outer list
* mutation on y does not touch x
* top-level independence achieved

👉 **Shallow copy separates only outer container**

---
## 🔹 ASSIGNMENT 18: Nested Shallow Copy Trap

### Question

~~~python
x = [[78], [79]]
y = x[:]
y[0].append(80)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[78, 80], [79]]
[[78, 80], [79]]
~~~

### 🧠 Reasoning

* outer list copied
* inner list shared
* nested mutation appears in both

👉 **Shallow copy does not clone nested objects**

---
## 🔹 ASSIGNMENT 19: Tuple with Mutable Item

### Question

~~~python
t = ([79], 'k')
t[0].append(80)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([79, 80], 'k')
~~~

### 🧠 Reasoning

* tuple is immutable container
* list element is mutable
* element mutation is allowed

👉 **Container immutability is not deep immutability**

---
## 🔹 ASSIGNMENT 20: del One Name

### Question

~~~python
a = [80]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[80]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21: Variable as Reference

### Question

~~~python
a = [81, 82]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[81, 82]
[81, 82]
~~~

### 🧠 Reasoning

* `a` creates one list object in heap
* `b = a` copies reference, not list object
* Both names point to same object

👉 **Variables are references (labels), not containers**

---
## 🔹 ASSIGNMENT 22: Mutable Object Mutation

### Question

~~~python
x = [82, 83]
y = x
y.append(84)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[82, 83, 84]
[82, 83, 84]
~~~

### 🧠 Reasoning

* `x` and `y` alias same list
* append mutates shared object
* Both names see change

👉 **Mutation affects all aliases**

---
## 🔹 ASSIGNMENT 23: Immutable Rebinding

### Question

~~~python
a = 83
b = a
b = 86
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
83
86
~~~

### 🧠 Reasoning

* Integers are immutable
* Reassignment binds b to a new int object
* a remains unchanged

👉 **Rebinding is not mutation**

---
## 🔹 ASSIGNMENT 24: Function Mutation

### Question

~~~python
def f(v):
    v.append(84)

l = [85]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[85, 84]
~~~

### 🧠 Reasoning

* Function gets reference to same list
* append mutates object in place
* caller sees mutation

👉 **Call-by-sharing + mutation changes original object**

---
## 🔹 ASSIGNMENT 25: Function Rebinding

### Question

~~~python
def f(v):
    v = [85, 86]

l = [87]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[87]
~~~

### 🧠 Reasoning

* Parameter name is local
* local rebinding does not touch caller binding
* original list remains

👉 **Local rebinding has no external effect**

---
## 🔹 ASSIGNMENT 26: Identity vs Equality

### Question

~~~python
a = [86]
b = a
c = [86]
print(a is b)
print(a == b)
print(a is c)
print(a == c)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
True
False
True
~~~

### 🧠 Reasoning

* `is` checks identity
* `==` checks value
* c is different object with same content

👉 **Identity and value equality are different**

---
## 🔹 ASSIGNMENT 27: Shallow Copy Top Level

### Question

~~~python
x = [87, 88]
y = x[:]
y.append(89)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[87, 88]
[87, 88, 89]
~~~

### 🧠 Reasoning

* slice creates new outer list
* mutation on y does not touch x
* top-level independence achieved

👉 **Shallow copy separates only outer container**

---
## 🔹 ASSIGNMENT 28: Nested Shallow Copy Trap

### Question

~~~python
x = [[88], [89]]
y = x[:]
y[0].append(90)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[88, 90], [89]]
[[88, 90], [89]]
~~~

### 🧠 Reasoning

* outer list copied
* inner list shared
* nested mutation appears in both

👉 **Shallow copy does not clone nested objects**

---
## 🔹 ASSIGNMENT 29: Tuple with Mutable Item

### Question

~~~python
t = ([89], 'k')
t[0].append(90)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([89, 90], 'k')
~~~

### 🧠 Reasoning

* tuple is immutable container
* list element is mutable
* element mutation is allowed

👉 **Container immutability is not deep immutability**

---
## 🔹 ASSIGNMENT 30: del One Name

### Question

~~~python
a = [90]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[90]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---