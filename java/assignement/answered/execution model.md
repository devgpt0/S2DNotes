# ☕ JAVA LEVEL 1 — EXECUTION MODEL ASSIGNMENT

**Predict the output and explain the reasoning for each question**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
10
20
```

### 🧠 Reasoning

* `a` stores **value 10** directly in stack
* `b = a` → **copies the value** (not reference)
* Changing `b` to 20 does NOT affect `a` because it's stored separately
* Stack has two independent variables with different values

👉 **Primitive = value copy → independent variables**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
B
B
```

### 🧠 Reasoning

* `new Person()` creates object in **heap**
* `p1` (in stack) → **points to the object**
* `p2 = p1` → **copies the reference** (both point to same object)
* Both `p1` and `p2` refer to **same memory location**
* When `p2.name = "B"` is executed, it modifies the shared object
* Both see the change because they point to the same object

👉 **Object = reference copy → both see mutations**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
A
B
```

### 🧠 Reasoning

* Initially: `p1` and `p2` point to **same object** (name="A")
* `p2 = new Person()` → `p2` now points to **NEW different object**
* `p1` still points to **old object** (name="A")
* Changing new object with `p2.name = "B"` do NOT affect old object
* `p1` and `p2` no longer reference the same memory

👉 **Reassignment = breaks the link → two different objects**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
10
```

### 🧠 Reasoning

* Java is **always pass-by-value** (even for objects)
* When calling `change(a)`, **value 10 is copied**
* Parameter `x` inside function is a **separate variable**
* Changing `x` inside function to 50 does NOT affect `a`
* Function has its own copy on its stack frame

👉 **Function parameter = separate copy → original unchanged**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
Changed
```

### 🧠 Reasoning

* When calling `change(p)`, **reference is copied** (pass-by-value)
* Parameter `p` inside function points to **same object in heap**
* Mutating object via `p.name = "Changed"` changes the shared object
* Original `p` in main still points to same object
* The object itself was changed, not the reference

👉 **Pass-by-value of reference = mutation affects original**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
Original
```

### 🧠 Reasoning

* Parameter `p` inside function is a **separate reference variable** (pass-by-value)
* `p = new Person()` → reassigns **only the parameter** to a new object
* Original `p` in main is **NOT affected** by reassignment
* Original `p` still points to old object with name="Original"
* The parameter's reassignment is local to the function scope

👉 **Critical: Reassignment of parameter ≠ affects original**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
true
```

### 🧠 Reasoning

* String literals are stored in **string pool** (memory optimization)
* JVM reuses the **same reference** for identical literal strings
* `a` and `b` point to **same object** in string pool
* `==` compares references (memory addresses) → true

👉 **String literals = shared references in pool**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
false
true
```

### 🧠 Reasoning

* `a` → string pool reference
* `new String("hello")` → **new object created in heap** (bypasses pool)
* `==` compares references → different objects → **false**
* `.equals()` compares actual string content (value) → same string → **true**

👉 **`new` = always new object | `==` = reference comparison | `.equals()` = value comparison**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
50
50
50
```

### 🧠 Reasoning

* All references (`b1`, `b2`, `b3`) point to **SAME object in heap**
* `b2 = b1` → copies reference
* `b3 = b2` → copies reference (still same object)
* Single object in heap with one field `value`
* When `b3.value = 50` executes, it changes the shared object
* All references see the change because there's only one object

👉 **Multiple references = single object → mutation affects all**

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

**Predict the output and explain why:**

---

### ✅ Expected Output

```
A
```

### 🧠 Reasoning

* `p1 = null` → `p1` no longer points to any object
* `p2` still points to **original object**
* Object remains in heap because `p2` still holds a reference to it
* GC will not collect it yet because there's still an active reference
* Setting one reference to null doesn't affect other references

👉 **Null one reference ≠ delete object | Other references keep it alive**

---

# 🎯 YOUR LEARNING CHECKLIST

After solving all 10 assignments, verify you understand:

- [ ] Primitive variables are independent copies
- [ ] Object variables are references to heap objects
- [ ] Assignment copies values (primitives) or references (objects)
- [ ] Functions always receive copies (pass-by-value)
- [ ] Mutation changes the object, not the reference
- [ ] Reassignment changes what a reference points to
- [ ] String literals share references (pool)
- [ ] `new String()` creates new object (not pooled)
- [ ] Multiple references to same object → mutations affect all
- [ ] Null removes only one reference, object survives if other references exist

---

**If you solved all 10 → Level 1 is complete! 🎉**

**Next: Level 2 = arrays, nested objects, shallow vs deep copy, edge cases**
