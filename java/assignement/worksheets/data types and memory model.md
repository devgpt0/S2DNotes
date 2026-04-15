# ☕ JAVA ASSIGNMENT - DATA TYPES AND MEMORY MODEL

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

## 🔹 ASSIGNMENT 11: Primitive Value Copy

### Question

~~~java
int a = 71;
int b = a;
b = 74;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 12: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 72;
Box b = a;
b.v = 75;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 13: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 73;
Box b = a;
b = new Box(); b.v = 76;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 14: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 77; }
int a = 74;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 15: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 78; }
Box a = new Box(); a.v = 75;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 16: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 79; }
Box a = new Box(); a.v = 76;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 17: String Pool vs equals

### Question

~~~java
String a = "v77";`nString b = new String("v77");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 18: Array Reference Copy

### Question

~~~java
int[] a = {78, 79};
int[] b = a;
b[0] = 81;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 19: Array Clone

### Question

~~~java
int[] a = {79, 80};
int[] b = a.clone();
b[0] = 82;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 20: Null One Reference

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

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21: Primitive Value Copy

### Question

~~~java
int a = 81;
int b = a;
b = 84;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 22: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 82;
Box b = a;
b.v = 85;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 23: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 83;
Box b = a;
b = new Box(); b.v = 86;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 24: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 87; }
int a = 84;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 25: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 88; }
Box a = new Box(); a.v = 85;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 26: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 89; }
Box a = new Box(); a.v = 86;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 27: String Pool vs equals

### Question

~~~java
String a = "v87";`nString b = new String("v87");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 28: Array Reference Copy

### Question

~~~java
int[] a = {88, 89};
int[] b = a;
b[0] = 91;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 29: Array Clone

### Question

~~~java
int[] a = {89, 90};
int[] b = a.clone();
b[0] = 92;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---
## 🔹 ASSIGNMENT 30: Null One Reference

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