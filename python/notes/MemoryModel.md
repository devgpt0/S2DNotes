# 🐍 PYTHON MEMORY MODEL

---

# 🔷 1. CORE CONCEPT

Every variable is a **reference** (label) pointing to an object in memory.

```text
Variable (Stack)    Object (Heap)
    x  ─────────►  [value]
```

---

# 🔷 2. STACK vs HEAP

| Stack | Heap |
| --- | --- |
| Stores references | Stores objects |
| Fast | Slower |
| Auto cleanup | Garbage collected |
| Variable addresses | Actual data |

---

# 🔷 3. ASSIGNMENT BEHAVIOR

## Reference Copy (objects)
```python
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3]  ← same object
```

Both variables point to **same object**

## Value Independence (reassignment)
```python
x = 10
y = x
y = 20
print(x)  # 10  ← different now
```

Immutable, so reassignment breaks link

---

# 🔷 4. MUTABLE vs IMMUTABLE IN MEMORY

## Mutable (list, dict, set)
```python
x = [1, 2]
y = x
y.append(3)
print(x)  # [1, 2, 3]  ← affects original
```

👉 **Mutation changes shared object**

## Immutable (int, str, tuple)
```python
x = "hello"
y = x
y = "world"
print(x)  # "hello"  ← unaffected
```

👉 **Reassignment creates/points to new object**

---

# 🔷 5. IDENTITY vs EQUALITY

## `is` → Identity (same object?)
```python
a = [1, 2]
b = a
print(a is b)  # True → same object

c = [1, 2]
print(a is c)  # False → different objects
```

## `==` → Equality (same value?)
```python
a = [1, 2]
c = [1, 2]
print(a == c)  # True → same content
print(a is c)  # False → different objects
```

---

# 🔷 6. FUNCTION ARGUMENTS

Python uses **call-by-sharing**:
* Function receives reference to object
* Mutations affect original
* Rebinding is local only

```python
def modify(lst):
    lst.append(10)  # ✅ affects original
    lst = [999]     # ❌ local rebind only

a = [1, 2]
modify(a)
print(a)  # [1, 2, 10]  ← mutation seen, rebind not
```

---

# 🔷 7. COPY OPERATIONS

## Reference Copy
```python
b = a  # same object, both affected
```

## Shallow Copy
```python
b = a[:]           # new list, same inner objects
b = a.copy()       # same as above
```

Nested objects still shared:
```python
x = [[1, 2]]
y = x[:]
y[0][0] = 99
print(x)  # [[99, 2]]  ← inner list shared
```

## Deep Copy
```python
import copy
b = copy.deepcopy(a)  # complete independence
```

---

# 🔷 8. DEFAULT MUTABLE ARGUMENTS (TRAP)

```python
def append_to(lst=[]):  # ❌ BAD
    lst.append(1)
    return lst

print(append_to())  # [1]
print(append_to())  # [1, 1]  ← persists!
```

Default is evaluated **once**, list persists

Solution:
```python
def append_to(lst=None):  # ✅ GOOD
    if lst is None:
        lst = []
    lst.append(1)
    return lst
```

---

# 🔷 9. GARBAGE COLLECTION

Objects are deleted when no references exist:

```python
x = [1, 2]
del x              # if no other refs, object deleted
```

Reference counting:
```python
import sys
x = [1, 2]
print(sys.getrefcount(x))  # shows ref count
```

---

# 🔷 10. CONTAINER REFERENCES

## Dict with list values
```python
d = {"a": [1, 2]}
d["a"].append(3)  # ✅ can mutate value
```

## Tuple with list
```python
t = ([1, 2], "text")
t[0].append(3)    # ✅ can mutate list inside
t[0] = [99]       # ❌ can't reassign tuple item
```

## Multiple references in list
```python
a = [1, 2]
lst = [a, a]
a.append(3)       # both lst[0] and lst[1] see change
```

---

# 🔷 11. INTEGER/STRING CACHING

Small integers cached (-5 to 256):
```python
a = 256
b = 256
print(a is b)  # True (cached)

c = 257
d = 257
print(c is d)  # False (not cached)
```

String literals interned:
```python
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True (pooled)

s3 = "".join(["h", "e", "l", "l", "o"])
print(s1 is s3)  # False (dynamic)
```

---

# 🔷 12. NONE, TRUE, FALSE (SINGLETONS)

Always same object:
```python
x = None
y = None
print(x is y)  # True

a = True
b = True
print(a is b)  # True
```

---

# 🔷 13. PASSING BY POSITION vs KEYWORD

```python
def func(a, b):
    a.append(1)
    b[0] = 99

x = [10]
y = [20]
func(x, y)
print(x, y)  # [10, 1] [99]  ← both mutated
```

---

# 🔷 14. MUTATION ORDER MATTERS

```python
def modify(lst):
    lst.append(100)      # mutation (affects original)
    lst = [888]          # rebind (local only)

x = [1, 2]
modify(x)
print(x)  # [1, 2, 100]  ← append seen, rebind not
```

---

# 🔷 15. OBJECT LIFECYCLE

```python
# Creation
x = [1, 2]         # object created, x references it

# Mutation
x.append(3)        # object modified

# Sharing
y = x              # y also references same object

# Rebinding
x = [99]           # x now references different object
                   # old list still referenced by y

# Deletion
del y              # if no other refs, old list deleted
```

---

# 🔷 16. GOLDEN RULES

1. **Variables are references** → labels to objects
2. **Assignment copies references** → both point to same object
3. **Mutable → mutation affects all references** → shared change
4. **Immutable → reassignment creates new object** → independent
5. **Function gets reference** → mutations seen, rebinds local
6. **Shallow copy → inner objects shared** → nested mutation affects original
7. **Deep copy → complete independence** → safe for nested structures
8. **Mutable defaults persist** → use None instead
9. **`is` checks identity** → don't use for numbers/strings
10. **`==` checks value** → use for comparisons

---

**Next:** Check Datatypes.md for what types exist!
