# ☕ JAVA — VARIABLES MODEL

---

## 🔷 1. VARIABLES — REAL MEANING

### 🧠 Definition

A variable is:

> **Either a value (primitive) OR a reference (address to object)**

---

## 🔹 Types

### 1. Primitive

```java
int a = 10;
```

* Stored directly in **stack**
* Holds **actual value**

---

### 2. Reference

```java
Person p = new Person();
```

* Stack → reference (address)
* Heap → object

---

## 🧠 Visualization

```text
Stack:         Heap:
p ───────►     [Person Object]
```

---

## 🔷 2. CORE OPERATIONS (THIS IS WHAT QUESTIONS TEST)

---

### 🔹 (A) Assignment

#### Primitive

```java
int a = 10;
int b = a;
```

👉 Copy of value

---

#### Object

```java
Person p2 = p1;
```

👉 Copy of reference (same object)

---

### 🔹 (B) Mutation vs Reassignment

#### Mutation

```java
p.name = "B";
```

👉 Same object modified

---

#### Reassignment

```java
p = new Person();
```

👉 New object, old unchanged

---

### 🔹 (C) Function Calls

Java is:

> ✅ **Always pass-by-value**

---

#### Primitive Case

```java
change(int x)
```

👉 Copy of value

---

#### Object Case

```java
change(Person p)
```

👉 Copy of reference

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

## 🔷 4. MOST ASKED INTERVIEW PATTERNS

---

### 🔥 Pattern 1: Primitive Copy

```java
int a = 5;
int b = a;
b = 10;
```

👉 `a` unchanged

---

### 🔥 Pattern 2: Shared Object

```java
Person p1 = new Person();
Person p2 = p1;
p2.name = "X";
```

👉 both change

---

### 🔥 Pattern 3: Reassignment Breaks Link

```java
p2 = new Person();
```

👉 no longer same object

---

### 🔥 Pattern 4: Function Mutation

```java
void f(Person p) {
    p.name = "X";
}
```

👉 original changes

---

### 🔥 Pattern 5: Function Reassignment

```java
void f(Person p) {
    p = new Person();
}
```

👉 original unchanged

---

### 🔥 Pattern 6: == vs equals

```java
a == b       // reference
a.equals(b)  // value
```

---

### 🔥 Pattern 7: String Pool

```java
String a = "hi";
String b = "hi";
```

👉 same reference

---

```java
String b = new String("hi");
```

👉 new object

---

## 🔷 5. COMMON MISTAKES (INTERVIEW TRAPS)

---

### ❌ Mistake 1

"Objects are passed by reference"

👉 WRONG
✔️ Java = pass-by-value (reference is copied)

---

### ❌ Mistake 2

"Assignment copies object"

👉 WRONG
✔️ It copies reference

---

### ❌ Mistake 3

"new modifies object"

👉 WRONG
✔️ It creates new object

---

## 🔷 6. FINAL MENTAL MODEL (CONDENSED)

If you remember ONLY this:

---

### 🧠 5 Golden Rules

1. Primitive → value stored directly
2. Object → reference to heap
3. Assignment → copies value/reference
4. Function → pass-by-value always
5. Mutation ≠ reassignment

---

## 🎯 HOW TO SOLVE ANY QUESTION

When given code:

---

### 🧠 Simulate like this:

```text
1. Draw stack
2. Draw heap
3. Track references
4. Check mutation vs new
5. Follow function calls
```

---

### Example Thinking

```java
Person p1 = new Person();
Person p2 = p1;
p2.name = "X";
```

```text
Stack:       Heap:
p1 ─┐
    ├──► Object(name="X")
p2 ─┘
```

Result: Both `p1` and `p2` point to the same object with `name="X"`

---

## Level 2

### Mental Model
Treat each variable as either a value slot (primitive) or an address slot (reference). For every line, ask: "Did I copy a value, copy an address, mutate an object, or rebind a reference?"

### Solve Steps
1. Draw stack variables first.
2. Draw heap objects and connect arrows.
3. Mark each statement as mutate or rebind.
4. Predict final object graph before output.

## Level 3

### Mental Model
Extend the object-graph model across function boundaries and multiple aliases. The hardest bugs come from hidden shared references.

### Solve Steps
1. Track alias count for each mutable object.
2. Track parameter passing as copy-of-reference.
3. Separate object identity (same object) from state equality (same content).
4. Validate behavior under null reassignment and nested objects.

---

### Level 2 Questions
1. If `Person p2 = p1; p2.name = "X";`, what prints from `p1.name` and why?
2. In a method parameter `change(Person p)`, what is the difference between `p.name = "A"` and `p = new Person()`?
3. How would you draw stack/heap after `Box b1 = new Box(); Box b2 = b1; b2 = new Box();`?

### Level 3 Questions
1. Why can aliasing across multiple helper methods cause hidden bugs even when each method looks correct locally?
2. What rule helps you decide if a statement changes shared state or only local binding?
3. How do identity checks differ from state checks in object-heavy code reviews?

---

## 🔷 2. EXECUTION MODEL

Understand how this topic runs in actual program flow:

- Read statement
- Resolve type/object/reference
- Execute operation (assignment, mutation, call, return)
- Update memory state (stack/heap bindings)
- Re-check final output from updated state
