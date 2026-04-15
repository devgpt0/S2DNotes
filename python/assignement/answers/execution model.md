# 🐍 PYTHON ASSIGNMENT - EXECUTION MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Variable as Reference

### Question

~~~python
a = [31, 32]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[31, 32]
[31, 32]
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
x = [32, 33]
y = x
y.append(34)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[32, 33, 34]
[32, 33, 34]
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
a = 33
b = a
b = 36
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
33
36
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
    v.append(34)

l = [35]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[35, 34]
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
    v = [35, 36]

l = [37]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[37]
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
a = [36]
b = a
c = [36]
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
x = [37, 38]
y = x[:]
y.append(39)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[37, 38]
[37, 38, 39]
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
x = [[38], [39]]
y = x[:]
y[0].append(40)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[38, 40], [39]]
[[38, 40], [39]]
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
t = ([39], 'k')
t[0].append(40)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([39, 40], 'k')
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
a = [40]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[40]
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
a = [41, 42]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[41, 42]
[41, 42]
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
x = [42, 43]
y = x
y.append(44)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[42, 43, 44]
[42, 43, 44]
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
a = 43
b = a
b = 46
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
43
46
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
    v.append(44)

l = [45]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[45, 44]
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
    v = [45, 46]

l = [47]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[47]
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
a = [46]
b = a
c = [46]
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
x = [47, 48]
y = x[:]
y.append(49)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[47, 48]
[47, 48, 49]
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
x = [[48], [49]]
y = x[:]
y[0].append(50)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[48, 50], [49]]
[[48, 50], [49]]
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
t = ([49], 'k')
t[0].append(50)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([49, 50], 'k')
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
a = [50]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[50]
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
a = [51, 52]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[51, 52]
[51, 52]
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
x = [52, 53]
y = x
y.append(54)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[52, 53, 54]
[52, 53, 54]
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
a = 53
b = a
b = 56
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
53
56
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
    v.append(54)

l = [55]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[55, 54]
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
    v = [55, 56]

l = [57]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[57]
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
a = [56]
b = a
c = [56]
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
x = [57, 58]
y = x[:]
y.append(59)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[57, 58]
[57, 58, 59]
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
x = [[58], [59]]
y = x[:]
y[0].append(60)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[58, 60], [59]]
[[58, 60], [59]]
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
t = ([59], 'k')
t[0].append(60)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([59, 60], 'k')
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
a = [60]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[60]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---