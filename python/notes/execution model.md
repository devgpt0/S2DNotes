# 🐍 PYTHON — LEVEL 1 NOTES: EXECUTION MODEL

---

# 🔷 1. EXECUTION MODEL

## 🧠 Mental Model

```text
.py → bytecode → Python Virtual Machine (PVM)
```

* Python compiles code into **bytecode**
* Bytecode runs in **Python interpreter (PVM)**
* No aggressive JIT (in CPython)

👉 Execution is **dynamic + interpreted**

---

# 🔷 2. CORE MEMORY MODEL

## 🧠 Fundamental Rule

> ❗ **Everything in Python is an object (stored in heap)**

---

## 🔹 Variables

A variable is:

> **a label (reference) pointing to an object**

---

## 🧠 Visualization

```text
x = 10

x ─────► [10 object]
```

---

# 🔷 3. ASSIGNMENT (MOST IMPORTANT)

## 🧠 Rule

> ❗ Assignment does NOT copy object
> ❗ It copies the reference

---

### Example Thinking

```python
a = [1,2]
b = a
```

```text
a ─┐
   ├──► [1,2]
b ─┘
```

👉 Both refer to same object

---

# 🔷 4. MUTABLE vs IMMUTABLE

---

## 🔹 Immutable Objects

* int, float, str, tuple

### Behavior:

> ❗ Any modification → NEW object created

---

### Mental Model

```python
x = 10
y = x
y += 1
```

```text
x ─────► [10]

y ─────► [11]   (new object)
```

---

## 🔹 Mutable Objects

* list, dict, set

### Behavior:

> ❗ Modification happens in SAME object

---

### Mental Model

```python
x = [1]
y = x
y.append(2)
```

```text
x ─┐
   ├──► [1,2]
y ─┘
```

---

# 🔷 5. MUTATION vs REBINDING

---

## 🔹 Mutation

```python
x.append(3)
```

👉 Changes existing object

---

## 🔹 Rebinding

```python
x = [1,2]
```

👉 New object created, variable now points to it

---

## 🧠 Key Difference

| Operation | Effect      |
| --------- | ----------- |
| Mutation  | same object |
| Rebinding | new object  |

---

# 🔷 6. FUNCTION ARGUMENT MODEL

## 🧠 Python uses:

> ✅ **Call-by-sharing (object reference passed)**

---

## 🔹 What it means

* Function gets **reference to same object**
* Behavior depends on operation

---

### Case 1: Mutation

```python
def f(x):
    x.append(10)
```

👉 Original object changes

---

### Case 2: Rebinding

```python
def f(x):
    x = [1,2]
```

👉 Only local variable changes

---

# 🔷 7. INTERVIEW MENTAL MODEL (STEP-BY-STEP)

When solving any question:

---

## 🧠 Step 1: Everything is object

* No primitives

---

## 🧠 Step 2: Track references

* Which variables point to same object?

---

## 🧠 Step 3: Check type

* Mutable or immutable?

---

## 🧠 Step 4: Identify operation

* Mutation → same object changes
* Rebinding → new object

---

## 🧠 Step 5: Function behavior

* Object shared
* Reassignment local

---

# 🔷 8. COMMON INTERVIEW PATTERNS

---

### 🔥 Pattern 1: Shared Reference

```python
a = [1,2]
b = a
```

👉 same object

---

### 🔥 Pattern 2: Copy

```python
b = a[:]
```

👉 new object

---

### 🔥 Pattern 3: Immutable Update

```python
x = 10
x += 1
```

👉 new object

---

### 🔥 Pattern 4: Function Mutation

```python
def f(x):
    x.append(1)
```

👉 affects original

---

### 🔥 Pattern 5: Function Rebinding

```python
def f(x):
    x = []
```

👉 no effect outside

---

# 🔷 9. COMMON MISTAKES (VERY IMPORTANT)

---

### ❌ "Python variables store values"

👉 WRONG
✔️ They store **references**

---

### ❌ "Assignment copies object"

👉 WRONG
✔️ Copies reference

---

### ❌ "Functions pass by reference"

👉 WRONG
✔️ Call-by-sharing

---

### ❌ "x += always mutates"

👉 WRONG
✔️ Depends on mutability

---

# 🔷 10. FINAL MENTAL MODEL (CONDENSED)

---

### 🧠 5 Golden Rules

1. Everything = object
2. Variable = reference (label)
3. Assignment = reference copy
4. Mutable → same object changes
5. Immutable → new object created

---

# 🎯 HOW TO THINK IN INTERVIEW

---

When you see code:

```text
1. Draw objects in heap
2. Track which variable points where
3. Check mutable vs immutable
4. Identify mutation vs rebinding
5. Follow function flow
```

---

# 🚀 LEVEL 1 TARGET

You should be able to:

* Predict output of simple code
* Explain reference behavior clearly
* Distinguish mutation vs reassignment instantly

---

**Ready for assignments?** Check the `assignement/test` folder to test your understanding!

**Next Level:** Level 2 covers hidden traps = nested lists, default args, shallow/deep copy, interning edge cases

---

## Level 2

### Mental Model
Python executes bytecode in frames. Each call creates a frame with local namespace, and control flow moves frame to frame.

### Solve Steps
1. Trace frame creation for each call.
2. Track local, global, and built-in lookups.
3. Follow exception propagation frame-by-frame.
4. Use this model to debug recursion and state leakage.

## Level 3

### Mental Model
Concurrency model depends on runtime strategy: threads share memory under GIL, processes isolate memory, asyncio shares one event loop.

### Solve Steps
1. Choose model first (threads/processes/asyncio).
2. Predict shared-state hazards only where memory is shared.
3. Use queues/messages for process communication.
4. In async code, reason at await boundaries.

---

### Level 2 Questions
1. What is a Python frame and what does it store?
2. How are local/global/built-in names resolved during execution?
3. How does an exception travel through nested calls?

### Level 3 Questions
1. Before each `await`, what state assumptions must be re-validated?
2. Why do process-based workers avoid many shared-memory bugs?
3. When does threading still need locks despite the GIL?

---

## 🔷 2. EXECUTION MODEL

Understand how this topic runs in actual program flow:

- Read statement
- Resolve type/object/reference
- Execute operation (assignment, mutation, call, return)
- Update memory state (stack/heap bindings)
- Re-check final output from updated state


---

## 🔷 3. INTERVIEW MENTAL MODEL (STEP-BY-STEP)

When you see ANY question:

---

### 🧠 Step 1: Identify variable type

* Primitive? → value
* Object? → reference

---

### 🧠 Step 2: Where is it stored?

* Primitive → stack
* Object → heap (via reference)

---

### 🧠 Step 3: Assignment behavior

* Primitive → copy value
* Object → copy reference

---

### 🧠 Step 4: Operation type

* Field change → mutation
* `new` → new object (reassignment)

---

### 🧠 Step 5: Function call

* Always pass-by-value
* Object → reference copied

---
