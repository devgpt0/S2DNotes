# ☕ JAVA LEVEL 1 — VARIABLES MODEL ASSIGNMENT

**Every question tests predict output + explain reasoning**

---

## 🔹 ASSIGNMENT 1: Primitive Assignment (Value Copy)

### Question

```java
public class Main {
    public static void main(String[] args) {
        int a = 10;
        int b = a;
        b = 20;

        System.out.println(a);
        System.out.println(b);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
10
20
```

**Explanation:**
* `a` stores **value 10** directly in stack
* `b = a` → **copies the value** (not reference)
* Changing `b` to 20 does NOT affect `a` because it's stored separately
* Stack has two independent variables

👉 **Primitive = value copy → independent**

---

## 🔹 ASSIGNMENT 2: Reference Assignment (Same Object)

### Question

```java
class Person {
    String name;
}

public class Main {
    public static void main(String[] args) {
        Person p1 = new Person();
        p1.name = "A";

        Person p2 = p1;
        p2.name = "B";

        System.out.println(p1.name);
        System.out.println(p2.name);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
B
B
```

**Explanation:**
* `new Person()` creates object in **heap**
* `p1` (stack) → **points to object**
* `p2 = p1` → **copies the reference** (same object)
* Both `p1` and `p2` refer to **same memory location**
* When `p2.name = "B"` executes, it modifies shared object
* Both see the change

👉 **Object = reference copy → shared object**

---

## 🔹 ASSIGNMENT 3: Reassigning Reference

### Question

```java
class Person {
    String name;
}

public class Main {
    public static void main(String[] args) {
        Person p1 = new Person();
        p1.name = "A";

        Person p2 = p1;
        p2 = new Person();
        p2.name = "B";

        System.out.println(p1.name);
        System.out.println(p2.name);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
A
B
```

**Explanation:**
* Initially: `p1` and `p2` → **same object** (name="A")
* `p2 = new Person()` → `p2` now → **NEW object**
* `p1` still → **old object** (name="A")
* Changing new object does NOT affect old object
* Two different objects now

👉 **Reassignment = breaks link → different objects**

---

## 🔹 ASSIGNMENT 4: Pass Primitive to Function

### Question

```java
public class Main {

    static void change(int x) {
        x = 50;
    }

    public static void main(String[] args) {
        int a = 10;
        change(a);

        System.out.println(a);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
10
```

**Explanation:**
* Java is **always pass-by-value**
* When calling `change(a)`, **value 10 is copied**
* Parameter `x` is **separate variable** in function's stack
* Changing `x` to 50 does NOT affect `a`
* Function has its own copy

👉 **Pass-by-value = original unchanged**

---

## 🔹 ASSIGNMENT 5: Pass Object to Function (Mutation)

### Question

```java
class Person {
    String name;
}

public class Main {

    static void change(Person p) {
        p.name = "Changed";
    }

    public static void main(String[] args) {
        Person p = new Person();
        p.name = "Original";

        change(p);

        System.out.println(p.name);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
Changed
```

**Explanation:**
* When calling `change(p)`, **reference is copied** (pass-by-value)
* Parameter `p` in function → **same object in heap**
* Mutating object via `p.name = "Changed"` → changes shared object
* Original `p` in main still points to same object
* Object was modified, not the reference

👉 **Mutation affects original object**

---

## 🔹 ASSIGNMENT 6: Pass Object + Reassignment

### Question

```java
class Person {
    String name;
}

public class Main {

    static void change(Person p) {
        p = new Person();
        p.name = "New";
    }

    public static void main(String[] args) {
        Person p = new Person();
        p.name = "Original";

        change(p);

        System.out.println(p.name);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
Original
```

**Explanation:**
* Parameter `p` is **separate reference variable** (pass-by-value)
* `p = new Person()` → reassigns **only the parameter**
* Original `p` in main is **NOT affected**
* Original `p` still → old object (name="Original")
* Parameter's reassignment is local to function

👉 **Reassignment of parameter ≠ affects original**

---

## 🔹 ASSIGNMENT 7: String Pool (== vs equals)

### Question

```java
public class Main {
    public static void main(String[] args) {
        String a = "hello";
        String b = "hello";

        System.out.println(a == b);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
true
```

**Explanation:**
* String literals → stored in **string pool**
* JVM reuses **same reference** for identical literals
* `a` and `b` → **same object** in pool
* `==` compares references → **true**

👉 **String literals = shared references**

---

## 🔹 ASSIGNMENT 8: new String() Case

### Question

```java
public class Main {
    public static void main(String[] args) {
        String a = "hello";
        String b = new String("hello");

        System.out.println(a == b);
        System.out.println(a.equals(b));
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
false
true
```

**Explanation:**
* `a` → string pool reference
* `new String("hello")` → **new object in heap** (bypasses pool)
* `==` compares references → different objects → **false**
* `.equals()` compares content (value) → same string → **true**

👉 **`new` = new object | `==` = reference | `.equals()` = value**

---

## 🔹 ASSIGNMENT 9: Multiple References Mutation

### Question

```java
class Box {
    int value;
}

public class Main {
    public static void main(String[] args) {
        Box b1 = new Box();
        b1.value = 10;

        Box b2 = b1;
        Box b3 = b2;

        b3.value = 50;

        System.out.println(b1.value);
        System.out.println(b2.value);
        System.out.println(b3.value);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
50
50
50
```

**Explanation:**
* All references (`b1`, `b2`, `b3`) → **SAME object in heap**
* `b2 = b1` → copies reference
* `b3 = b2` → copies reference (still same object)
* Single object with field `value`
* `b3.value = 50` → changes shared object
* All references see the change

👉 **Multiple references = one object → mutation affects all**

---

## 🔹 ASSIGNMENT 10: Null Reference

### Question

```java
class Person {
    String name;
}

public class Main {
    public static void main(String[] args) {
        Person p1 = new Person();
        p1.name = "A";

        Person p2 = p1;
        p1 = null;

        System.out.println(p2.name);
    }
}
```

**Predict output and explain:**

---

### ✅ Answer

**Output:**
```
A
```

**Explanation:**
* `p1 = null` → `p1` no longer points to object
* `p2` still → **original object**
* Object remains in heap (still has reference from `p2`)
* GC won't collect it (active reference exists)
* Nulling one reference doesn't affect others

👉 **Null one reference ≠ delete object**

---

# 🧠 FINAL MENTAL MODEL (5 GOLDEN RULES)

After completing all 10 assignments, you should instantly know:

1. ✅ **Primitive** → value stored directly in stack
2. ✅ **Object** → reference stored in stack, object in heap
3. ✅ **Assignment** → copies value (primitive) OR reference (object)
4. ✅ **Function** → always pass-by-value
5. ✅ **Mutation ≠ Reassignment** → completely different behaviors

---

# 🎯 ADDITIONAL RULES TO REMEMBER

6. ✅ **== vs equals** → reference vs value comparison
7. ✅ **String literals** → string pool (shared references)
8. ✅ **new String()** → new object (not pooled)
9. ✅ **Multiple references** → single object, mutations affect all
10. ✅ **Null** → removes one reference, object survives if others exist

---

# 📋 SELF-CHECK

After solving all 10, can you:

- [ ] Predict output for primitive copy scenarios
- [ ] Predict output for reference copy scenarios
- [ ] Explain mutation vs reassignment difference
- [ ] Explain why primitive function parameters don't change original
- [ ] Explain why object mutations affect original
- [ ] Explain why object reassignments in functions don't affect original
- [ ] Explain string pool behavior
- [ ] Explain == vs .equals()
- [ ] Predict output for multiple references to same object
- [ ] Explain null reference behavior

---

**If you got 10/10 → Level 1 is MASTERED 🎉**

**Next: Level 2 = arrays, nested objects, shallow vs deep copy, edge cases, tricky combinations**
