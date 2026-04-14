# 🐍 PYTHON DATA TYPES ASSIGNMENT

**Identify types and predict behavior**

---

## 🔹 ASSIGNMENT 1: Type Identification

### Question

```python
x = [1, 2, 3]
y = (1, 2, 3)
z = {1, 2, 3}
d = {"a": 1}
s = "hello"
n = 42
b = True

print(type(x).__name__)
print(type(y).__name__)
print(type(z).__name__)
print(type(d).__name__)
print(type(s).__name__)
print(type(n).__name__)
print(type(b).__name__)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 2: Mutability Behavior

### Question

```python
# Mutable
lst = [1, 2]
lst.append(3)
print(lst)

# Immutable
s = "hello"
s = s + " world"
print(s)

# Immutable
t = (1, 2)
t = t + (3,)
print(t)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 3: Type Modification

### Question

```python
lst = [1, 2]
lst[0] = 99
print(lst)

# Try this with immutable
s = "hello"
# s[0] = "H"  # Would error

d = {"a": 1}
d["b"] = 2
print(d)

s = {"a", "b"}
s.add("c")
print(s)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 4: Type Conversion

### Question

```python
print(str(42))
print(int("99"))
print(float("3.5"))
print(list("abc"))
print(tuple([1, 2, 3]))
print(set([1, 2, 2, 3]))
print(dict([("a", 1), ("b", 2)]))
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 5: Isinstance Checks

### Question

```python
print(isinstance([1, 2], list))
print(isinstance((1, 2), tuple))
print(isinstance({1, 2}, set))
print(isinstance("hello", str))
print(isinstance(42, int))
print(isinstance(True, bool))
print(isinstance({}, dict))
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 6: Mutable Collections

### Question

```python
# List operations
lst = [1, 2]
lst.append(3)
lst.remove(2)
print(lst)

# Dict operations
d = {"x": 10}
d["y"] = 20
print(d)

# Set operations
s = {1, 2}
s.add(3)
s.remove(1)
print(s)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 7: Tuple vs List

### Question

```python
lst = [1, 2, 3]
tpl = (1, 2, 3)

lst[0] = 99
print(lst)

# tpl[0] = 99  # Would error

tpl_new = tpl + (4,)
print(tpl_new)

lst_new = lst + [4]
print(lst_new)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 8: Container in Container

### Question

```python
# Dict with list
d = {"items": [1, 2]}
d["items"].append(3)
print(d)

# Tuple with list
t = ([1, 2], "text")
t[0].append(3)
print(t)

# List with dict
lst = [{"a": 1}]
lst[0]["b"] = 2
print(lst)
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 9: Comparison Operations

### Question

```python
print([1, 2] == [1, 2])
print((1, 2) == (1, 2))
print({1, 2} == {2, 1})
print({"a": 1} == {"a": 1})
print("hello" == "hello")
print([1, 2] == (1, 2))
print({1, 2} == [1, 2])
```

**Predict the output and explain why:**

---

## 🔹 ASSIGNMENT 10: Empty Collections

### Question

```python
print(len([]))
print(len(()))
print(len({}))
print(len(set()))
print(len(""))

print(bool([]))
print(bool(()))
print(bool({}))
print(bool(set()))
print(bool(""))
print(bool(0))
print(bool(None))
```

**Predict the output and explain why:**

---
