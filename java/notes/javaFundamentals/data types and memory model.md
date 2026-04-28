# ☕ JAVA — LEVEL 1 NOTES: DATA TYPES & MEMORY BEHAVIOR

---

# 🔷 1. WHAT ARE DATA TYPES (INTERVIEW VIEW)

## 🧠 Definition

A data type defines:

> **what kind of data is stored + how much memory + how it behaves**

---

## 🔹 Two Categories

```text
1. Primitive Types
2. Reference Types
```

---

# 🔷 2. PRIMITIVE DATA TYPES

---

## 🔹 List (Must Know)

```text
Integer Types:  int, long, short, byte
Floating Point: float, double
Character:      char
Boolean:        boolean
```

---

## 🔹 Memory Behavior

```text
✅ Stored directly in STACK
✅ Fixed size
✅ No object involved
✅ Fast access
```

---

## 🧠 Example

```java
int a = 10;
```

```text
Stack:
a = 10
(value stored directly)
```

---

## 🔹 Key Properties

| Property | Primitive  |
| -------- | ---------- |
| Storage  | Stack      |
| Size     | Fixed      |
| Speed    | Fast       |
| Copy     | Value copy |
| Null?    | ❌          |

---

# 🔷 3. REFERENCE DATA TYPES

---

## 🔹 Examples

```text
String, Array, Class objects, Wrapper classes
(Integer, Double, Boolean, etc.)
```

---

## 🔹 Memory Behavior

```text
Stack → stores REFERENCE (memory address)
Heap → stores ACTUAL OBJECT
```

---

## 🧠 Example

```java
String s = "hello";
```

```text
Stack:           Heap:
s ─────►         ["hello"]
(address)        (actual string object)
```

---

## 🔹 Key Properties

| Property | Reference      |
| -------- | -------------- |
| Storage  | Stack + Heap   |
| Variable | Holds address  |
| Copy     | Reference copy |
| Mutable? | Depends        |
| Size     | Dynamic        |
| Null?    | ✅              |

---

# 🔷 4. PRIMITIVE vs REFERENCE (CORE INTERVIEW TABLE)

| Feature          | Primitive    | Reference      |
| ---------------- | ------------ | -------------- |
| Stored in        | Stack        | Heap (object)  |
| Variable holds   | Value        | Address        |
| Assignment       | Value copy   | Reference copy |
| Null allowed     | ❌            | ✅              |
| Default value    | 0,false      | null           |
| Mutable          | N/A          | Depends        |

---

# 🔷 5. MEMORY BEHAVIOR RULES (INTERVIEW CORE)

---

## 🔥 Rule 1: Primitive = Independent

```java
int a = 10;
int b = a;
b = 20;
```

💭 Explanation:
* `a = 10` → value 10 in stack
* `b = a` → **copies the value** (not reference)
* Each variable has its own copy
* Changing `b` does NOT affect `a`

👉 Output: `a = 10, b = 20`

---

## 🔥 Rule 2: Reference = Shared

```java
Person p1 = new Person();
Person p2 = p1;
```

💭 Explanation:
* `new Person()` → object created in heap
* `p2 = p1` → **copies the reference** (address)
* Both point to **same object**
* Changes affect both

👉 Both see same object

---

## 🔥 Rule 3: `new` = New Object

```java
p2 = new Person();
```

💭 Explanation:
* `new` always creates a **new object in heap**
* `p2` now points to different object
* Breaks the link with `p1`

👉 Now they reference different objects

---

## 🔥 Rule 4: Default Values

| Type       | Default | Storage |
| ---------- | ------- | ------- |
| int        | 0       | Stack   |
| double     | 0.0     | Stack   |
| boolean    | false   | Stack   |
| char       | '\0'    | Stack   |
| String     | null    | Stack   |
| Object     | null    | Stack   |

---

# 🔷 6. STRING MEMORY (VERY IMPORTANT FOR INTERVIEWS)

---

## 🔹 String Literals → String Pool

```java
String a = "hello";
String b = "hello";
```

```text
a ─┐
   ├──► "hello" (pooled string in heap)
b ─┘
```

💭 Why?
* JVM optimizes memory by reusing identical strings
* String literals go to **string pool**
* Both point to SAME object

👉 `a == b` returns **true**

---

## 🔹 `new String()` → Heap Allocation

```java
String c = new String("hello");
```

```text
c ─────► new "hello" (separate object in heap)
```

💭 Why?
* `new` always creates a **new object**
* Bypasses the string pool
* Different from literal

👉 `a == c` returns **false** (different objects)

👉 `a.equals(c)` returns **true** (same content)

---

## 🧠 Rule

| Syntax | Storage | Behavior |
| --- | --- | --- |
| `String s = "hi"` | String pool | Reused/shared |
| `String s = new String("hi")` | Heap | Always new object |

---

# 🔷 7. ARRAYS (REFERENCE TYPE)

---

## 🔹 Example

```java
int[] arr = new int[3];
```

```text
Stack:           Heap:
arr ─────►       [0, 0, 0]
(address)        (array object)
```

---

## 🔹 Key Points

* **Array itself is an object** → stored in heap
* **Array reference** → stored in stack
* **Elements** → stored inside the array object
* In array of primitives: values stored in heap (inside array)
* In array of objects: references stored in array

---

## 🧠 Example with Objects

```java
Person[] people = new Person[2];
people[0] = new Person();
```

```text
Stack:            Heap:
people ─────►     [ref1, null]
                   ↓
                  [name=...]
```

---

## 🔹 Array Assignment

```java
int[] a = {1, 2};
int[] b = a;
```

💭 Explanation:
* `a` and `b` reference **same array object**
* `b[0] = 99` affects original

👉 Both see the same array

---

# 🔷 8. WRAPPER CLASSES (BOXING/UNBOXING)

---

## 🔹 Difference

```java
int x = 10;       // primitive
Integer y = 10;   // wrapper object
```

| Aspect | Primitive | Wrapper |
| --- | --- | --- |
| Storage | Stack | Heap |
| Type | Value | Object |
| Null | ❌ | ✅ |
| Speed | Fast | Slow |
| Use | Simple values | Collections |

---

## 🔹 Autoboxing (Auto Conversion)

```java
Integer x = 10;  // automatically wrapped
int y = x;       // automatically unwrapped
```

💭 Explanation:
* JVM automatically converts between primitive and wrapper
* `int` → `Integer` when needed
* `Integer` → `int` when needed

---

## 🧠 Interview Implication

* Wrapper adds memory overhead
* Used in collections: `ArrayList<Integer>`
* Equality: `==` checks reference; `.equals()` checks value

---

# 🔷 9. NULL BEHAVIOR

---

## 🔹 Null Assignment

```java
String s = null;
```

💭 Variable `s` doesn't reference any object

---

## 🔹 NullPointerException (NPE)

```java
String s = null;
s.length();  // ❌ NullPointerException
```

💭 Trying to access method on null (no object)

---

## 🧠 Rule

* Only reference types can be null
* Primitives cannot be null
* Accessing null object → runtime error

---

# 🔷 10. TYPE CASTING

---

## 🔹 Primitive Casting

```java
int a = 10;
double b = (double) a;  // 10.0
```

---

## 🔹 Reference Casting

```java
Object obj = new String("hello");
String s = (String) obj;  // cast to String
```

---

## ⚠️ Interview Note

* Casting doesn't change object
* Just tells compiler type for access
* Wrong cast → ClassCastException

---

# 🔷 11. INTERVIEW MENTAL MODEL (STEP-BY-STEP)

---

When analyzing code:

---

## 🧠 Step 1: Identify Type

* Primitive or Reference?

---

## 🧠 Step 2: Identify Storage

* Primitive → Stack
* Reference → Stack (ref) + Heap (object)

---

## 🧠 Step 3: Identify Operation

* Assignment → value copy or reference copy?
* `new` involved?
* String literal or `new String()`?

---

## 🧠 Step 4: Track References

* Which variables point to same object?
* Different objects?

---

## 🧠 Step 5: Predict Output

* Based on memory model

---

# 🔷 12. COMMON INTERVIEW PATTERNS

---

## 🔥 Pattern 1: Primitive Independence

```java
int a = 5;
int b = a;
a = 10;
// a = 10, b = 5 (independent)
```

---

## 🔥 Pattern 2: Reference Sharing

```java
String[] s1 = {"a"};
String[] s2 = s1;
// s1 and s2 reference same array
```

---

## 🔥 Pattern 3: String Pool

```java
String a = "code";
String b = "code";
String c = new String("code");
// a == b (true), a == c (false)
```

---

## 🔥 Pattern 4: Array Mutation

```java
int[] a = {1};
int[] b = a;
b[0] = 99;
// a[0] = 99 (same array affected)
```

---

## 🔥 Pattern 5: Wrapper vs Primitive

```java
Integer a = 10;
Integer b = 10;
// a == b might be true (caching)
// But don't rely on it for large numbers
```

---

# 🔷 13. COMMON MISTAKES (VERY IMPORTANT)

---

### ❌ Mistake 1: "String is primitive"

👉 WRONG
✔️ String is an object (reference type)

---

### ❌ Mistake 2: "Assignment copies object"

👉 WRONG
✔️ Assignment either:
  * Copies value (primitives)
  * Copies reference (objects)

---

### ❌ Mistake 3: "Array is primitive"

👉 WRONG
✔️ Array is an object reference type

---

### ❌ Mistake 4: "All string references are pooled"

👉 WRONG
✔️ Only string literals are pooled
✔️ `new String()` creates separate object

---

### ❌ Mistake 5: "Integer == comparison always works"

👉 WRONG
✔️ `==` compares references
✔️ Use `.equals()` for integer value comparison

---

# 🔷 14. FINAL MENTAL MODEL (CONDENSED)

---

### 🧠 5 Golden Rules (Data Types Edition)

1. **Primitive** → value stored in stack (fast, independent)
2. **Reference** → address in stack, object in heap (shared)
3. **Assignment** → value copy (primitive) OR reference copy (object)
4. **`new`** → always creates new object in heap
5. **String literals** → pooled; `new String()` → separate object

---

# 🎯 LEVEL 1 TARGET

You should be able to:

✅ Identify primitive vs reference instantly
✅ Predict memory behavior
✅ Explain string pool basics
✅ Understand array as reference type
✅ Explain wrapper classes vs primitives
✅ Predict output using memory model

---

**Ready for assignments?** Go to `assignement/test` folder!

**Next Level:** Level 2 = Integer caching, string intern(), array mutation traps, wrapper comparison pitfalls

---

## Level 2

### Mental Model
Type decides representation; representation decides memory behavior. Primitive operations copy bits, reference operations copy addresses.

### Solve Steps
1. Classify each value as primitive or reference.
2. Check boxing/unboxing boundaries.
3. Track String pool and Integer cache scenarios.
4. Predict equality with == (identity/value by type) vs equals (content).

## Level 3

### Mental Model
The JVM memory system is optimized for object lifetime patterns. Correctness depends on reference visibility; performance depends on allocation and GC pressure.

### Solve Steps
1. Estimate allocation frequency in loops and helpers.
2. Identify long-lived vs short-lived objects.
3. Reduce temporary object churn when needed.
4. In concurrent code, reason with visibility and atomicity explicitly.

---

### Level 2 Questions
1. For `int a=10; int b=a; b=20;`, explain memory behavior line-by-line.
2. For `Integer x=127; Integer y=127;` vs `Integer x=128; Integer y=128;`, predict `==` results.
3. Why is `==` unsafe for String value comparison in general?

### Level 3 Questions
1. How do allocation rate and object lifetime influence GC pressure?
2. Why is reducing temporary object churn often more useful than micro-optimizing one line?
3. In concurrent code, which memory questions must be answered before trusting observed output?

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
