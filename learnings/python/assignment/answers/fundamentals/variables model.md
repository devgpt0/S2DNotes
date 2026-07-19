# 🐍 PYTHON ASSIGNMENT - VARIABLES MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Variable as Reference

### Question

~~~python
a = [1, 2]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1, 2]
[1, 2]
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
x = [2, 3]
y = x
y.append(4)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[2, 3, 4]
[2, 3, 4]
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
a = 3
b = a
b = 6
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
3
6
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
    v.append(4)

l = [5]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[5, 4]
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
    v = [5, 6]

l = [7]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[7]
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
a = [6]
b = a
c = [6]
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
x = [7, 8]
y = x[:]
y.append(9)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[7, 8]
[7, 8, 9]
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
x = [[8], [9]]
y = x[:]
y[0].append(10)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[8, 10], [9]]
[[8, 10], [9]]
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
t = ([9], 'k')
t[0].append(10)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([9, 10], 'k')
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
a = [10]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[10]
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
a = [11, 12]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[11, 12]
[11, 12]
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
x = [12, 13]
y = x
y.append(14)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[12, 13, 14]
[12, 13, 14]
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
a = 13
b = a
b = 16
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
13
16
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
    v.append(14)

l = [15]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[15, 14]
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
    v = [15, 16]

l = [17]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[17]
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
a = [16]
b = a
c = [16]
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
x = [17, 18]
y = x[:]
y.append(19)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[17, 18]
[17, 18, 19]
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
x = [[18], [19]]
y = x[:]
y[0].append(20)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[18, 20], [19]]
[[18, 20], [19]]
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
t = ([19], 'k')
t[0].append(20)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([19, 20], 'k')
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
a = [20]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[20]
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
a = [21, 22]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[21, 22]
[21, 22]
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
x = [22, 23]
y = x
y.append(24)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[22, 23, 24]
[22, 23, 24]
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
a = 23
b = a
b = 26
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
23
26
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
    v.append(24)

l = [25]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[25, 24]
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
    v = [25, 26]

l = [27]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[27]
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
a = [26]
b = a
c = [26]
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
x = [27, 28]
y = x[:]
y.append(29)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[27, 28]
[27, 28, 29]
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
x = [[28], [29]]
y = x[:]
y[0].append(30)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[28, 30], [29]]
[[28, 30], [29]]
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
t = ([29], 'k')
t[0].append(30)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([29, 30], 'k')
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
a = [30]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[30]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---