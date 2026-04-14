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

## 🔹 ASSIGNMENT 8: Null Behavior

### Question

```java
public class Main {
    public static void main(String[] args) {
        String s = null;
        String t = "test";

        System.out.println(s == null);
        System.out.println(t == null);
        // Uncommment below to see NPE: System.out.println(s.length());
    }
}
```

**Predict the output and explain why:**

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
