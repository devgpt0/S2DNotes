# ☕ JAVA — EXECUTION MODEL

---

## 🔷 1. EXECUTION MODEL (What actually runs?)

### 🧠 Mental Model

```text
.java → javac → .class (bytecode) → JVM → execution
```

### What you must say in interview:

* Java compiles to **bytecode**
* Runs on **JVM**
* JVM interprets + uses **JIT** for optimization

👉 You don't run Java directly—you run **bytecode inside JVM**

---

## 🔷 2. MEMORY MODEL (CORE FOUNDATION)

### 🧠 Think in 2 areas only (Level 1)

```text
STACK (per thread)         HEAP (shared)
-------------------        -------------------
local variables            objects
function calls             instances
references                 dynamic memory
```

---

### 🔥 Rule

* **Stack → stores variables**
* **Heap → stores objects**

---

## Key Takeaways

| Aspect | Stack | Heap |
|--------|-------|------|
| Scope | Per Thread | Shared |
| Storage | Variables, References | Objects, Instances |
| Memory Management | Automatic (LIFO) | Garbage Collection |
| Speed | Faster | Slower |
| Size | Limited | Larger |

---

## Level 2

### Mental Model
Execution is a pipeline: source -> bytecode -> class loading -> stack frame execution. Each method call creates a new frame with its own locals.

### Solve Steps
1. Identify compile-time type checks.
2. Identify runtime class loading and method dispatch.
3. Trace call stack push/pop for each method call.
4. Predict where exceptions unwind the stack.

## Level 3

### Mental Model
Hot code is optimized by JIT, but semantics do not change. Think "same result, different machine path" with possible de-optimization.

### Solve Steps
1. Separate language semantics from JVM optimization details.
2. Consider inlining and escape analysis only as performance factors.
3. Use happens-before rules when reasoning about threads.
4. For confusing output, trust Java semantics first, then performance model.

---

### Level 2 Questions
1. Trace the execution path from `.java` source to actual machine execution in JVM.
2. What is created on call stack for each method call, and when is it removed?
3. How does exception propagation change normal frame pop order?

### Level 3 Questions
1. Why do JIT optimizations not change Java language semantics?
2. What is de-optimization in JVM and when can it occur?
3. Which execution-model assumptions break first when concurrency is introduced?

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
