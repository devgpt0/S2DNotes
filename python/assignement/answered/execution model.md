# 🐍 PYTHON LEVEL 1 — EXECUTION MODEL ASSIGNMENT

**Predict the output and explain the reasoning for each question**

---

## 🔹 ASSIGNMENT 1: Variable as Reference

### Question

```python
a = [1, 2]
b = a
print(a)
print(b)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2]
[1, 2]
```

### 🧠 Reasoning

* `a = [1, 2]` creates a list object in heap
* `b = a` does NOT copy the object, it copies the **reference**
* Both `a` and `b` point to the **same object in memory**
* Printing both shows same content

👉 **Variables are references (labels), not containers**

---

## 🔹 ASSIGNMENT 2: Mutable Object Mutation

### Question

```python
x = [1, 2]
y = x
y.append(3)
print(x)
print(y)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2, 3]
[1, 2, 3]
```

### 🧠 Reasoning

* `x = [1, 2]` creates list object in heap
* `y = x` copies the reference (both point to same object)
* `y.append(3)` **mutates** the object itself
* Since they reference the same object, both see the change
* Mutation affects the shared object, not the reference

👉 **Mutable objects: mutation modifies shared object**

---

## 🔹 ASSIGNMENT 3: Immutable Object Assignment

### Question

```python
a = 10
b = a
b = 20
print(a)
print(b)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
10
20
```

### 🧠 Reasoning

* `a = 10` creates int object with value 10
* `b = a` copies reference, both point to same object (10)
* `b = 20` **rebinds** `b` to a new int object (20)
* Rebinding creates/points to new object, doesn't affect `a`
* `a` still points to old object (10)

👉 **Immutable objects: reassignment creates new object**

---

## 🔹 ASSIGNMENT 4: Immutable Object Augmented Assignment

### Question

```python
x = 10
y = x
y += 5
print(x)
print(y)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
10
15
```

### 🧠 Reasoning

* `x = 10`, `y = x` → both point to int object (10)
* `y += 5` is equivalent to `y = y + 5`
* For immutable objects, `+=` creates a new object
* `y` now points to new int object (15)
* `x` still points to old object (10)

👉 **For immutables: augmented assignment = rebinding**

---

## 🔹 ASSIGNMENT 5: Function Argument - Mutable Mutation

### Question

```python
def modify(lst):
    lst.append(10)

a = [1, 2]
modify(a)
print(a)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2, 10]
```

### 🧠 Reasoning

* `a = [1, 2]` creates list in heap
* `modify(a)` passes reference to function (call-by-sharing)
* Parameter `lst` receives reference to SAME object
* `lst.append(10)` mutates the object
* Original `a` still references same object, now modified

👉 **Function receives reference: mutation affects original**

---

## 🔹 ASSIGNMENT 6: Function Argument - Rebinding

### Question

```python
def modify(lst):
    lst = [999]

a = [1, 2]
modify(a)
print(a)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2]
```

### 🧠 Reasoning

* `a = [1, 2]` creates list in heap
* `modify(a)` passes reference to function
* `lst = [999]` **rebinds** local parameter to new object
* Rebinding is local to function scope
* Original `a` still points to original object
* Local reassignment does NOT affect caller's reference

👉 **Function rebinding ≠ affects original**

---

## 🔹 ASSIGNMENT 7: Identity vs Equality (Mutable)

### Question

```python
a = [1, 2]
b = a
c = [1, 2]

print(a is b)
print(a == b)
print(a is c)
print(a == c)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
True
True
False
True
```

### 🧠 Reasoning

* `a = [1, 2]`, `b = a` → same object
* `c = [1, 2]` → NEW object with same content

* `a is b` → same object? **True** (both point to same object)
* `a == b` → same value? **True** (content is same)
* `a is c` → same object? **False** (different objects, different memory)
* `a == c` → same value? **True** (content is same)

👉 **`is` = identity | `==` = value equality**

---

## 🔹 ASSIGNMENT 8: Shallow Copy

### Question

```python
x = [1, 2]
y = x[:]
y.append(3)
print(x)
print(y)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2]
[1, 2, 3]
```

### 🧠 Reasoning

* `x = [1, 2]` creates list in heap
* `y = x[:]` creates **shallow copy** (new object, same content)
* `x` and `y` point to **different objects**
* `y.append(3)` mutates `y` object only
* `x` object is unaffected

👉 **Shallow copy creates new object at top level**

---

## 🔹 ASSIGNMENT 9: Multiple References to Same Object

### Question

```python
a = [10]
b = a
c = b
c[0] = 50

print(a)
print(b)
print(c)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[50]
[50]
[50]
```

### 🧠 Reasoning

* `a = [10]` creates list object in heap
* `b = a` → `b` references same object
* `c = b` → `c` also references same object
* All three variables point to **one single object**
* `c[0] = 50` mutates the shared object
* All references see the change

👉 **Multiple references to same object: mutation affects all**

---

## 🔹 ASSIGNMENT 10: Mutation vs Rebinding in Function

### Question

```python
def test(x):
    x.append(100)
    x = [999]

a = [1, 2]
test(a)
print(a)
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
[1, 2, 100]
```

### 🧠 Reasoning

* `a = [1, 2]` creates list in heap
* `test(a)` passes reference to function
* `x.append(100)` **mutates** the shared object → now [1, 2, 100]
* `x = [999]` **rebinds** local parameter to new object (only affects parameter)
* Original `a` still references original object (now [1, 2, 100])
* Rebinding happens after mutation, too late to affect original

👉 **Mutation happens first (affects original), then rebinding (local only)**

---

# 🎯 YOUR LEARNING CHECKLIST

After solving all 10 assignments, verify you understand:

- [ ] Variables are references (labels), not containers
- [ ] Assignment copies references, not objects
- [ ] Mutable objects: mutation affects all references
- [ ] Immutable objects: reassignment creates new object
- [ ] Augmented assignment on immutables also creates new object
- [ ] Functions receive references (call-by-sharing)
- [ ] Function mutation affects original object
- [ ] Function reassignment is local only
- [ ] Identity (`is`) vs equality (`==`) difference
- [ ] Shallow copy creates new object but not nested copies

---

**If you solved all 10 → Level 1 is complete! 🎉**

**Next: Level 2 = nested mutable objects, deep copy, default arguments, integer caching, string interning**
