# 🐍 PYTHON LEVEL 1 — VARIABLES MODEL ASSIGNMENT

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
* `b = a` copies the **reference** (not the object)
* Both `a` and `b` point to the **same object in memory**
* Printing both shows same content

👉 **Variables are references, not containers**

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
* `y = x` copies reference (same object)
* `y.append(3)` **mutates** the shared object
* Since both reference same object, both see the change

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

* `a = 10`, `b = a` → both reference int object 10
* `b = 20` **rebinds** `b` to new int object
* Rebinding creates new object, doesn't affect `a`
* `a` still points to original object (10)

👉 **Immutable objects: assignment creates new object**

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

* `x = 10`, `y = x` → both reference int 10
* `y += 5` is equivalent to `y = y + 5`
* For immutable objects, augmented assignment creates new object
* `y` now references new int object (15)
* `x` still references old object (10)

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
* `modify(a)` passes reference (call-by-sharing)
* Parameter `lst` references SAME object
* `lst.append(10)` mutates the object
* Original `a` sees the change

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
* `modify(a)` passes reference
* `lst = [999]` **rebinds** local parameter to new object
* Rebinding is local to function scope
* Original `a` unaffected

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
* `c = [1, 2]` → NEW object, same content

* `a is b` → same object? **True**
* `a == b` → same value? **True**
* `a is c` → same object? **False** (different memory locations)
* `a == c` → same value? **True** (content matches)

👉 **`is` checks identity | `==` checks value**

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
* `y = x[:]` creates **shallow copy** (new object, copied content)
* `x` and `y` now reference **different objects**
* `y.append(3)` mutates `y` object only
* `x` object is unaffected

👉 **Shallow copy creates new object**

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

* `a = [10]` creates list in heap
* `b = a` → references same object
* `c = b` → also references same object
* All three reference **one single object**
* `c[0] = 50` mutates the shared object
* All see the change

👉 **Multiple references to same object: all affected by mutation**

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
* `test(a)` passes reference
* `x.append(100)` **mutates** shared object → [1, 2, 100]
* `x = [999]` **rebinds** local parameter (local only)
* Original `a` reflects mutation but not rebinding

👉 **Mutation affects original: rebinding doesn't**

---

# 🧠 FINAL MENTAL MODEL (5 GOLDEN RULES)

After completing all 10 assignments, you should instantly know:

1. ✅ **Variable** = reference (label to object)
2. ✅ **Assignment** = copies reference, not object
3. ✅ **Mutable objects** → mutation changes shared object
4. ✅ **Immutable objects** → reassignment creates new object
5. ✅ **Function arguments** = call-by-sharing (reference passed)

---

# 🎯 ADDITIONAL RULES TO REMEMBER

6. ✅ **Mutation** = changes object itself
7. ✅ **Rebinding** = points to new object
8. ✅ **`is`** = identity (same object in memory)
9. ✅ **`==`** = value equality (same content)
10. ✅ **Shallow copy** = new top-level object

---

# 📋 SELF-CHECK

After solving all 10, can you:

- [ ] Explain that variables are references
- [ ] Predict output for mutable object sharing scenarios
- [ ] Predict output for immutable object reassignment
- [ ] Explain mutation vs rebinding difference
- [ ] Explain function argument behavior
- [ ] Predict if function mutation affects original
- [ ] Explain why function rebinding doesn't affect original
- [ ] Distinguish `is` from `==`
- [ ] Predict output for multiple references to same object
- [ ] Explain shallow copy behavior

---

**If you got 10/10 → Level 1 is MASTERED 🎉**

**Next: Level 2 = nested mutables, deep copy, default args, integer caching, string interning, circular references**
