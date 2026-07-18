# Java Variables - Easy Mental Model

A variable is a **named place used by code to hold one value**.

That value is either:

- a primitive value, such as `10` or `true`
- a reference that identifies an object, such as a `Person` or `List`

## 1) Declare and Initialize

```java
int age = 20;
String name = "Asha";
System.out.println(name + " is " + age);
// Output: Asha is 20
```

- declaration: `int age`
- initialization: giving its first value, `= 20`
- assignment: replacing its current value later

## 2) Primitive Variable

```java
int first = 10;
int second = first;
second = 99;
System.out.println(first);
System.out.println(second);
// Output:
// 10
// 99
```

`second` received a copy of the integer value. Changing the copy did not change `first`.

## 3) Reference Variable

```java
List<String> first = new ArrayList<>();
List<String> second = first;
second.add("Java");
System.out.println(first);
// Output: [Java]
```

Both variables contain copied references that identify the same list object. Mutation through either reference is visible through the other.

Do not describe a Java reference as a raw address. The JVM controls its representation.

## 4) Mutation vs Reassignment

Mutation changes an existing object. Reassignment makes a variable hold a different value/reference.

```java
List<String> names = new ArrayList<>(List.of("Asha"));
names.add("Ravi");                 // mutates the existing list
names = new ArrayList<>(List.of("Anu")); // reassigns the variable
System.out.println(names);
// Output: [Anu]
```

## 5) Local Variables and Fields

A local variable is declared inside a method/block and must be assigned before use.

A field belongs to an object or class and receives a default value.

```java
final class Settings {
    int retries;       // default 0
    boolean enabled;   // default false
}
Settings settings = new Settings();
System.out.println(settings.retries + ", " + settings.enabled);
// Output: 0, false
```

## 6) Scope

Scope is the region where a variable name is available.

```java
int outer = 10;
if (outer > 0) {
    int inner = 20;
    System.out.println(outer + inner);
}
// Output: 30
// inner is not available after the if block.
```

Prefer the smallest useful scope.

## 7) `final` Variables

A final variable can be assigned once.

```java
final List<String> names = new ArrayList<>();
names.add("Java");
System.out.println(names);
// Output: [Java]
// The reference cannot be reassigned, but the ArrayList remains mutable.
```

Use an immutable object or defensive copy when the object itself must not change.

## 8) `static` Variables

A static field belongs to the class and is shared by its instances.

```java
final class Counter {
    static int created;
    Counter() { created++; }
}
new Counter();
new Counter();
System.out.println(Counter.created);
// Output: 2
```

Shared mutable static fields need synchronization and often make tests dependent on execution order. Avoid them unless the shared lifecycle is intentional.

## 9) Naming

- use `camelCase`: `orderTotal`
- choose names that state meaning: `retryCount`, not `x`
- use `UPPER_SNAKE_CASE` for constants: `MAX_RETRIES`
- avoid names that repeat the type without describing the role

## Interview Checklist

Explain value copy, reference copy, shared-object mutation, reassignment, local vs field defaults, scope, final references, static fields, and Java pass-by-value.
