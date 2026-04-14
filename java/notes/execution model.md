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
