# JAVA WEEK 1 TEST

Instructions:
- Write answers only.
- Predict output only.
- Questions are Level 1 and Level 2 only.
- Topics are only from worksheets: Variable Model, Function, Execution Model, Data Types and Memory Model, Control Flow.

Total Questions: 60

---

## Variable Model (10)

### Q1
```java
int a = 10;
int b = a;
a = a + 5;
System.out.println(a + " " + b);
```
Predict output.
Answer: ______________________________

### Q2
```java
class P { int x; }
P p1 = new P();
p1.x = 2;
P p2 = p1;
p2.x = p2.x + 3;
System.out.println(p1.x);
```
Predict output.
Answer: ______________________________

### Q3
```java
class P { int x; }
P p1 = new P();
p1.x = 7;
P p2 = p1;
p1 = new P();
p1.x = 20;
System.out.println(p2.x + " " + p1.x);
```
Predict output.
Answer: ______________________________

### Q4
```java
int[] a = {3, 4};
int[] b = a;
a[1] = 99;
System.out.println(b[1]);
```
Predict output.
Answer: ______________________________

### Q5
```java
int[] a = {5, 6};
int[] b = a.clone();
a[0] = 50;
b[1] = 60;
System.out.println(a[1] + " " + b[0]);
```
Predict output.
Answer: ______________________________

### Q6
```java
String s1 = "dev";
String s2 = s1;
s1 = s1 + "ops";
System.out.println(s1 + " " + s2);
```
Predict output.
Answer: ______________________________

### Q7
```java
class N { String name; }
N n1 = new N();
n1.name = "A";
N n2 = n1;
n1 = null;
System.out.println(n2.name);
```
Predict output.
Answer: ______________________________

### Q8
```java
int x = 8;
{
    int y = x * 2;
    y = 1;
}
System.out.println(x);
```
Predict output.
Answer: ______________________________

### Q9
```java
int[][] m = {{1, 2}, {3, 4}};
int[] r = m[1];
r[0] = 30;
System.out.println(m[1][0]);
```
Predict output.
Answer: ______________________________

### Q10
```java
class B { int v; }
B b1 = new B();
b1.v = 1;
B b2 = b1;
B b3 = b2;
b2.v = b2.v + 9;
System.out.println(b1.v + " " + b3.v);
```
Predict output.
Answer: ______________________________

---

## Function (14)

### Q11
```java
static void addOne(int n) { n = n + 1; }
int a = 4;
addOne(a);
System.out.println(a);
```
Predict output.
Answer: ______________________________

### Q12
```java
class Box { int v; }
static void scale(Box b) { b.v = b.v * 3; }
Box b = new Box();
b.v = 2;
scale(b);
System.out.println(b.v);
```
Predict output.
Answer: ______________________________

### Q13
```java
class Box { int v; }
static void reset(Box b) {
    b = new Box();
    b.v = 100;
}
Box b = new Box();
b.v = 5;
reset(b);
System.out.println(b.v);
```
Predict output.
Answer: ______________________________

### Q14
```java
static int square(int x) { return x * x; }
System.out.println(square(5));
```
Predict output.
Answer: ______________________________

### Q15
```java
static void show(int x) { System.out.println("int"); }
static void show(long x) { System.out.println("long"); }
show(10);
```
Predict output.
Answer: ______________________________

### Q16
```java
static void show(Integer x) { System.out.println("Integer"); }
static void show(Object x) { System.out.println("Object"); }
show(null);
```
Predict output.
Answer: ______________________________

### Q17
```java
static void show(int... x) { System.out.println("varargs"); }
static void show(int x, int y) { System.out.println("two"); }
show(1, 2);
```
Predict output.
Answer: ______________________________

### Q18
```java
static void show(long x) { System.out.println("long"); }
static void show(float x) { System.out.println("float"); }
show(7);
```
Predict output.
Answer: ______________________________

### Q19
```java
static int f() {
    try { return 1; }
    finally { System.out.println("F"); }
}
System.out.println(f());
```
Predict output.
Answer: ______________________________

### Q20
```java
static int f() {
    try { return 2; }
    finally { return 9; }
}
System.out.println(f());
```
Predict output.
Answer: ______________________________

### Q21
```java
static int sum(int... a) {
    int s = 0;
    for (int v : a) s += v;
    return s;
}
System.out.println(sum(1, 2, 3));
System.out.println(sum());
```
Predict output.
Answer: ______________________________

### Q22
```java
static void print(int x) { System.out.println(x); }
int p = 1;
print(++p);
print(p++);
print(p);
```
Predict output.
Answer: ______________________________

### Q23
```java
static void show(int x) { System.out.println("int"); }
static <T> void show(T x) { System.out.println("generic"); }
show(3);
```
Predict output.
Answer: ______________________________

### Q24
```java
class D { int n; }
static void g(D d) {
    d.n = 40;
    d = new D();
    d.n = 90;
}
D d = new D();
d.n = 10;
g(d);
System.out.println(d.n);
```
Predict output.
Answer: ______________________________

---

## Execution Model (8)

### Q25
```java
class X {
    static { System.out.println("S1"); }
    public static void main(String[] args) {
        System.out.println("M");
    }
}
```
Predict output.
Answer: ______________________________

### Q26
```java
class X {
    static int a = init();
    static int init() {
        System.out.println("INIT");
        return 5;
    }
    static { System.out.println("BLOCK"); }
    public static void main(String[] args) {
        System.out.println(a);
    }
}
```
Predict output.
Answer: ______________________________

### Q27
```java
class P {
    static { System.out.println("P"); }
}
class C extends P {
    static { System.out.println("C"); }
    public static void main(String[] args) {
        System.out.println("MAIN");
    }
}
```
Predict output.
Answer: ______________________________

### Q28
```java
class A {
    A() { System.out.println("ctor"); }
    public static void main(String[] args) {
        new A();
        new A();
    }
}
```
Predict output.
Answer: ______________________________

### Q29
```java
class A {
    static int x;
    public static void main(String[] args) {
        System.out.println(x);
    }
}
```
Predict output.
Answer: ______________________________

### Q30
```java
class A {
    int y;
    A() { System.out.println(y); }
    public static void main(String[] args) {
        new A();
    }
}
```
Predict output.
Answer: ______________________________

### Q31
```java
class Z {
    public static void main(String[] args) {
        System.out.println("start");
        int[] a = new int[-1];
        System.out.println("end");
    }
}
```
Predict output.
Answer: ______________________________

### Q32
```java
class T {
    static int x = 1;
    static { x = x + 2; }
    static { x = x * 2; }
    public static void main(String[] args) {
        System.out.println(x);
    }
}
```
Predict output.
Answer: ______________________________

---

## Data Types and Memory Model (14)

### Q33
```java
byte b = 9;
int x = b;
System.out.println(x);
```
Predict output.
Answer: ______________________________

### Q34
```java
double d = 7.9;
int x = (int) d;
System.out.println(x);
```
Predict output.
Answer: ______________________________

### Q35
```java
char c = 'B';
int k = c;
System.out.println(k);
```
Predict output.
Answer: ______________________________

### Q36
```java
Integer a = 10;
int b = a;
System.out.println(a + b);
```
Predict output.
Answer: ______________________________

### Q37
```java
Integer a = null;
System.out.println(a + 1);
```
Predict output.
Answer: ______________________________

### Q38
```java
String a = "ab";
String b = "a" + "b";
System.out.println(a == b);
```
Predict output.
Answer: ______________________________

### Q39
```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);
```
Predict output.
Answer: ______________________________

### Q40
```java
Integer a = 128;
Integer b = 128;
System.out.println(a == b);
```
Predict output.
Answer: ______________________________

### Q41
```java
Integer a = 128;
Integer b = 128;
System.out.println(a.equals(b));
```
Predict output.
Answer: ______________________________

### Q42
```java
String a = "cat";
String b = new String("cat").intern();
System.out.println(a == b);
```
Predict output.
Answer: ______________________________

### Q43
```java
int[] p = {1, 2};
int[] q = p;
q = q.clone();
q[0] = 9;
System.out.println(p[0] + " " + q[0]);
```
Predict output.
Answer: ______________________________

### Q44
```java
import java.util.*;
List<Integer> list = Arrays.asList(1, 2, 3);
list.set(1, 20);
System.out.println(list);
```
Predict output.
Answer: ______________________________

### Q45
```java
import java.util.*;
List<Integer> list = Arrays.asList(1, 2, 3);
list.add(4);
System.out.println(list);
```
Predict output.
Answer: ______________________________

### Q46
```java
int[] arr = {2, 4};
for (int v : arr) {
    v = v + 10;
}
System.out.println(arr[0] + " " + arr[1]);
```
Predict output.
Answer: ______________________________

---

## Control Flow (14)

### Q47
```java
int n = -1;
if (n > 0) {
    System.out.println("P");
} else {
    System.out.println("N");
}
```
Predict output.
Answer: ______________________________

### Q48
```java
int x = 2;
switch (x) {
    case 1:
        System.out.println("A");
    case 2:
        System.out.println("B");
    default:
        System.out.println("C");
}
```
Predict output.
Answer: ______________________________

### Q49
```java
for (int i = 0; i < 3; i++) {
    System.out.print(i + " ");
}
```
Predict output.
Answer: ______________________________

### Q50
```java
int i = 1;
while (i <= 3) {
    System.out.print(i + " ");
    i++;
}
```
Predict output.
Answer: ______________________________

### Q51
```java
int i = 5;
do {
    System.out.print(i + " ");
    i--;
} while (i > 5);
```
Predict output.
Answer: ______________________________

### Q52
```java
for (int i = 1; i <= 6; i++) {
    if (i % 2 == 0) continue;
    if (i == 5) break;
    System.out.print(i + " ");
}
```
Predict output.
Answer: ______________________________

### Q53
```java
int x = 0;
if (x != 0 && 10 / x > 1) {
    System.out.println("T");
} else {
    System.out.println("F");
}
```
Predict output.
Answer: ______________________________

### Q54
```java
int x = 0;
if (x != 0 & 10 / x > 1) {
    System.out.println("T");
} else {
    System.out.println("F");
}
```
Predict output.
Answer: ______________________________

### Q55
```java
outer:
for (int a = 1; a <= 2; a++) {
    for (int b = 1; b <= 3; b++) {
        if (a == 2 && b == 2) break outer;
        System.out.print(a + "" + b + " ");
    }
}
```
Predict output.
Answer: ______________________________

### Q56
```java
for (int i = 0, j = 3; i < 3 && j > 0; i++, j--) {
    System.out.print(i + ":" + j + " ");
}
```
Predict output.
Answer: ______________________________

### Q57
```java
int i = 0;
do {
    i++;
    if (i == 2) continue;
    if (i == 4) break;
    System.out.print(i + " ");
} while (i < 5);
```
Predict output.
Answer: ______________________________

### Q58
```java
int v = 1;
String r = switch (v) {
    case 0 -> "zero";
    case 1 -> "one";
    default -> "other";
};
System.out.println(r);
```
Predict output.
Answer: ______________________________

### Q59
```java
int a = 2, b = 6, c = 4;
int ans = a > b ? a : b > c ? b : c;
System.out.println(ans);
```
Predict output.
Answer: ______________________________

### Q60
```java
int day = 6;
switch (day) {
    case 1, 2, 3, 4, 5 -> System.out.println("Workday");
    case 6, 7 -> System.out.println("Offday");
}
```
Predict output.
Answer: ______________________________

---
End of Test
