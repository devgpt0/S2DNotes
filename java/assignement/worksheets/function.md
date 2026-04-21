````md
# Java Functions — Level 1 (Interview-Focused, Tricky Syntax)

## Q1
```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
````

**What is the output? Why?**

---

## Q2

```java
class Test {
    static void fun(int... x) {
        System.out.println("varargs");
    }

    static void fun(int x, int y) {
        System.out.println("two args");
    }

    public static void main(String[] args) {
        fun(10, 20);
    }
}
```

**Which method is called? Explain resolution priority.**

---

## Q3

```java
class Test {
    static void fun(long x) {
        System.out.println("long");
    }

    static void fun(float x) {
        System.out.println("float");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why does Java choose that method?**

---

## Q4

```java
class Test {
    static void fun(int x, Integer y) {
        System.out.println("A");
    }

    static void fun(Integer x, int y) {
        System.out.println("B");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Will this compile? If not, why?**

---

## Q5

```java
class Test {
    static void fun(int x) {
        System.out.println(x);
    }

    public static void main(String[] args) {
        int a = 5;
        fun(a++);
        fun(++a);
    }
}
```

**Output? Explain evaluation order.**

---

## Q6

```java
class Test {
    static void change(int x) {
        x = 100;
    }

    public static void main(String[] args) {
        int a = 10;
        change(a);
        System.out.println(a);
    }
}
```

**Output? Why doesn't value change?**

---

## Q7

```java
class Test {
    static void change(int[] arr) {
        arr[0] = 100;
    }

    public static void main(String[] args) {
        int[] arr = {10, 20, 30};
        change(arr);
        System.out.println(arr[0]);
    }
}
```

**Output? Why different from previous question?**

---

## Q8

```java
class Test {
    static int fun() {
        try {
            return 1;
        } finally {
            return 2;
        }
    }

    public static void main(String[] args) {
        System.out.println(fun());
    }
}
```

**Output? Why does this happen?**

---

## Q9

```java
class Test {
    static void fun(Object o) {
        System.out.println("Object");
    }

    static void fun(String s) {
        System.out.println("String");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
```

**Output? Why is there no ambiguity?**

---

## Q10

```java
class Test {
    static void fun(int x, int... y) {
        System.out.println("A");
    }

    static void fun(int... x) {
        System.out.println("B");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Which method is called? Explain varargs resolution.**

