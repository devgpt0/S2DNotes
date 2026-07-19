# Java Data Types and Memory - Beginner to Interview Level

A data type tells Java **which values are allowed and which operations are valid**.

Java has primitive types and reference types.

## 1) Primitive Types

| Type | Example | Meaning |
|---|---|---|
| `byte` | `byte level = 10;` | signed 8-bit integer |
| `short` | `short year = 2026;` | signed 16-bit integer |
| `int` | `int count = 100;` | signed 32-bit integer |
| `long` | `long views = 3_000_000_000L;` | signed 64-bit integer |
| `float` | `float ratio = 1.5F;` | 32-bit floating point |
| `double` | `double price = 10.5;` | 64-bit floating point |
| `char` | `char grade = 'A';` | UTF-16 code unit |
| `boolean` | `boolean active = true;` | true or false |

```java
int count = 10;
double average = 2.5;
boolean ready = true;
System.out.println(count + ", " + average + ", " + ready);
// Output: 10, 2.5, true
```

## 2) Reference Types

Classes, interfaces, records, enums, arrays, and strings are reference types.

```java
String name = "Asha";
int[] scores = {80, 90};
List<String> skills = List.of("Java", "SQL");
System.out.println(name);
System.out.println(Arrays.toString(scores));
System.out.println(skills);
// Output:
// Asha
// [80, 90]
// [Java, SQL]
```

A reference can also be `null`, meaning it identifies no object.

## 3) Primitive vs Reference

```java
int primitive = 10;
String reference = "Java";
System.out.println(primitive);
System.out.println(reference.length());
// Output:
// 10
// 4
```

Primitives are values and have no instance methods. A reference lets code access the identified object's behavior.

## 4) Memory Model Without Misleading Shortcuts

- each thread has method-call frames containing execution state and local variables
- objects are normally managed in heap memory
- fields are stored as part of their object/class storage
- a reference's physical representation is a JVM implementation detail
- JIT escape analysis may remove allocations or place data differently

Therefore, “all primitives are on the stack and all objects are on the heap” is not always correct. Focus on value behavior and reachability unless diagnosing a specific JVM.

## 5) Default Values

Fields receive defaults; local variables do not.

```java
final class Defaults {
    int number;
    boolean flag;
    String text;
}
Defaults value = new Defaults();
System.out.println(value.number);
System.out.println(value.flag);
System.out.println(value.text);
// Output:
// 0
// false
// null
```

## 6) Widening and Narrowing

Widening to a larger compatible primitive type is usually automatic. Narrowing requires an explicit cast and may lose information.

```java
int number = 130;
long wider = number;
byte narrower = (byte) number;
System.out.println(wider);
System.out.println(narrower);
// Output:
// 130
// -126
```

The byte value wrapped because 130 is outside byte range.

## 7) Numeric Promotion

Arithmetic on `byte`, `short`, and `char` normally promotes values to `int`.

```java
byte left = 10;
byte right = 20;
int total = left + right;
System.out.println(total);
// Output: 30
```

## 8) Integer Division and Overflow

```java
System.out.println(5 / 2);
System.out.println(5 / 2.0);
System.out.println(Integer.MAX_VALUE + 1);
// Output:
// 2
// 2.5
// -2147483648
```

Use `Math.addExact` when silent overflow is unacceptable.

## 9) Floating-Point Precision

Binary floating-point cannot exactly represent every decimal fraction.

```java
System.out.println(0.1 + 0.2);
System.out.println(new BigDecimal("0.1").add(new BigDecimal("0.2")));
// Output:
// 0.30000000000000004
// 0.3
```

Use integer minor units or `BigDecimal` for exact money calculations. Construct `BigDecimal` from strings or exact integers.

## 10) Wrapper Types and Boxing

Every primitive has a wrapper: `Integer`, `Long`, `Double`, `Boolean`, and so on.

```java
Integer boxed = 10; // boxing
int primitive = boxed; // unboxing
System.out.println(primitive);
// Output: 10
```

Unboxing null throws `NullPointerException`. Collections use reference types, so `List<Integer>` stores wrapper objects rather than primitive `int` values.

## 11) Equality

`==` compares primitive values or reference identity. `equals` normally compares object content according to the class contract.

```java
String first = new String("Java");
String second = new String("Java");
System.out.println(first == second);
System.out.println(first.equals(second));
// Output:
// false
// true
```

## 12) Garbage Collection and Reachability

An object can be collected when it is no longer strongly reachable. Setting one reference to null does not guarantee collection if another reference still reaches the object.

Garbage collection handles memory, not external resources. Close files, sockets, and database connections explicitly.

## Interview Checklist

Know all eight primitives, defaults, widening/narrowing, promotion, overflow, floating-point precision, wrappers/autoboxing, null unboxing, reference equality, object equality, and the difference between language behavior and JVM storage details.
