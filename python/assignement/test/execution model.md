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
