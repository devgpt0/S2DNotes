# 🔹  PYTHON ASSIGNMENT - DATATYPES PYTHON ASSIGNMENT - DATATYPES

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

### 🔹 Expected Output

~~~
[91, 92]
[91, 92]
~~~

### 🔹  Reasoning

* `a` creates one list object in heap
* `b = a` copies reference, not list object
* Both names point to same object

🔹 **Variables are references (labels), not containers**

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

### 🔹 Expected Output

~~~
[92, 93, 94]
[92, 93, 94]
~~~

### 🔹  Reasoning

* `x` and `y` alias same list
* append mutates shared object
* Both names see change

🔹 **Mutation affects all aliases**

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

### 🔹 Expected Output

~~~
93
96
~~~

### 🔹  Reasoning

* Integers are immutable
* Reassignment binds b to a new int object
* a remains unchanged

🔹 **Rebinding is not mutation**

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

### 🔹 Expected Output

~~~
[95, 94]
~~~

### 🔹  Reasoning

* Function gets reference to same list
* append mutates object in place
* caller sees mutation

🔹 **Call-by-sharing + mutation changes original object**

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

### 🔹 Expected Output

~~~
[97]
~~~

### 🔹  Reasoning

* Parameter name is local
* local rebinding does not touch caller binding
* original list remains

🔹 **Local rebinding has no external effect**

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

### 🔹 Expected Output

~~~
True
True
False
True
~~~

### 🔹  Reasoning

* `is` checks identity
* `==` checks value
* c is different object with same content

🔹 **Identity and value equality are different**

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

### 🔹 Expected Output

~~~
[97, 98]
[97, 98, 99]
~~~

### 🔹  Reasoning

* slice creates new outer list
* mutation on y does not touch x
* top-level independence achieved

🔹 **Shallow copy separates only outer container**

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

### 🔹 Expected Output

~~~
[[98, 100], [99]]
[[98, 100], [99]]
~~~

### 🔹  Reasoning

* outer list copied
* inner list shared
* nested mutation appears in both

🔹 **Shallow copy does not clone nested objects**

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

### 🔹 Expected Output

~~~
([99, 100], 'k')
~~~

### 🔹  Reasoning

* tuple is immutable container
* list element is mutable
* element mutation is allowed

🔹 **Container immutability is not deep immutability**

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

### 🔹 Expected Output

~~~
[100]
~~~

### 🔹  Reasoning

* del removes one binding
* object still referenced by b
* object remains alive

🔹 **Lifetime depends on remaining references**

---

## Level 2 (Assignments 11-20)

## 🔹 ASSIGNMENT 11: Shared Inner List Trap

### Question

~~~python
x = [[0]] * 3
x[0].append(1)
print(x)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[0, 1], [0, 1], [0, 1]]
~~~

### 🧠 Reasoning

* `[[0]] * 3` repeats references to the same inner list.

---
## 🔹 ASSIGNMENT 12: Assignment vs Shallow vs Deep Copy

### Question

~~~python
import copy

a = [[1, 2], [3, 4]]
b = a
c = a[:]
d = copy.deepcopy(a)

a[0].append(99)

print(b)
print(c)
print(d)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[1, 2, 99], [3, 4]]
[[1, 2, 99], [3, 4]]
[[1, 2], [3, 4]]
~~~

### 🧠 Reasoning

* `b` is same object as `a`; `c` is shallow copy (shares inner lists); `d` is deep copy.

---
## 🔹 ASSIGNMENT 13: In-Place Element Update

### Question

~~~python
def f(x):
    x[0] = x[0] + 10

l = [5]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[15]
~~~

### 🧠 Reasoning

* list is mutable; element at index `0` is updated in place.

---
## 🔹 ASSIGNMENT 14: Mutable Default Argument Trap

### Question

~~~python
def f(val, lst=[]):
    lst.append(val)
    return lst

print(f(1))
print(f(2))
print(f(3))
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1]
[1, 2]
[1, 2, 3]
~~~

### 🧠 Reasoning

* default list argument is created once and reused across calls.

---
## 🔹 ASSIGNMENT 15: Local Rebinding with `+`

### Question

~~~python
def f(x):
    x = x + [100]

l = [1, 2]
f(l)
print(l)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1, 2]
~~~

### 🧠 Reasoning

* `x = x + [100]` rebinds local `x` to a new list; original `l` unchanged.

---
## 🔹 ASSIGNMENT 16: Tuple with Shared Mutable Elements

### Question

~~~python
t1 = ([1, 2], [3, 4])
t2 = t1[:]

t2[0].append(99)

print(t1)
print(t2)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
([1, 2, 99], [3, 4])
([1, 2, 99], [3, 4])
~~~

### 🧠 Reasoning

* tuple slicing is shallow; both tuples reference same inner lists.

---
## 🔹 ASSIGNMENT 17: Shallow `dict.copy()` Trap

### Question

~~~python
d = {"a": [1]}
x = d
y = d.copy()

d["a"].append(2)

print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
{'a': [1, 2]}
{'a': [1, 2]}
~~~

### 🧠 Reasoning

* `dict.copy()` is shallow, so both dicts share the same list at key `"a"`.

---
## 🔹 ASSIGNMENT 18: Identity After Function Mutation

### Question

~~~python
def f(x):
    x.append(5)
    return x

a = [1]
b = f(a)

print(a is b)
print(a)
print(b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
[1, 5]
[1, 5]
~~~

### 🧠 Reasoning

* `f` mutates and returns the same list object.

---
## 🔹 ASSIGNMENT 19: Replacing a Nested Slot via Alias

### Question

~~~python
x = [[1], [2]]
y = x

y[0] = [99]

print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[[99], [2]]
[[99], [2]]
~~~

### 🧠 Reasoning

* `y` and `x` are same outer list; assignment `y[0] = [99]` changes shared outer list slot.

---
## 🔹 ASSIGNMENT 20: `id()` Before and After Rebinding

### Question

~~~python
x = [1, 2]
y = x

print(id(x), id(y))

y = y + [3]

print(id(x), id(y))
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
<same_id> <same_id>
<old_id> <new_id>
~~~

### 🧠 Reasoning

* initially `x` and `y` are same object. `y = y + [3]` creates a new list and rebinds `y`.

---

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21: Small Integer Identity

### Question

~~~python
a = 256
b = 256

print(a is b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
~~~

### 🧠 Reasoning

* in this runtime, both names point to same interned/cached integer object.

---
## 🔹 ASSIGNMENT 22: Large Integer Identity (Runtime Detail)

### Question

~~~python
a = 1000
b = 1000

print(a is b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
~~~

### 🧠 Reasoning

* in this runtime, compiler/runtime reused the same constant object for `1000` in this code block.

---
## 🔹 ASSIGNMENT 23: String Literal Interning

### Question

~~~python
a = "hello"
b = "hello"

print(a is b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
~~~

### 🧠 Reasoning

* identical string literals are interned/reused in this runtime.

---
## 🔹 ASSIGNMENT 24: Compile-Time Constant Folding

### Question

~~~python
a = "hello world"
b = "hello " + "world"

print(a is b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
~~~

### 🧠 Reasoning

* `"hello " + "world"` is constant-folded at compile time in this runtime.

---
## 🔹 ASSIGNMENT 25: In-Place List Update with `+=`

### Question

~~~python
x = [1, 2]
y = x

x += [3]

print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1, 2, 3]
[1, 2, 3]
~~~

### 🧠 Reasoning

* `+=` mutates list in place, so both names see change.

---
## 🔹 ASSIGNMENT 26: New List Creation with `+`

### Question

~~~python
x = [1, 2]
y = x

x = x + [3]

print(x)
print(y)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1, 2, 3]
[1, 2]
~~~

### 🧠 Reasoning

* `x = x + [3]` creates new list and rebinds only `x`.

---
## 🔹 ASSIGNMENT 27: Closure Capturing Mutable State

### Question

~~~python
def f():
    x = []
    def g():
        x.append(1)
        return x
    return g

a = f()
print(a())
print(a())
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1]
[1, 1]
~~~

### 🧠 Reasoning

* closure keeps same `x` list between calls.

---
## 🔹 ASSIGNMENT 28: Late Binding in Loop Lambdas

### Question

~~~python
funcs = []

for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[2, 2, 2]
~~~

### 🧠 Reasoning

* lambdas capture `i` by reference (late binding), final loop value is `2`.

---
## 🔹 ASSIGNMENT 29: Mutable Default Cache

### Question

~~~python
def f(x, cache={}):
    if x in cache:
        return cache[x]
    cache[x] = x * x
    return cache[x]

print(f(2))
print(f(2))
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
4
4
~~~

### 🧠 Reasoning

* default `cache` dict persists between calls.

---
## 🔹 ASSIGNMENT 30: Equality vs Identity

### Question

~~~python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)
print(a is b)
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
True
False
~~~

### 🧠 Reasoning

* `==` compares values; `is` compares object identity.

---
