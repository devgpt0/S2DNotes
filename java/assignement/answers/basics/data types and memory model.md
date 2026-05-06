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

### 🔹 Expected Output

~~~
61
64
~~~

### 🔹  Reasoning

* Primitive assignment copies value
* b changes independently
* a unchanged

🔹 **Primitive copy creates independent values**

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

### 🔹 Expected Output

~~~
65
~~~

### 🔹  Reasoning

* a and b reference same object
* field update mutates shared object
* a observes updated value

🔹 **Reference assignment shares object**

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

### 🔹 Expected Output

~~~
63
66
~~~

### 🔹  Reasoning

* b now points to new object
* a still points to old object
* state diverges

🔹 **Reassignment breaks aliasing**

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

### 🔹 Expected Output

~~~
64
~~~

### 🔹  Reasoning

* Java passes primitives by value
* method changes local copy
* caller value unaffected

🔹 **Primitive args are copied**

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

### 🔹 Expected Output

~~~
68
~~~

### 🔹  Reasoning

* reference value copied
* both refs point same object
* field mutation visible to caller

🔹 **Pass-by-value of reference still mutates object**

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

### 🔹 Expected Output

~~~
66
~~~

### 🔹  Reasoning

* parameter is local reference copy
* rebind affects only local b
* caller reference unchanged

🔹 **Parameter reassignment is local only**

---
## 🔹 ASSIGNMENT 7: String Pool vs equals

### Question

~~~java
String a = "v67";`nString b = new String("v67");`nSystem.out.println(a == b);`nSystem.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---

### 🔹 Expected Output

~~~
false
true
~~~

### 🔹  Reasoning

* new String creates distinct object
* == compares identity
* equals compares content

🔹 **Use equals for String content**

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

### 🔹 Expected Output

~~~
71
~~~

### 🔹  Reasoning

* arrays are objects
* reference copy aliases same array
* element mutation shared

🔹 **Array assignment copies reference**

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

### 🔹 Expected Output

~~~
69
72
~~~

### 🔹  Reasoning

* clone creates new array object
* primitive elements copied by value
* arrays become independent

🔹 **clone separates top-level array state**

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

### 🔹 Expected Output

~~~
x
~~~

### 🔹  Reasoning

* b still references object
* nulling a removes only one reference
* object remains accessible

🔹 **Nulling one variable does not delete object**

---

## Level 2 (Assignments 11-20)

## 🔹 ASSIGNMENT 11

### Question

~~~java
int[][] arr = new int[2][];
arr[0] = new int[]{1};
arr[1] = arr[0];

arr[0][0] = 99;

System.out.println(arr[1][0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
99
~~~

### 🧠 Reasoning

* `arr[1]` and `arr[0]` point to the same inner array.
* Updating `arr[0][0]` changes that shared array.

👉 **2D arrays can share row references**

---
## 🔹 ASSIGNMENT 12

### Question

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

### ✅ Expected Output

~~~
99
1
~~~

### 🧠 Reasoning

* First element stores reference to original `a`.
* Second element stores cloned array `b`.
* Mutation on `a` does not affect `b`.

👉 **`clone()` separates top-level array state**

---
## 🔹 ASSIGNMENT 13

### Question

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

### ✅ Expected Output

~~~
[[99]]
[[99]]
~~~

### 🧠 Reasoning

* `new ArrayList<>(x)` is a shallow copy of outer list.
* Inner list reference is shared in both `x` and `y`.

👉 **Shallow copy duplicates container, not nested objects**

---
## 🔹 ASSIGNMENT 14

### Question

~~~java
import java.util.*;

List<Integer> a = new ArrayList<>(Arrays.asList(1, 2));
List<Integer> b = Collections.unmodifiableList(a);

a.add(3);

System.out.println(b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[1, 2, 3]
~~~

### 🧠 Reasoning

* `unmodifiableList` creates a read-only view, not a copy.
* Backing list `a` is still mutable.

👉 **Unmodifiable view reflects backing-list changes**

---
## 🔹 ASSIGNMENT 15

### Question

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

### ✅ Expected Output

~~~
[1, 2]
~~~

### 🧠 Reasoning

* Method parameter is a copied reference value.
* Rebinding `list` inside method affects only local variable.

👉 **Local reassignment does not change caller reference**

---
## 🔹 ASSIGNMENT 16

### Question

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

### ✅ Expected Output

~~~
[1, 2, 100]
~~~

### 🧠 Reasoning

* Method receives reference to same list object.
* `add` mutates that shared object.

👉 **Object mutation is visible to caller**

---
## 🔹 ASSIGNMENT 17

### Question

~~~java
import java.util.*;

List<Integer> a = Arrays.asList(1, 2, 3);
a.set(0, 99);

System.out.println(a);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
[99, 2, 3]
~~~

### 🧠 Reasoning

* `Arrays.asList` gives fixed-size list.
* `set` is allowed because it does not change size.

👉 **Fixed-size list allows replace, not add/remove**

---
## 🔹 ASSIGNMENT 18

### Question

~~~java
import java.util.*;

List<Integer> a = Arrays.asList(1, 2, 3);
a.add(4);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
Exception in thread "main" java.lang.UnsupportedOperationException
~~~

### 🧠 Reasoning

* `Arrays.asList` returns fixed-size list.
* `add` tries to change size, so runtime throws exception.

👉 **Fixed-size lists reject structural modification**

---
## 🔹 ASSIGNMENT 19

### Question

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

### ✅ Expected Output

~~~
[[1, 2, 99], [1, 2]]
~~~

### 🧠 Reasoning

* First inner list in `outer` is `base` itself.
* Second inner list is an independent copy.
* Mutating `base` affects only first entry.

👉 **Copying inner list breaks later mutation sharing**

---
## 🔹 ASSIGNMENT 20

### Question

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

### ✅ Expected Output

~~~
1
99
~~~

### 🧠 Reasoning

* Initially `b` aliases `a`.
* After `clone`, `b` points to a new array.
* Mutating `b` no longer affects `a`.

👉 **Alias removed after explicit clone + rebinding**

---

## Level 3 (Assignments 21-30)

## 🔹 ASSIGNMENT 21

### Question

~~~java
Integer a = 127;
Integer b = 127;

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
true
~~~

### 🧠 Reasoning

* Autoboxing uses `Integer.valueOf`.
* `127` is inside Integer cache range (`-128` to `127`).

👉 **Cached boxed Integers can share identity**

---
## 🔹 ASSIGNMENT 22

### Question

~~~java
Integer a = 128;
Integer b = 128;

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
false
~~~

### 🧠 Reasoning

* `128` is outside default Integer cache range.
* Two distinct `Integer` objects are typically created.

👉 **Do not use `==` for boxed numeric value comparison**

---
## 🔹 ASSIGNMENT 23

### Question

~~~java
Integer a = 128;
Integer b = 128;

System.out.println(a.equals(b));
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
true
~~~

### 🧠 Reasoning

* `equals` compares numeric value, not identity.

👉 **Use `equals` for wrapper value equality**

---
## 🔹 ASSIGNMENT 24

### Question

~~~java
String a = "ab";
String b = "a" + "b";

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
true
~~~

### 🧠 Reasoning

* Literal concatenation is compile-time constant folding.
* Both references point to same pooled string.

👉 **Compile-time constants are interned in string pool**

---
## 🔹 ASSIGNMENT 25

### Question

~~~java
String a = "ab";
String b = new String("a") + new String("b");

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
false
~~~

### 🧠 Reasoning

* Runtime concatenation with `new String(...)` creates new object.
* It is not automatically the pooled literal reference.

👉 **Runtime-created Strings are usually distinct objects**

---
## 🔹 ASSIGNMENT 26

### Question

~~~java
String a = "ab";
String b = (new String("a") + new String("b")).intern();

System.out.println(a == b);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
true
~~~

### 🧠 Reasoning

* `intern()` returns pooled canonical string reference.
* Literal `"ab"` already points to pooled instance.

👉 **`intern()` aligns runtime String with pool identity**

---
## 🔹 ASSIGNMENT 27

### Question

~~~java
int[] a = {1, 2, 3};

for (int x : a) {
    x = x + 10;
}

System.out.println(a[0]);
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
1
~~~

### 🧠 Reasoning

* Enhanced for-loop variable `x` is a copy of each element value.
* Reassigning `x` does not write back into array.

👉 **For-each variable reassignment does not mutate source array**

---
## 🔹 ASSIGNMENT 28

### Question

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

### ✅ Expected Output

~~~
[1, 2, 3]
~~~

### 🧠 Reasoning

* `x` is local loop variable holding reference/value copy.
* Rebinding `x` does not replace elements in list.

👉 **Reassigning loop variable is not list mutation**

---
## 🔹 ASSIGNMENT 29

### Question

~~~java
import java.util.*;

List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));

for (int i = 0; i < list.size(); i++) {
    list.add(i);
}
~~~

**Predict the output and explain why:**

---

### ✅ Expected Output

~~~
No normal completion: loop keeps growing list until resource failure (typically OutOfMemoryError)
~~~

### 🧠 Reasoning

* `i` increases by 1 each iteration.
* `list.size()` also increases by 1 each iteration due to `add`.
* Condition `i < list.size()` stays true, so loop does not terminate normally.

👉 **Mutating loop bound source can create non-terminating growth**

---
## 🔹 ASSIGNMENT 30

### Question

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

### ✅ Expected Output

~~~
true
false
true
~~~

### 🧠 Reasoning

* `a` and `b` use cached boxed Integer for `100`.
* `new Integer(100)` always creates a new object.
* `equals` compares numeric value.

👉 **Boxed identity and boxed value equality are different checks**

---
