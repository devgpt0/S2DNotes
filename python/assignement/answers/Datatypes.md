# 🐍 PYTHON ASSIGNMENT - DATATYPES

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

### ✅ Expected Output

~~~
[91, 92]
[91, 92]
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
x = [92, 93]
y = x
y.append(94)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[92, 93, 94]
[92, 93, 94]
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
a = 93
b = a
b = 96
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
93
96
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
    v.append(94)

l = [95]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[95, 94]
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
    v = [95, 96]

l = [97]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[97]
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
x = [97, 98]
y = x[:]
y.append(99)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[97, 98]
[97, 98, 99]
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
x = [[98], [99]]
y = x[:]
y[0].append(100)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[98, 100], [99]]
[[98, 100], [99]]
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
t = ([99], 'k')
t[0].append(100)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([99, 100], 'k')
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
a = [100]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[100]
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
a = [101, 102]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[101, 102]
[101, 102]
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
x = [102, 103]
y = x
y.append(104)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[102, 103, 104]
[102, 103, 104]
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
a = 103
b = a
b = 106
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
103
106
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
    v.append(104)

l = [105]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[105, 104]
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
    v = [105, 106]

l = [107]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[107]
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
a = [106]
b = a
c = [106]
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
x = [107, 108]
y = x[:]
y.append(109)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[107, 108]
[107, 108, 109]
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
x = [[108], [109]]
y = x[:]
y[0].append(110)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[108, 110], [109]]
[[108, 110], [109]]
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
t = ([109], 'k')
t[0].append(110)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([109, 110], 'k')
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
a = [110]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[110]
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
a = [111, 112]
b = a
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[111, 112]
[111, 112]
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
x = [112, 113]
y = x
y.append(114)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[112, 113, 114]
[112, 113, 114]
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
a = 113
b = a
b = 116
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
113
116
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
    v.append(114)

l = [115]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[115, 114]
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
    v = [115, 116]

l = [117]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[117]
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
a = [116]
b = a
c = [116]
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
x = [117, 118]
y = x[:]
y.append(119)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[117, 118]
[117, 118, 119]
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
x = [[118], [119]]
y = x[:]
y[0].append(120)
print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[118, 120], [119]]
[[118, 120], [119]]
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
t = ([119], 'k')
t[0].append(120)
print(t)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([119, 120], 'k')
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
a = [120]
b = a
del a
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[120]
~~~

### 🧠 Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

👉 **Lifetime depends on remaining references**

---