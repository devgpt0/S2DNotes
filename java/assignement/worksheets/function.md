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
````md
# Java Functions — Level 2 (Advanced, Interview-Focused)

## Q1
```java
class Test {
    static void fun(Object o) {
        System.out.println("Object");
    }

    static void fun(String s) {
        System.out.println("String");
    }

    static void fun(Integer i) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
````

**What is the output? Explain most specific method selection.**

---

## Q2

```java
class Test {
    static void fun(int x, long y) {
        System.out.println("int-long");
    }

    static void fun(long x, int y) {
        System.out.println("long-int");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Will this compile? If not, explain ambiguity in overload resolution.**

---

## Q3

```java
class Test {
    static void fun(Integer x) {
        System.out.println("Integer");
    }

    static void fun(long x) {
        System.out.println("long");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why does widening beat boxing (or not)?**

---

## Q4

```java
class Test {
    static void fun(int... x) {
        System.out.println("varargs");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Which method is chosen? Explain boxing vs varargs priority.**

---

## Q5

```java
class Test {
    static void fun(Object... x) {
        System.out.println("Object varargs");
    }

    static void fun(String... x) {
        System.out.println("String varargs");
    }

    public static void main(String[] args) {
        fun("A", "B");
    }
}
```

**Output? Why is one varargs more specific?**

---

## Q6

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(int... x) {
        System.out.println("varargs");
    }

    public static void main(String[] args) {
        fun();
    }
}
```

**Output? Why does this resolve that way?**

---

## Q7

```java
class Test {
    static void fun(int x, int y) {
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

**Which method is called? Why?**

---

## Q8

```java
class Test {
    static int fun() {
        try {
            return 10;
        } finally {
            System.out.println("finally");
        }
    }

    public static void main(String[] args) {
        System.out.println(fun());
    }
}
```

**Output? Does finally override return here? Explain behavior.**

---

## Q9

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Integer... x) {
        System.out.println("Integer varargs");
    }

    public static void main(String[] args) {
        fun(10, 20);
    }
}
```

**Output? Why is fixed arity vs varargs important here?**

---

## Q10

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static <T> void fun(T x) {
        System.out.println("generic");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why does non-generic method win?**

---

## Q11

```java
class Test {
    static <T> void fun(T x) {
        System.out.println("generic");
    }

    static void fun(String x) {
        System.out.println("String");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
```

**Output? Explain method specificity with generics.**

---

## Q12

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        Integer a = null;
        fun(a);
    }
}
```

**Output? Why is null handled this way?**

---

## Q13

```java
class Test {
    static void fun(int x, double y) {
        System.out.println("int-double");
    }

    static void fun(double x, int y) {
        System.out.println("double-int");
    }

    public static void main(String[] args) {
        fun(10, 10.0);
    }
}
```

**Output? Why no ambiguity here?**

---

## Q14

```java
class Test {
    static void fun(byte x) {
        System.out.println("byte");
    }

    static void fun(int x) {
        System.out.println("int");
    }

    public static void main(String[] args) {
        byte b = 10;
        fun(b);
    }
}
```

**Output? Explain exact match vs widening.**

---

## Q15

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(long... x) {
        System.out.println("long varargs");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why fixed arity wins over varargs?**

````md
# Java Functions — Level 2 (Advanced, Interview-Focused)

## Q1
```java
class Test {
    static void fun(Object o) {
        System.out.println("Object");
    }

    static void fun(String s) {
        System.out.println("String");
    }

    static void fun(Integer i) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
````

**What is the output? Explain most specific method selection.**

---

## Q2

```java
class Test {
    static void fun(int x, long y) {
        System.out.println("int-long");
    }

    static void fun(long x, int y) {
        System.out.println("long-int");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Will this compile? If not, explain ambiguity in overload resolution.**

---

## Q3

```java
class Test {
    static void fun(Integer x) {
        System.out.println("Integer");
    }

    static void fun(long x) {
        System.out.println("long");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why does widening beat boxing (or not)?**

---

## Q4

```java
class Test {
    static void fun(int... x) {
        System.out.println("varargs");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Which method is chosen? Explain boxing vs varargs priority.**

---

## Q5

```java
class Test {
    static void fun(Object... x) {
        System.out.println("Object varargs");
    }

    static void fun(String... x) {
        System.out.println("String varargs");
    }

    public static void main(String[] args) {
        fun("A", "B");
    }
}
```

**Output? Why is one varargs more specific?**

---

## Q6

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(int... x) {
        System.out.println("varargs");
    }

    public static void main(String[] args) {
        fun();
    }
}
```

**Output? Why does this resolve that way?**

---

## Q7

```java
class Test {
    static void fun(int x, int y) {
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

**Which method is called? Why?**

---

## Q8

```java
class Test {
    static int fun() {
        try {
            return 10;
        } finally {
            System.out.println("finally");
        }
    }

    public static void main(String[] args) {
        System.out.println(fun());
    }
}
```

**Output? Does finally override return here? Explain behavior.**

---

## Q9

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Integer... x) {
        System.out.println("Integer varargs");
    }

    public static void main(String[] args) {
        fun(10, 20);
    }
}
```

**Output? Why is fixed arity vs varargs important here?**

---

## Q10

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static <T> void fun(T x) {
        System.out.println("generic");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why does non-generic method win?**

---

## Q11

```java
class Test {
    static <T> void fun(T x) {
        System.out.println("generic");
    }

    static void fun(String x) {
        System.out.println("String");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
```

**Output? Explain method specificity with generics.**

---

## Q12

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        Integer a = null;
        fun(a);
    }
}
```

**Output? Why is null handled this way?**

---

## Q13

```java
class Test {
    static void fun(int x, double y) {
        System.out.println("int-double");
    }

    static void fun(double x, int y) {
        System.out.println("double-int");
    }

    public static void main(String[] args) {
        fun(10, 10.0);
    }
}
```

**Output? Why no ambiguity here?**

---

## Q14

```java
class Test {
    static void fun(byte x) {
        System.out.println("byte");
    }

    static void fun(int x) {
        System.out.println("int");
    }

    public static void main(String[] args) {
        byte b = 10;
        fun(b);
    }
}
```

**Output? Explain exact match vs widening.**

---

## Q15

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(long... x) {
        System.out.println("long varargs");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Why fixed arity wins over varargs?**

# Java Functions — Level 3 (Expert, Edge Cases & JVM-Level Reasoning)

## Q1
```java
class Test {
    static void fun(int x, Object... y) {
        System.out.println("A");
    }

    static void fun(int... x) {
        System.out.println("B");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
````

**Which method is selected? Explain varargs + fixed parameter interaction.**

---

## Q2

```java
class Test {
    static void fun(Integer x) {
        System.out.println("Integer");
    }

    static void fun(long x) {
        System.out.println("long");
    }

    static void fun(int... x) {
        System.out.println("varargs");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Output? Explain full overload resolution order (widening vs boxing vs varargs).**

---

## Q3

```java
class Test {
    static void fun(Object o) {
        System.out.println("Object");
    }

    static void fun(Object... o) {
        System.out.println("Object varargs");
    }

    public static void main(String[] args) {
        fun(null);
    }
}
```

**Will this compile? If yes, which method is called? Explain ambiguity rules.**

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

    static void fun(int... x) {
        System.out.println("C");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Which method is selected? Does ambiguity still exist or is it resolved?**

---

## Q5

```java
class Test {
    static <T> void fun(T x, T y) {
        System.out.println("generic");
    }

    static void fun(Object x, String y) {
        System.out.println("Object-String");
    }

    public static void main(String[] args) {
        fun("A", "B");
    }
}
```

**Output? Explain type inference vs overload specificity.**

---

## Q6

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static <T extends Number> void fun(T x) {
        System.out.println("Number generic");
    }

    public static void main(String[] args) {
        fun(10);
    }
}
```

**Which method is chosen? Why does bounded generic lose/win?**

---

## Q7

```java
class Test {
    static void fun(Integer x) {
        System.out.println("Integer");
    }

    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(Object x) {
        System.out.println("Object");
    }

    public static void main(String[] args) {
        Integer a = null;
        fun(a);
    }
}
```

**Output? Explain null + reference hierarchy resolution.**

---

## Q8

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(int... x) {
        System.out.println("varargs");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun();
    }
}
```

**Output? Why are only certain overloads considered?**

---

## Q9

```java
class Test {
    static void fun(long x, float y) {
        System.out.println("long-float");
    }

    static void fun(float x, long y) {
        System.out.println("float-long");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Will this compile? Explain dual widening ambiguity.**

---

## Q10

```java
class Test {
    static void fun(Object o, String s) {
        System.out.println("Object-String");
    }

    static void fun(String s, Object o) {
        System.out.println("String-Object");
    }

    public static void main(String[] args) {
        fun(null, null);
    }
}
```

**Compile or error? Explain most specific method failure.**

---

## Q11

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(long x) {
        System.out.println("long");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        short s = 10;
        fun(s);
    }
}
```

**Output? Explain widening chain priority.**

---

## Q12

```java
class Test {
    static void fun(int x) {
        System.out.println("int");
    }

    static void fun(double x) {
        System.out.println("double");
    }

    static void fun(Integer x) {
        System.out.println("Integer");
    }

    public static void main(String[] args) {
        fun(10.0f);
    }
}
```

**Output? Explain float → double vs boxing path.**

---

## Q13

```java
class Test {
    static <T> void fun(T... x) {
        System.out.println("generic varargs");
    }

    static void fun(String... x) {
        System.out.println("String varargs");
    }

    public static void main(String[] args) {
        fun("A", "B");
    }
}
```

**Output? Why does non-generic varargs win?**

---

## Q14

```java
class Test {
    static void fun(int x, long y) {
        System.out.println("A");
    }

    static void fun(long x, long y) {
        System.out.println("B");
    }

    public static void main(String[] args) {
        fun(10, 10);
    }
}
```

**Output? Explain partial exact match vs full widening.**

---

## Q15

```java
class Test {
    static void fun(int x, Object y) {
        System.out.println("A");
    }

    static void fun(Integer x, Object y) {
        System.out.println("B");
    }

    public static void main(String[] args) {
        fun(10, null);
    }
}
```

**Output? Explain boxing vs exact reference match interaction.**







