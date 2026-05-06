# ☕ JAVA ASSIGNMENT - VARIABLES MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Primitive Value Copy

### Question

~~~java
int a = 1;
int b = a;
b = 4;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
1
4
~~~

### 🧠 Reasoning

* Primitive assignment copies value
* b changes independently
* a unchanged

👉 **Primitive copy creates independent values**

---
## 🔹 ASSIGNMENT 2: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 2;
Box b = a;
b.v = 5;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
5
~~~

### 🧠 Reasoning

* a and b reference same object
* field update mutates shared object
* a observes updated value

👉 **Reference assignment shares object**

---
## 🔹 ASSIGNMENT 3: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 3;
Box b = a;
b = new Box(); b.v = 6;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
3
6
~~~

### 🧠 Reasoning

* b now points to new object
* a still points to old object
* state diverges

👉 **Reassignment breaks aliasing**

---
## 🔹 ASSIGNMENT 4: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 7; }
int a = 4;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
4
~~~

### 🧠 Reasoning

* Java passes primitives by value
* method changes local copy
* caller value unaffected

👉 **Primitive args are copied**

---
## 🔹 ASSIGNMENT 5: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 8; }
Box a = new Box(); a.v = 5;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
8
~~~

### 🧠 Reasoning

* reference value copied
* both refs point same object
* field mutation visible to caller

👉 **Pass-by-value of reference still mutates object**

---
## 🔹 ASSIGNMENT 6: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 9; }
Box a = new Box(); a.v = 6;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
6
~~~

### 🧠 Reasoning

* parameter is local reference copy
* rebind affects only local b
* caller reference unchanged

👉 **Parameter reassignment is local only**

---
## 🔹 ASSIGNMENT 7: String Pool vs equals

### Question

~~~java
String a = "v7";`nString b = new String("v7");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
false
true
~~~

### 🧠 Reasoning

* new String creates distinct object
* == compares identity
* equals compares content

👉 **Use equals for String content**

---
## 🔹 ASSIGNMENT 8: Array Reference Copy

### Question

~~~java
int[] a = {8, 9};
int[] b = a;
b[0] = 11;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
11
~~~

### 🧠 Reasoning

* arrays are objects
* reference copy aliases same array
* element mutation shared

👉 **Array assignment copies reference**

---
## 🔹 ASSIGNMENT 9: Array Clone

### Question

~~~java
int[] a = {9, 10};
int[] b = a.clone();
b[0] = 12;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
9
12
~~~

### 🧠 Reasoning

* clone creates new array object
* primitive elements copied by value
* arrays become independent

👉 **clone separates top-level array state**

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

### ✅ Expected Output

~~~
x
~~~

### 🧠 Reasoning

* b still references object
* nulling a removes only one reference
* object remains accessible

👉 **Nulling one variable does not delete object**

---

## Level 2 (Assignments 11-20)

## 🔹 ASSIGNMENT 11: Primitive Value Copy

### Question

~~~java
int a = 11;
int b = a;
b = 14;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
11
14
~~~

### 🧠 Reasoning

* Primitive assignment copies value
* b changes independently
* a unchanged

👉 **Primitive copy creates independent values**

---
## 🔹 ASSIGNMENT 12: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 12;
Box b = a;
b.v = 15;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
15
~~~

### 🧠 Reasoning

* a and b reference same object
* field update mutates shared object
* a observes updated value

👉 **Reference assignment shares object**

---
## 🔹 ASSIGNMENT 13: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 13;
Box b = a;
b = new Box(); b.v = 16;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
13
16
~~~

### 🧠 Reasoning

* b now points to new object
* a still points to old object
* state diverges

👉 **Reassignment breaks aliasing**

---
## 🔹 ASSIGNMENT 14: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 17; }
int a = 14;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
14
~~~

### 🧠 Reasoning

* Java passes primitives by value
* method changes local copy
* caller value unaffected

👉 **Primitive args are copied**

---
## 🔹 ASSIGNMENT 15: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 18; }
Box a = new Box(); a.v = 15;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
18
~~~

### 🧠 Reasoning

* reference value copied
* both refs point same object
* field mutation visible to caller

👉 **Pass-by-value of reference still mutates object**

---
## 🔹 ASSIGNMENT 16: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 19; }
Box a = new Box(); a.v = 16;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
16
~~~

### 🧠 Reasoning

* parameter is local reference copy
* rebind affects only local b
* caller reference unchanged

👉 **Parameter reassignment is local only**

---
## 🔹 ASSIGNMENT 17: String Pool vs equals

### Question

~~~java
String a = "v17";`nString b = new String("v17");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
false
true
~~~

### 🧠 Reasoning

* new String creates distinct object
* == compares identity
* equals compares content

👉 **Use equals for String content**

---
## 🔹 ASSIGNMENT 18: Array Reference Copy

### Question

~~~java
int[] a = {18, 19};
int[] b = a;
b[0] = 21;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
21
~~~

### 🧠 Reasoning

* arrays are objects
* reference copy aliases same array
* element mutation shared

👉 **Array assignment copies reference**

---
## 🔹 ASSIGNMENT 19: Array Clone

### Question

~~~java
int[] a = {19, 20};
int[] b = a.clone();
b[0] = 22;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
19
22
~~~

### 🧠 Reasoning

* clone creates new array object
* primitive elements copied by value
* arrays become independent

👉 **clone separates top-level array state**

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

### ✅ Expected Output

~~~
x
~~~

### 🧠 Reasoning

* b still references object
* nulling a removes only one reference
* object remains accessible

👉 **Nulling one variable does not delete object**

---

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21: Primitive Value Copy

### Question

~~~java
int a = 21;
int b = a;
b = 24;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
21
24
~~~

### 🧠 Reasoning

* Primitive assignment copies value
* b changes independently
* a unchanged

👉 **Primitive copy creates independent values**

---
## 🔹 ASSIGNMENT 22: Reference Assignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 22;
Box b = a;
b.v = 25;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
25
~~~

### 🧠 Reasoning

* a and b reference same object
* field update mutates shared object
* a observes updated value

👉 **Reference assignment shares object**

---
## 🔹 ASSIGNMENT 23: Reference Reassignment

### Question

~~~java
class Box { int v; }
Box a = new Box(); a.v = 23;
Box b = a;
b = new Box(); b.v = 26;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
23
26
~~~

### 🧠 Reasoning

* b now points to new object
* a still points to old object
* state diverges

👉 **Reassignment breaks aliasing**

---
## 🔹 ASSIGNMENT 24: Method Primitive Param

### Question

~~~java
static void f(int x){ x = 27; }
int a = 24;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
24
~~~

### 🧠 Reasoning

* Java passes primitives by value
* method changes local copy
* caller value unaffected

👉 **Primitive args are copied**

---
## 🔹 ASSIGNMENT 25: Method Object Mutation

### Question

~~~java
class Box { int v; }
static void f(Box b){ b.v = 28; }
Box a = new Box(); a.v = 25;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
28
~~~

### 🧠 Reasoning

* reference value copied
* both refs point same object
* field mutation visible to caller

👉 **Pass-by-value of reference still mutates object**

---
## 🔹 ASSIGNMENT 26: Method Object Rebinding

### Question

~~~java
class Box { int v; }
static void f(Box b){ b = new Box(); b.v = 29; }
Box a = new Box(); a.v = 26;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
26
~~~

### 🧠 Reasoning

* parameter is local reference copy
* rebind affects only local b
* caller reference unchanged

👉 **Parameter reassignment is local only**

---
## 🔹 ASSIGNMENT 27: String Pool vs equals

### Question

~~~java
String a = "v27";`nString b = new String("v27");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
false
true
~~~

### 🧠 Reasoning

* new String creates distinct object
* == compares identity
* equals compares content

👉 **Use equals for String content**

---
## 🔹 ASSIGNMENT 28: Array Reference Copy

### Question

~~~java
int[] a = {28, 29};
int[] b = a;
b[0] = 31;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
31
~~~

### 🧠 Reasoning

* arrays are objects
* reference copy aliases same array
* element mutation shared

👉 **Array assignment copies reference**

---
## 🔹 ASSIGNMENT 29: Array Clone

### Question

~~~java
int[] a = {29, 30};
int[] b = a.clone();
b[0] = 32;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
29
32
~~~

### 🧠 Reasoning

* clone creates new array object
* primitive elements copied by value
* arrays become independent

👉 **clone separates top-level array state**

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

### ✅ Expected Output

~~~
x
~~~

### 🧠 Reasoning

* b still references object
* nulling a removes only one reference
* object remains accessible

👉 **Nulling one variable does not delete object**

---