
## Mental Model

> Think in terms of how data flows through memory and execution: what is copied, what is referenced, and what changes after each operation.

---

## Level 2

### Mental Model
Memory behavior is mostly reference counting plus cyclic garbage collection. Objects are reclaimed when unreachable.

### Solve Steps
1. Track strong references that keep objects alive.
2. Detect cycles for container-heavy designs.
3. Distinguish shallow copy from deep copy.
4. Use explicit cleanup for external resources.

## Level 3

### Mental Model
In production systems, memory issues are often lifetime and ownership issues, not syntax issues. Ownership boundaries must be explicit.

### Solve Steps
1. Define who owns long-lived objects.
2. Minimize hidden global references and caches.
3. Audit thread/process boundaries for copy/share semantics.
4. Monitor memory with repeatable load scenarios.

---

### Level 2 Questions
1. Why does deleting one variable name not always free object memory?
2. What is the difference between reference counting cleanup and cyclic GC cleanup?
3. How does `copy.copy` differ from `copy.deepcopy` for nested data?

### Level 3 Questions
1. What ownership mistakes usually cause memory growth in long-running apps?
2. Why can global caches become hidden memory leaks?
3. What memory model checks do you run before introducing concurrency?

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
