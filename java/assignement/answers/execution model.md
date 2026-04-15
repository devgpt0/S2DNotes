# ☕ JAVA ASSIGNMENT - EXECUTION MODEL

## Level 1 (Assignments 1-10)
## 🔹 ASSIGNMENT 1: Primitive Value Copy

### Question

~~~java
int a = 31;
int b = a;
b = 34;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
31
34
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
Box a = new Box(); a.v = 32;
Box b = a;
b.v = 35;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
35
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
Box a = new Box(); a.v = 33;
Box b = a;
b = new Box(); b.v = 36;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
33
36
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
static void f(int x){ x = 37; }
int a = 34;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
34
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
static void f(Box b){ b.v = 38; }
Box a = new Box(); a.v = 35;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
38
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
static void f(Box b){ b = new Box(); b.v = 39; }
Box a = new Box(); a.v = 36;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
36
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
String a = "v37";`nString b = new String("v37");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
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
int[] a = {38, 39};
int[] b = a;
b[0] = 41;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
41
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
int[] a = {39, 40};
int[] b = a.clone();
b[0] = 42;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
39
42
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
int a = 41;
int b = a;
b = 44;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
41
44
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
Box a = new Box(); a.v = 42;
Box b = a;
b.v = 45;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
45
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
Box a = new Box(); a.v = 43;
Box b = a;
b = new Box(); b.v = 46;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
43
46
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
static void f(int x){ x = 47; }
int a = 44;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
44
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
static void f(Box b){ b.v = 48; }
Box a = new Box(); a.v = 45;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
48
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
static void f(Box b){ b = new Box(); b.v = 49; }
Box a = new Box(); a.v = 46;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
46
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
String a = "v47";`nString b = new String("v47");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
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
int[] a = {48, 49};
int[] b = a;
b[0] = 51;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
51
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
int[] a = {49, 50};
int[] b = a.clone();
b[0] = 52;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
49
52
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
int a = 51;
int b = a;
b = 54;
System.out.println(a);
System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
51
54
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
Box a = new Box(); a.v = 52;
Box b = a;
b.v = 55;
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
55
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
Box a = new Box(); a.v = 53;
Box b = a;
b = new Box(); b.v = 56;
System.out.println(a.v);
System.out.println(b.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
53
56
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
static void f(int x){ x = 57; }
int a = 54;
f(a);
System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
54
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
static void f(Box b){ b.v = 58; }
Box a = new Box(); a.v = 55;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
58
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
static void f(Box b){ b = new Box(); b.v = 59; }
Box a = new Box(); a.v = 56;
f(a);
System.out.println(a.v);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
56
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
String a = "v57";`nString b = new String("v57");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
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
int[] a = {58, 59};
int[] b = a;
b[0] = 61;
System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
61
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
int[] a = {59, 60};
int[] b = a.clone();
b[0] = 62;
System.out.println(a[0]);
System.out.println(b[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
59
62
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