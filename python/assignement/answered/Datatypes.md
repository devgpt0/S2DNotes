# 🐍 PYTHON DATA TYPES ASSIGNMENT (ANSWERED)

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

### ✅ Expected Output

```
list
tuple
set
dict
str
int
bool
```

### 🧠 Reasoning

* Each value has a specific type
* `type()` returns the type object
* `.__name__` gets the string name of type
* Lists use `[]`, tuples use `()`, sets use `{}` with values, dicts use `{}` with key-value pairs

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

### ✅ Expected Output

```
[1, 2, 3]
hello world
(1, 2, 3)
```

### 🧠 Reasoning

* `lst.append(3)` modifies the list itself → `[1, 2, 3]`
* `s = s + " world"` creates new string (immutable) → `"hello world"`
* `t = t + (3,)` creates new tuple (immutable) → `(1, 2, 3)`
* For immutables, reassignment is needed to see new value

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

### ✅ Expected Output

```
[99, 2]
{'a': 1, 'b': 2}
{'a', 'b', 'c'}
```

### 🧠 Reasoning

* `lst[0] = 99` modifies list element → `[99, 2]`
* String cannot be modified (immutable) → `s[0] = "H"` would error
* `d["b"] = 2` adds new key-value to dict → `{'a': 1, 'b': 2}`
* `s.add("c")` adds element to set → `{'a', 'b', 'c'}`

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

### ✅ Expected Output

```
42
99
3.5
['a', 'b', 'c']
(1, 2, 3)
{1, 2, 3}
{'a': 1, 'b': 2}
```

### 🧠 Reasoning

* `str(42)` converts int to string → `"42"`
* `int("99")` converts string to int → `99`
* `float("3.5")` converts string to float → `3.5`
* `list("abc")` converts string to list of chars → `['a', 'b', 'c']`
* `tuple([1, 2, 3])` converts list to tuple → `(1, 2, 3)`
* `set([1, 2, 2, 3])` converts list to set (removes duplicate 2) → `{1, 2, 3}`
* `dict([...])` converts list of tuples to dict → `{'a': 1, 'b': 2}`

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

### ✅ Expected Output

```
True
True
True
True
True
True
True
```

### 🧠 Reasoning

* `isinstance(obj, type)` checks if object is of given type
* All examples match correct types
* `True` returns for all

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

### ✅ Expected Output

```
[1, 3]
{'x': 10, 'y': 20}
{2, 3}
```

### 🧠 Reasoning

* `lst.append(3)` adds at end → `[1, 2, 3]`
* `lst.remove(2)` removes value 2 → `[1, 3]`
* `d["y"] = 20` adds key-value pair → `{'x': 10, 'y': 20}`
* `s.add(3)` adds element → `{1, 2, 3}`
* `s.remove(1)` removes element → `{2, 3}`

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

### ✅ Expected Output

```
[99, 2, 3]
(1, 2, 3, 4)
[99, 2, 3, 4]
```

### 🧠 Reasoning

* Lists are mutable: `lst[0] = 99` works → modifies to `[99, 2, 3]`
* Tuples are immutable: `tpl[0] = 99` would error (not executed)
* `tpl + (4,)` creates new tuple → `(1, 2, 3, 4)`
* `lst + [4]` creates new list → `[99, 2, 3, 4]`

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

### ✅ Expected Output

```
{'items': [1, 2, 3]}
([1, 2, 3], 'text')
[{'a': 1, 'b': 2}]
```

### 🧠 Reasoning

* Dict value is list (mutable): can append → `{'items': [1, 2, 3]}`
* Tuple contains list: tuple immutable but list (content) mutable → can append → `([1, 2, 3], 'text')`
* List contains dict: can mutate inner dict → `[{'a': 1, 'b': 2}]`

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

### ✅ Expected Output

```
True
True
True
True
True
False
False
```

### 🧠 Reasoning

* Same values compare equal: `[1, 2] == [1, 2]` → `True`
* Sets unordered: `{1, 2} == {2, 1}` → `True`
* Different types never equal: `[1, 2] == (1, 2)` → `False`
* Different types never equal: `{1, 2} == [1, 2]` → `False`

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

### ✅ Expected Output

```
0
0
0
0
0
False
False
False
False
False
False
False
```

### 🧠 Reasoning

* Empty containers have length 0
* Empty containers are falsy in boolean context
* Also 0, None are falsy
* Non-empty, non-zero values are truthy

---

# 🎯 LEARNING CHECKLIST

After solving all 10:
- [ ] Can identify all Python types
- [ ] Understand mutability differences
- [ ] Can perform type conversions
- [ ] Know isinstance() usage
- [ ] Understand container nesting
- [ ] Know immutable vs mutable comparison

---

**Next:** Check MemoryModel assignments!
