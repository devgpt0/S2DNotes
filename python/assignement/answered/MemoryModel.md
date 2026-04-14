# 🐍 PYTHON MEMORY MODEL ASSIGNMENT (ANSWERED)

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

### ✅ Expected Output

```
[1, 2, 3]
10
```

### 🧠 Reasoning

* `a = [1, 2]` creates list, `a` references it
* `b = a` makes `b` reference same list
* `b.append(3)` mutates shared list
* Both `a` and `b` point to same object → both see change → `[1, 2, 3]`

* `x = 10` creates int, `x` references it
* `y = x` makes `y` reference same int
* `y = 20` rebinds `y` to different int object
* Now `x` points to 10, `y` points to 20 → independent → `10`

👉 **Mutable: mutation affects original | Immutable: reassignment creates new object**

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

### ✅ Expected Output

```
True
False
True
True
```

### 🧠 Reasoning

* `a = [1, 2]` creates list object in memory
* `b = a` makes `b` reference same object
* `c = [1, 2]` creates different list object

* `a is b` → same object? **True** (both reference same list)
* `a is c` → same object? **False** (different objects, different memory)
* `a == b` → same value? **True** (both contain [1, 2])
* `a == c` → same value? **True** (both contain [1, 2])

👉 **`is` checks identity (memory), `==` checks equality (value)**

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

### ✅ Expected Output

```
[[99, 2], [3, 4]]
[[99, 2], [3, 4]]
```

### 🧠 Reasoning

* `x = [[1, 2], [3, 4]]` creates outer list with inner list references
* `y = x[:]` creates shallow copy:
  - New outer list
  - But inner lists are still references to original
* `y[0][0] = 99` modifies inner list that `x[0]` also references
* Both `x` and `y` see the mutation

👉 **Shallow copy creates new container, but contents still shared**

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

### ✅ Expected Output

```
{'a': [1, 2, 3]}
{'a': [1, 2, 3]}
```

### 🧠 Reasoning

* `d1 = {"a": [1, 2]}` creates dict with list value
* `d2 = d1.copy()` creates shallow copy:
  - New dict object
  - But list value is still reference to original
* `d2["a"].append(3)` mutates the shared list
* Both `d1` and `d2` reference same list → both see change

👉 **Dict.copy() is shallow: values remain references**

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

### ✅ Expected Output

```
[1, 2, 100]
```

### 🧠 Reasoning

* Function receives reference to list object (call-by-sharing)
* `lst.append(100)` mutates the object
* Original `x` references same object
* Mutation is visible outside function → `[1, 2, 100]`

👉 **Function receives reference: mutations affect original**

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

### ✅ Expected Output

```
[1, 2]
```

### 🧠 Reasoning

* Function receives reference to list object
* `lst = [999]` rebinds parameter to new list (local only)
* `lst.append(200)` modifies new list (not original)
* Rebinding is local to function scope
* Original `x` unchanged → `[1, 2]`

👉 **Function rebinding is local: doesn't affect original**

---

## 🔹 ASSIGNMENT 7: Tuple Mutability

### Question

```python
t = ([1, 2], "text")

t[0].append(3)
print(t)

# t[0] = [99]  # Would error
```

### ✅ Expected Output

```
([1, 2, 3], 'text')
```

### 🧠 Reasoning

* Tuple is immutable: can't reassign items
* But items can be mutable (list inside)
* `t[0].append(3)` mutates the inner list (allowed)
* Tuple itself unchanged structure, but contents mutated

👉 **Tuple is immutable container, but contents can be mutable**

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

### ✅ Expected Output

```
[1, 2, 3]
[1, 2, 3]
[[1, 2, 3], [1, 2, 3]]
```

### 🧠 Reasoning

* `a = [1, 2]` creates list
* `b = a` references same list
* `c = [a, a]` creates list containing **two references to same list**
* `a.append(3)` mutates the list
* `a` and `b` both reference it → both show `[1, 2, 3]`
* `c[0]` and `c[1]` are references to same object → both show `[1, 2, 3]`

👉 **List can contain multiple references to same object**

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

### ✅ Expected Output

```
[1]
[1, 1]
[1, 1, 1]
```

### 🧠 Reasoning

* Default `lst=[]` evaluated ONCE at function definition
* Same list object persists across calls
* First call: `[].append(1)` → `[1]`
* Second call: `[1].append(1)` → `[1, 1]` (same list)
* Third call: `[1, 1].append(1)` → `[1, 1, 1]` (same list accumulating)

⚠️ **TRAP: Mutable defaults persist across calls!**

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

### ✅ Expected Output

```
True
False
True
```

### 🧠 Reasoning

* Python caches integers -5 to 256 for optimization
* `a = 256, b = 256` both reference cached object → `True`
* `c = 257, d = 257` outside cache, separate objects → `False`
* `x = 256 + 0` evaluates to 256, hits cache
* `y = 256` direct assignment, also cached
* Both hit cache → `True`

⚠️ **Caching only guaranteed for -5 to 256**

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

### ✅ Expected Output

```
True
True
False
True
```

### 🧠 Reasoning

* String literals interned automatically (pooled)
* `s1 = "hello"` interned
* `s2 = "hello"` same literal, reused → `True`
* `s3 = "hel" + "lo"` compile-time optimization, results in interned "hello" → `True`
* `s4 = "".join(...)` dynamically constructed, NOT auto-interned → `False`
* `s1 == s4` same value, different objects → `True`

👉 **Literals interned; dynamic strings not**

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

### ✅ Expected Output

```
[[99, 2], [3, 4]]
[99, 2]
[99, 99]
```

### 🧠 Reasoning

* `a, b = lst` unpacks list
* `a` references `[1, 2]`
* `b` references `[3, 4]`
* `a[0] = 99` mutates shared inner list → `lst[0]` also shows `[99, 2]`
* `b = [99, 99]` rebinds `b` to new list (local variable)
* `lst[1]` unchanged `[3, 4]` (not affected by rebinding)

👉 **Unpacking creates references; rebinding is local**

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

### ✅ Expected Output

```
{1, 2}
{'a': {1, 2, 3}}
```

### 🧠 Reasoning

* `s1 = {1, 2}` creates set
* `s2 = s1.copy()` creates independent copy
* `s2.add(3)` only affects `s2`
* `s1` unchanged → `{1, 2}`

* `d1 = {"a": {1, 2}}` dict with set value
* `d2 = d1.copy()` shallow copy (set value is reference)
* `d2["a"].add(3)` mutates shared set
* `d1["a"]` also affected → `{'a': {1, 2, 3}}`

👉 **Set.copy() independent; Dict values in shallow copy shared**

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

### ✅ Expected Output

```
[{'a': [1, 2, 99]}]
[{'a': [1, 2, 99]}]
```

### 🧠 Reasoning

* `data = [{"a": [1, 2]}]` list with dict with list
* `copy = data[:]` shallow copy:
  - New outer list
  - But dict inside still referenced
  - And list inside dict still referenced
* `copy[0]["a"].append(99)` mutates deeply nested list
* `data` sees mutation (same objects) → both show `[{'a': [1, 2, 99]}]`

👉 **Shallow copy of container with nested mutables still shares deep objects**

---

## 🔹 ASSIGNMENT 15: Garbage Collection

### Question

```python
x = [1, 2]
y = x
del x

print(y)  # Will this work?
```

### ✅ Expected Output

```
[1, 2]
```

### 🧠 Reasoning

* `x = [1, 2]` creates list, `x` references it
* `y = x` creates another reference to same list
* `del x` removes variable `x` (but object still referenced by `y`)
* List object NOT garbage collected (reference count > 0)
* `y` still references list → `print(y)` works → `[1, 2]`

👉 **Object survives if any reference exists**

---

# 🎯 LEARNING CHECKLIST

After solving all 15:
- [ ] Understand reference vs value
- [ ] Know identity vs equality
- [ ] Understand shallow copy pitfall
- [ ] Know function mutation behavior
- [ ] Understand rebinding is local
- [ ] Know mutable defaults trap
- [ ] Understand integer caching limits
- [ ] Know string interning behavior
- [ ] Understand unpacking creates references
- [ ] Know garbage collection basics

---

**Congratulations!** You've mastered Python memory and data types! 🎉
