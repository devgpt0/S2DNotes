# 🐍 PYTHON DATA TYPES

---

# 🔷 1. WHAT ARE DATA TYPES?

A data type defines what kind of data an object holds and how it behaves.

---

# 🔷 2. CATEGORIES

## Mutable Types (can be changed)
* `list` - ordered collection
* `dict` - key-value pairs
* `set` - unordered unique values

## Immutable Types (cannot be changed)
* `int` - integer numbers
* `float` - decimal numbers
* `str` - text/strings
* `tuple` - ordered collection (frozen)
* `frozenset` - set (frozen)
* `bool` - True/False
* `None` - null value

---

# 🔷 3. MUTABLE TYPES

## List
```python
lst = [1, 2, 3]
lst.append(4)      # changes original
lst[0] = 99        # can reassign items
```

👉 Modifying changes the object itself

## Dict
```python
d = {"a": 1}
d["b"] = 2         # can add items
d["a"] = 99        # can change values
```

👉 Can add/modify/remove keys

## Set
```python
s = {1, 2, 3}
s.add(4)           # can add elements
s.remove(1)        # can remove elements
```

👉 Unordered, no duplicates

---

# 🔷 4. IMMUTABLE TYPES

## String
```python
s = "hello"
s[0] = "H"         # ❌ ERROR - cannot change
s = "Hello"        # ✅ Can reassign to new string
```

👉 Cannot modify, can only create new

## Tuple
```python
t = (1, 2, 3)
t[0] = 99          # ❌ ERROR - cannot change
t = (9, 9, 9)      # ✅ Can reassign to new tuple
```

👉 Like list but immutable

## Int/Float/Bool/None
```python
x = 10
x = 20             # reassign, not modify
x = x + 5          # creates new object
```

---

# 🔷 5. MUTABLE vs IMMUTABLE BEHAVIOR

When assigned:

```python
# Mutable (shared)
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3] → shared reference

# Immutable (independent)
x = 10
y = x
y = 20
print(x)  # 10 → independent
```

---

# 🔷 6. TYPE CHECKING

```python
isinstance(5, int)           # True
isinstance("hello", str)     # True
isinstance([1, 2], list)     # True
isinstance((1, 2), tuple)    # True
isinstance({1, 2}, set)      # True
isinstance({"a": 1}, dict)   # True
isinstance(True, bool)       # True
isinstance(None, type(None)) # True
```

---

# 🔷 7. TYPE CONVERSION

```python
# To string
str(5)           # "5"
str([1, 2])      # "[1, 2]"

# To int
int("5")         # 5
int(5.9)         # 5 (truncates)
int(True)        # 1

# To float
float("5.5")     # 5.5
float(5)         # 5.0

# To list
list({1, 2})     # Random order
list("abc")      # ['a', 'b', 'c']

# To tuple
tuple([1, 2])    # (1, 2)
tuple("abc")     # ('a', 'b', 'c')

# To dict
dict([("a", 1)]) # {"a": 1}

# To set
set([1, 2, 2])   # {1, 2}
set("aab")       # {'a', 'b'}
```

---

# 🔷 8. MUTABLE + IMMUTABLE INTERACTION

```python
# Dict with list values (mutable value)
d = {"key": [1, 2]}
d["key"].append(3)     # ✅ Can mutate the list value

# Tuple with list inside (mutable content)
t = ([1, 2], "text")
t[0].append(3)         # ✅ Can mutate the list inside tuple

# List of dicts (mutable list, mutable items)
lst = [{"a": 1}]
lst[0]["b"] = 2        # ✅ Can mutate inner dict
```

---

# 🔷 9. DEFAULT TYPES

```python
# Empty collections
[] = list()            # empty list
{} = dict()            # empty dict
() = tuple()           # empty tuple
set()                  # empty set
```

---

# 🔷 10. KEY RULES

| Type | Mutable | Can be in Set/Dict Key |
| --- | --- | --- |
| list | Yes | No |
| dict | Yes | No |
| set | Yes | No |
| tuple | No | Yes (if empty/immutable) |
| str | No | Yes |
| int | No | Yes |

---

# 🔷 11. COMMON OPERATIONS

```python
# Length
len([1, 2, 3])         # 3
len("hello")           # 5
len({"a": 1, "b": 2})  # 2

# Access
lst[0]                 # first element
s[1]                   # second character
d["key"]               # value by key

# Check membership
1 in [1, 2, 3]         # True
"a" in "abc"           # True
"key" in {"key": 1}    # True (checks keys)
```

---

# 🔷 12. ITERATION

```python
# List
for item in [1, 2, 3]:
    print(item)

# String
for char in "hello":
    print(char)

# Dict
for key in {"a": 1, "b": 2}:
    print(key)      # prints keys

# Dict items
for key, value in {"a": 1}.items():
    print(key, value)
```

---

# 🔷 13. SUMMARY TABLE

| Type | Mutable | Ordered | Duplicates | Example |
| --- | --- | --- | --- | --- |
| list | Yes | Yes | Yes | [1, 2, 2] |
| tuple | No | Yes | Yes | (1, 2, 2) |
| dict | Yes | Yes* | Keys unique | {"a": 1} |
| set | Yes | No | No | {1, 2} |
| str | No | Yes | Yes | "hello" |
| int | No | N/A | N/A | 42 |

*Python 3.7+ maintains insertion order

---

**Next:** Check MemoryModel.md for how data types behave in memory!
