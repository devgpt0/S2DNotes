
## Mental Model

> Think in terms of how data flows through memory and execution: what is copied, what is referenced, and what changes after each operat---

## Level 2

### Mental Model
Data type choice is an algorithm decision. Each type offers different mutability, lookup cost, and memory behavior.

### Solve Steps
1. Pick type by access pattern (index, hash, order, uniqueness).
2. Check mutability constraints for safe sharing.
3. Track copy depth for nested structures.
4. Validate complexity hotspots in loops.

## Level 3

### Mental Model
Some performance and identity behavior comes from CPython internals (interning, object headers, allocator). Use internals for optimization, not for correctness assumptions.

### Solve Steps
1. Keep correctness independent of implementation quirks.
2. Profile before micro-optimizing data structures.
3. Use tuple/frozenset for stable hashable keys.
4. Avoid accidental quadratic behavior in repeated copies.

---

### Level 2 Questions
1. Why is `set` preferred over `list` for fast membership checks?
2. What practical differences matter between `list` and `tuple` in shared code?
3. How does shallow copy behave with nested containers?

### Level 3 Questions
1. Why should implementation details (like interning) not be used for correctness logic?
2. How do you choose between readability and micro-optimization for data structures?
3. What data-type choices reduce accidental quadratic behavior?

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
