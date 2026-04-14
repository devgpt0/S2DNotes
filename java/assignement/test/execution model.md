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
