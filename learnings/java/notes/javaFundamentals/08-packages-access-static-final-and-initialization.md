# 08 - Packages, Access, Static, Final, and Initialization

## Access Modifiers

| Modifier | Same class | Same package | Subclass in another package | Other code |
|---|---:|---:|---:|---:|
| `private` | yes | no | no | no |
| package-private | yes | yes | no | no |
| `protected` | yes | yes | through inheritance | no |
| `public` | yes | yes | yes | yes |

Top-level types may be public or package-private.

## `static`

Static members belong to the class, not an instance.

```java
final class Sequence {
    private static int next;
    static int next() { return ++next; }
}
System.out.println(Sequence.next());
System.out.println(Sequence.next());
// Output:
// 1
// 2
```

Shared mutable static state needs a thread-safety policy and usually harms test isolation.

## `final`

- final variable: assigned once
- final method: cannot be overridden
- final class: cannot be extended
- final reference: cannot point to another object, but the referenced object may remain mutable

```java
final List<String> names = new ArrayList<>();
names.add("Asha");
System.out.println(names);
// Output: [Asha]
// names cannot be reassigned, but the ArrayList can be mutated.
```

## Initialization Order

```java
class Parent {
    static { System.out.println("parent static"); }
    { System.out.println("parent instance"); }
    Parent() { System.out.println("parent constructor"); }
}
class Child extends Parent {
    static { System.out.println("child static"); }
    { System.out.println("child instance"); }
    Child() { System.out.println("child constructor"); }
}
new Child();
// Output:
// parent static
// child static
// parent instance
// parent constructor
// child instance
// child constructor
```

Static initialization occurs once per class loader before first active use. Instance initialization runs parent-first for every object.

## Packages

Packages organize namespaces and access boundaries. Directory layout should match package names. Avoid the default package in production code.
