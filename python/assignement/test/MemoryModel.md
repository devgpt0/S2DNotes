# 🐍 PYTHON MEMORY MODEL ASSIGNMENT

**Predict output and explain memory behavior**

---

## 🔹 ASSIGNMENT 1: Reference vs Value

### Question

```python
# Mutable reference
a = [1, 2]
b = a
b.append(3)
print(a)

# Immutable independent
x = 10
y = x
y = 20
print(x)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 2: Identity Check

### Question

```python
a = [1, 2]
b = a
c = [1, 2]

print(a is b)
print(a is c)
print(a == b)
print(a == c)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 3: Shallow Copy Issue

### Question

```python
x = [[1, 2], [3, 4]]
y = x[:]
y[0][0] = 99

print(x)
print(y)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 4: Dict Reference Sharing

### Question

```python
d1 = {"a": [1, 2]}
d2 = d1.copy()

d2["a"].append(3)

print(d1)
print(d2)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 5: Function Mutation

### Question

```python
def modify(lst):
    lst.append(100)

x = [1, 2]
modify(x)
print(x)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 6: Function Rebinding

### Question

```python
def modify(lst):
    lst = [999]
    lst.append(200)

x = [1, 2]
modify(x)
print(x)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 7: Tuple Mutability

### Question

```python
t = ([1, 2], "text")

t[0].append(3)
print(t)

# t[0] = [99]  # Would error
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 8: Multiple References

### Question

```python
a = [1, 2]
b = a
c = [a, a]

a.append(3)

print(a)
print(b)
print(c)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 9: Default Mutable Argument

### Question

```python
def append_item(lst=[]):
    lst.append(1)
    return lst

print(append_item())
print(append_item())
print(append_item())
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 10: Integer Caching

### Question

```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)

x = 256 + 0
y = 256
print(x is y)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 11: String Interning

### Question

```python
s1 = "hello"
s2 = "hello"
s3 = "hel" + "lo"
s4 = "".join(["h", "e", "l", "l", "o"])

print(s1 is s2)
print(s1 is s3)
print(s1 is s4)
print(s1 == s4)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 12: Unpacking

### Question

```python
lst = [[1, 2], [3, 4]]
a, b = lst

a[0] = 99
b = [99, 99]

print(lst)
print(a)
print(b)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 13: Set/Dict Copy

### Question

```python
s1 = {1, 2}
s2 = s1.copy()
s2.add(3)

d1 = {"a": {1, 2}}
d2 = d1.copy()
d2["a"].add(3)

print(s1)
print(d1)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 14: Complex Nesting

### Question

```python
data = [{"a": [1, 2]}]
copy = data[:]

copy[0]["a"].append(99)

print(data)
print(copy)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 15: Garbage Collection

### Question

```python
x = [1, 2]
y = x
del x

print(y)  # Will this work?
```

**Predict the output and explain why:**

---
