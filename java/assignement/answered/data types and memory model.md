# ☕ JAVA LEVEL 1 — DATA TYPES & MEMORY MODEL ASSIGNMENT

**Predict the output and explain the reasoning for each question**

---

## 🔹 ASSIGNMENT 1: Primitive Type Independence

### Question

```java
public class Main {
    public static void main(String[] args) {
        int x = 5;
        int y = x;
        y = 10;

        System.out.println(x);
        System.out.println(y);
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
5
10
```

### 🧠 Reasoning

* `int x = 5` stores value 5 directly in stack
* `int y = x` **copies the value** (not reference) into stack
* Each variable has its own independent copy in stack
* `y = 10` changes only `y`'s value in stack
* `x` remains unchanged because primitives are independent

👉 **Primitive = value copy → each variable has independent copy**

---

## 🔹 ASSIGNMENT 2: Reference Type Sharing

### Question

```java
public class Main {
    public static void main(String[] args) {
        String[] s1 = {"A"};
        String[] s2 = s1;
        s2[0] = "B";

        System.out.println(s1[0]);
        System.out.println(s2[0]);
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

* `new String[1]` creates array object in **heap**
* `s1` (in stack) stores **reference (address)** to the array
* `s2 = s1` **copies the reference** (same address)
* Both `s1` and `s2` point to **same array object in heap**
* `s2[0] = "B"` modifies the shared array
* Both see the change because they reference same object

👉 **Reference = address copy → both point to same object**

---

## 🔹 ASSIGNMENT 3: String Pool (Literals)

### Question

```java
public class Main {
    public static void main(String[] args) {
        String a = "hello";
        String b = "hello";
        String c = new String("hello");

        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a.equals(c));
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
true
false
true
```

### 🧠 Reasoning

* `String a = "hello"` → literal stored in **string pool**
* `String b = "hello"` → same literal, JVM reuses **pooled object**
* `String c = new String("hello")` → `new` always creates **new object in heap** (bypasses pool)

* `a == b` → same object? **true** (both in pool)
* `a == c` → same object? **false** (different memory locations)
* `a.equals(c)` → same value? **true** (content is identical)

👉 **String literals are pooled and reused; `new String()` creates separate object**

---

## 🔹 ASSIGNMENT 4: Array as Object

### Question

```java
public class Main {
    public static void main(String[] args) {
        int[] arr1 = {1, 2};
        int[] arr2 = arr1;
        arr2[0] = 99;

        System.out.println(arr1[0]);
        System.out.println(arr2[0]);
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
99
99
```

### 🧠 Reasoning

* `new int[2]` creates array object in **heap**
* `arr1` stores **reference** to array in stack
* `arr2 = arr1` **copies the reference** (same address)
* Both variables point to **same array object**
* `arr2[0] = 99` modifies the shared array
* `arr1[0]` sees the change because it references same array

👉 **Array is reference type: assignment shares the array object**

---

## 🔹 ASSIGNMENT 5: Primitive vs Reference in Array

### Question

```java
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = {1, 2, 3};

        System.out.println(a == b);
        System.out.println(a[0] == b[0]);
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

* `new int[3]` creates array object in heap
* `a` and `b` reference **different array objects** (separate `new` calls)
* Array elements are **primitives** (int values)

* `a == b` → same array object? **false** (different arrays)
* `a[0] == b[0]` → same int value? **true** (both contain 1)

👉 **Arrays are references; elements inside are primitives**

---

## 🔹 ASSIGNMENT 6: Wrapper Class Behavior

### Question

```java
public class Main {
    public static void main(String[] args) {
        Integer p = 10;
        Integer q = 10;

        System.out.println(p == q);
        System.out.println(p.equals(q));
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
true
true
```

### 🧠 Reasoning

* `Integer` is wrapper class (object type) → stored in heap
* `p` and `q` are autoboxed to Integer objects
* **JVM caches integers -128 to 127** (optimization)
* Both `10` references are the **same cached object**
* `p == q` → same object? **true** (due to caching)
* `p.equals(q)` → same value? **true** (content equals)

⚠️ **Note**: This works for small numbers due to caching. For larger numbers (e.g., 1000), `==` returns false

👉 **Wrapper classes use caching for small integers**

---

## 🔹 ASSIGNMENT 7: Autoboxing/Unboxing

### Question

```java
public class Main {
    public static void main(String[] args) {
        Integer x = 5;  // autoboxing
        int y = x;      // unboxing
        y = 10;

        System.out.println(x);
        System.out.println(y);
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
5
10
```

### 🧠 Reasoning

* `Integer x = 5` → JVM automatically wraps `5` in Integer object (autoboxing)
* `int y = x` → JVM automatically unwraps object to primitive (unboxing)
* `y = 10` changes only the primitive variable
* Once unboxed, `y` is **independent** from `x`
* `x` still references object with value 5

👉 **Once unboxed, primitive becomes independent**

---

## 🔹 ASSIGNMENT 8: Null Behavior

### Question

```java
public class Main {
    public static void main(String[] args) {
        String s = null;
        String t = "test";

        System.out.println(s == null);
        System.out.println(t == null);
        // Uncomment below to see NPE: System.out.println(s.length());
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
true
false
```

### 🧠 Reasoning

* `String s = null` → variable doesn't reference any object
* `String t = "test"` → variable references a String object

* `s == null` → is s null? **true** (no object)
* `t == null` → is t null? **false** (references an object)
* `s.length()` would throw **NullPointerException** (can't call method on null)

👉 **Only reference types can be null; primitives cannot**

---

## 🔹 ASSIGNMENT 9: Type Casting

### Question

```java
public class Main {
    public static void main(String[] args) {
        int a = 10;
        double b = a;
        double c = 10.5;
        int d = (int) c;

        System.out.println(b);
        System.out.println(d);
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
10.0
10
```

### 🧠 Reasoning

* `int a = 10` → primitive int value
* `double b = a` → **widening conversion** (int → double automatically)
* `b` becomes 10.0 (int value displayed as double)

* `double c = 10.5` → double value
* `int d = (int) c` → **narrowing conversion** (explicit cast)
* Cast truncates decimal part (10.5 → 10)
* `d` is 10

👉 **Widening is automatic; narrowing requires explicit cast and loses precision**

---

## 🔹 ASSIGNMENT 10: String Literal vs new String()

### Question

```java
public class Main {
    public static void main(String[] args) {
        String s1 = "code";
        String s2 = "code";
        String s3 = new String("code");
        String s4 = new String("code");

        System.out.println(s1 == s2);
        System.out.println(s1 == s3);
        System.out.println(s3 == s4);
        System.out.println(s1.equals(s3));
    }
}
```

**Predict the output and explain why:**

---

### ✅ Expected Output

```
true
false
false
true
```

### 🧠 Reasoning

* `String s1 = "code"` → literal in **string pool** (heap)
* `String s2 = "code"` → same literal, **pooled** (reused)
* `String s3 = new String("code")` → **new object in heap** (bypasses pool)
* `String s4 = new String("code")` → **another new object in heap**

* `s1 == s2` → same pool object? **true**
* `s1 == s3` → literal vs new object? **false** (different locations)
* `s3 == s4` → two separate new objects? **false** (different objects)
* `s1.equals(s3)` → same string content? **true**

👉 **Literals are pooled and shared; `new` always creates separate objects**

---

# 🎯 YOUR LEARNING CHECKLIST

After solving all 10 assignments, verify you understand:

- [ ] Primitive types store values directly in stack
- [ ] Reference types store addresses in stack, objects in heap
- [ ] Primitive assignment copies values (independent)
- [ ] Reference assignment copies addresses (shared objects)
- [ ] Arrays are reference types (objects in heap)
- [ ] String literals are pooled and reused
- [ ] `new String()` creates separate heap objects
- [ ] `==` compares references/values; `.equals()` compares content
- [ ] Wrapper classes use caching for small numbers
- [ ] Autoboxing/Unboxing happens automatically but creates distinction

---

**If you solved all 10 → Level 1 is complete! 🎉**

**Next: Level 2 = Integer caching pitfalls, string intern(), array mutation traps, wrapper comparison edge cases**
