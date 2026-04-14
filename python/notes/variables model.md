# 🐍 PYTHON — LEVEL 1 NOTES: VARIABLES MODEL

---

# 🔷 1. WHAT IS A VARIABLE?

## 🧠 Mental Model

> **A variable is a label (reference) pointing to an object in memory**

---

### NOT a Container

> ❌ Variables do NOT store values inside them
> ✅ Variables REFERENCE objects that store values

---

## 🧠 Visualization

```text
Variable (Stack)     Object (Heap)
    x  ─────────────► [10]
```

---

# 🔷 2. CORE PRINCIPLE

## ❗ Everything in Python is an object

* **int** → object
* **str** → object
* **list** → object
* **function** → object
* **module** → object

---

## All objects are stored in HEAP

Variables are just **labels pointing to heap objects**

---

# 🔷 3. ASSIGNMENT BEHAVIOR

## 🧠 Rule: Assignment Copies REFERENCE, NOT Object

---

### Example 1: Mutable Assignment

```python
a = [1, 2]
b = a
```

```text
a ─┐
   ├──► [1, 2]  (one object in heap)
b ─┘
```

**Both point to SAME object**

---

### Example 2: Immutable Assignment

```python
x = 10
y = x
```

```text
x ─┐
   ├──► [10]    (immutable, typically same object due to caching)
y ─┘
```

**Reference copied, not value**

---

# 🔷 4. MUTABLE vs IMMUTABLE BEHAVIOR

---

## 🔹 Mutable Objects

**list, dict, set**

### Property:

> ❗ Modifications change the SAME object

---

### Example

```python
x = [1, 2]
y = x
y.append(3)
print(x)  # [1, 2, 3]  ← x also changed!
```

```text
Before: x ─┐
           ├──► [1, 2]
        y ─┘

After:  x ─┐
           ├──► [1, 2, 3]  ← SAME object modified
        y ─┘
```

---

## 🔹 Immutable Objects

**int, float, str, tuple**

### Property:

> ❗ Any modification creates NEW object

---

### Example

```python
x = 10
y = x
y = y + 1  # or y += 1
print(x)   # 10  ← x unchanged
print(y)   # 11
```

```text
Before: x ─────► [10]
        y ─────┘

After:  x ─────► [10]        (original, unchanged)
        y ─────► [11]        (new object created)
```

---

# 🔷 5. MUTATION vs REBINDING

---

## 🔹 Mutation

Changes the object itself

```python
x = [1, 2]
x.append(3)  # ← mutation
```

```text
x ─────► [1, 2, 3]
         (same object, modified)
```

---

## 🔹 Rebinding

Points to a different object

```python
x = [1, 2]
x = [3, 4]  # ← rebinding
```

```text
Before: x ─────► [1, 2]
After:  x ─────► [3, 4]  (new object)
```

---

## 🧠 CRITICAL DIFFERENCE

| Action    | Mutable | Immutable |
| --------- | ------- | --------- |
| Mutation  | Same object | N/A |
| Rebinding | New reference | New object |

---

# 🔷 6. FUNCTION ARGUMENTS (CALL-BY-SHARING)

---

## 🧠 Python uses: Call-by-sharing

> Function parameter receives a REFERENCE to the same object

---

### Case 1: Mutation (Affects Original)

```python
def modify(lst):
    lst.append(10)  # mutation

a = [1, 2]
modify(a)
print(a)  # [1, 2, 10]  ← changed!
```

```text
Inside function:
lst ─┐
     ├──► [1, 2, 10]  ← SAME object modified
a ─┘
```

---

### Case 2: Rebinding (Local Only)

```python
def modify(lst):
    lst = [999]  # rebinding

a = [1, 2]
modify(a)
print(a)  # [1, 2]  ← unchanged!
```

```text
Inside function:
lst ─────► [999]  (new local object, function scope only)
a ─────► [1, 2]   (unchanged, still original)
```

---

# 🔷 7. IDENTITY vs EQUALITY

---

```python
a is b   # → Are they the SAME object? (identity)
a == b   # → Do they have the SAME value? (equality)
```

---

## 🧠 Key Difference

### `is` → Identity Check

* Checks if both variables point to same object in memory
* Compares memory addresses

```python
a = [1, 2]
b = a
print(a is b)  # True  (same object)
```

---

### `==` → Equality Check

* Checks if both objects have same value
* Compares content

```python
a = [1, 2]
c = [1, 2]
print(a == c)  # True  (same value)
print(a is c)  # False (different objects)
```

---

## 🧠 Table

```python
a = [1, 2]
b = a
c = [1, 2]
```

| Expression | Result | Why |
| --- | --- | --- |
| `a is b` | `True` | Same object in memory |
| `a == b` | `True` | Same content |
| `a is c` | `False` | Different objects |
| `a == c` | `True` | Same content |

---

# 🔷 8. COPY vs REFERENCE

---

## 🔹 Reference Copy

```python
b = a
```

* Creates new variable
* Points to SAME object
* Both see mutations

```text
a ─┐
   ├──► [1, 2]
b ─┘
```

---

## 🔹 Shallow Copy

```python
b = a[:]  # or b = a.copy()
```

* Creates NEW object
* Copies content at top level
* Mutations don't affect original

```text
a ─────► [1, 2]
b ─────► [1, 2]  (different object, same content)
```

---

# 🔷 9. STEP-BY-STEP MENTAL MODEL

---

When analyzing code:

---

## 🧠 Step 1: Variables are references

* Track which variable points where
* Not "what value does x hold" but "what object does x refer to"

---

## 🧠 Step 2: Identify object type

* Mutable? (list, dict, set)
* Immutable? (int, str, tuple)

---

## 🧠 Step 3: Identify operation

* **Mutation:** `x.append()`, `x[0] = val`, `x.pop()`
* **Rebinding:** `x = new_value`

---

## 🧠 Step 4: Apply rules

* Mutable + mutation → shared object changes
* Immutable + rebinding → new object created
* Function argument → reference passed, mutation affects original

---

# 🔷 10. COMMON MISTAKES

---

### ❌ Mistake 1: "Variables store values"

```python
x = 10  # ❌ "x stores 10"
```

✔️ Correct: "x is a reference to object 10"

---

### ❌ Mistake 2: "Assignment copies the object"

```python
b = a  # ❌ "copied a to b"
```

✔️ Correct: "b now references the same object as a"

---

### ❌ Mistake 3: "Functions pass by reference"

✔️ Correct: "Functions use call-by-sharing (reference passed)"

---

### ❌ Mistake 4: "x += always mutates"

```python
x = [1]
x += [2]  # ✔️ Mutates (in-place for lists)

y = 10
y += 5    # ❌ Does NOT mutate (creates new int)
```

✔️ Correct: "Immutable objects create new object, mutable objects may mutate in-place"

---

# 🔷 11. FINAL MENTAL MODEL (5 GOLDEN RULES)

---

### 🧠 Master These 5 Rules

1. **Everything is an object** → stored in heap
2. **Variables are references** → labels pointing to objects
3. **Assignment = reference copy** → both point to same object
4. **Mutable objects** → mutation changes shared object
5. **Immutable objects** → reassignment creates new object

---

# 🎯 HOW TO THINK IN INTERVIEW

---

### Process:

```text
1️⃣ Draw boxes for objects in heap
2️⃣ Draw arrows for references (variables)
3️⃣ Identify mutable vs immutable
4️⃣ Track mutation vs rebinding
5️⃣ Follow function flow
6️⃣ Predict output
```

---

# 🚀 LEVEL 1 MASTERY GOALS

By end of Level 1, you should:

✅ Instantly recognize reference behavior
✅ Explain mutation vs reassignment clearly
✅ Predict output without running code
✅ Distinguish `is` from `==`
✅ Handle function arguments confidently

---

**Ready to test?** Go to `assignement/test` folder!

**Next Level:** Level 2 = nested structures, default arguments, integer caching, string interning, deep copy
