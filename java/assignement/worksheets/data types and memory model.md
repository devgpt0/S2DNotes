# 🔹 JAVA ASSIGNMENT - DATA TYPES AND MEMORY MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Primitive Value Copy

### Question

~~~java
int a = 61;
int b = a;
b = 64;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 2: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 62;
Box b = a;
b.v = 65;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 3: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 63;
Box b = a;
b = new Box(); b.v = 66;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 4: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 67; }
int a = 64;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 5: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 68; }
Box a = new Box(); a.v = 65;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 6: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 69; }
Box a = new Box(); a.v = 66;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 7: String Pool vs equals

### Question

~~~java
String a = "v67";`nString b = new String("v67");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 8: Array Reference Copy

### Question

~~~java
int[] a = {68, 69};
int[] b = a;
b[0] = 71;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 9: Array Clone

### Question

~~~java
int[] a = {69, 70};
int[] b = a.clone();
b[0] = 72;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 10: Null One Reference

### Question

~~~java
class P { String n; }
P a = new P(); a.n = 'x';
P b = a;
a = null;
System.out.println(b.n);
~~~

**Predict the output and explain why:**

---

## Level 2 (Assignments 11-20)

## 🔹 ASSIGNMENT 11

~~~java
int[][] arr = new int[2][];
arr[0] = new int[]{1};
arr[1] = arr[0];

arr[0][0] = 99;

System.out.println(arr[1][0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 12

~~~java
import java.util.*;

List<int[]> list = new ArrayList<>();
int[] a = {1};
list.add(a);

int[] b = a.clone();
list.add(b);

a[0] = 99;

System.out.println(list.get(0)[0]);
System.out.println(list.get(1)[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 13

~~~java
import java.util.*;

List<List<Integer>> x = new ArrayList<>();
x.add(new ArrayList<>(Arrays.asList(1)));

List<List<Integer>> y = new ArrayList<>(x);

y.get(0).set(0, 99);

System.out.println(x);
System.out.println(y);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 14

~~~java
import java.util.*;

List<Integer> a = new ArrayList<>(Arrays.asList(1, 2));
List<Integer> b = Collections.unmodifiableList(a);

a.add(3);

System.out.println(b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 15

~~~java
void f(List<Integer> list) {
    list = new ArrayList<>(list);
    list.add(100);
}

List<Integer> l = new ArrayList<>(Arrays.asList(1, 2));
f(l);

System.out.println(l);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 16

~~~java
void f(List<Integer> list) {
    list.add(100);
}

List<Integer> l = new ArrayList<>(Arrays.asList(1, 2));
f(l);

System.out.println(l);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 17

~~~java
import java.util.*;

List<Integer> a = Arrays.asList(1, 2, 3);
a.set(0, 99);

System.out.println(a);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 18

~~~java
import java.util.*;

List<Integer> a = Arrays.asList(1, 2, 3);
a.add(4);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 19

~~~java
import java.util.*;

List<Integer> base = new ArrayList<>(Arrays.asList(1, 2));
List<List<Integer>> outer = new ArrayList<>();
outer.add(base);

List<Integer> copy = new ArrayList<>(base);
outer.add(copy);

base.add(99);

System.out.println(outer);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 20

~~~java
int[] a = {1, 2};
int[] b = a;

b = b.clone();
b[0] = 99;

System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21

~~~java
Integer a = 127;
Integer b = 127;

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 22

~~~java
Integer a = 128;
Integer b = 128;

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 23

~~~java
Integer a = 128;
Integer b = 128;

System.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 24

~~~java
String a = "ab";
String b = "a" + "b";

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 25

~~~java
String a = "ab";
String b = new String("a") + new String("b");

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 26

~~~java
String a = "ab";
String b = (new String("a") + new String("b")).intern();

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 27

~~~java
int[] a = {1, 2, 3};

for (int x : a) {
    x = x + 10;
}

System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 28

~~~java
import java.util.*;

List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));

for (Integer x : list) {
    x = x + 10;
}

System.out.println(list);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 29

~~~java
import java.util.*;

List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));

for (int i = 0; i < list.size(); i++) {
    list.add(i);
}
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 30

~~~java
Integer a = 100;
Integer b = 100;
Integer c = new Integer(100);

System.out.println(a == b);
System.out.println(a == c);
System.out.println(a.equals(c));
~~~

**Predict the output and explain why:**

---
