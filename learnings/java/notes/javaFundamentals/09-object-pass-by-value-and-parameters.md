# 09 - Object, Pass-by-Value, and Parameters

## Java Is Always Pass-by-Value

For an object variable, the copied value is a reference. A method can mutate the referenced object but cannot replace the caller's variable.

```java
static void change(List<String> values) {
    values.add("mutated");
    values = new ArrayList<>(List.of("reassigned"));
}

List<String> names = new ArrayList<>(List.of("original"));
change(names);
System.out.println(names);
// Output: [original, mutated]
```

## Primitive Parameter

```java
static void increment(int value) { value++; }
int count = 10;
increment(count);
System.out.println(count);
// Output: 10
```

## The `Object` Contract

Frequently asked methods:

- `equals`: logical equality
- `hashCode`: hash-based collection contract
- `toString`: diagnostic representation
- `getClass`: runtime class
- `wait`, `notify`, `notifyAll`: monitor coordination
- `clone`: protected and generally avoided
- `finalize`: deprecated for removal and never appropriate for resource cleanup

```java
record UserId(long value) {}
UserId first = new UserId(7);
UserId second = new UserId(7);
System.out.println(first.equals(second));
System.out.println(first.hashCode() == second.hashCode());
// Output:
// true
// true
```

## Overloading Resolution

Overloading is selected at compile time from declared argument types. Overriding is selected at runtime from the object's actual type.

```java
class Parent { String name() { return "parent"; } }
class Child extends Parent { @Override String name() { return "child"; } }
Parent value = new Child();
System.out.println(value.name());
// Output: child
```

## Parameter Design

Reject invalid arguments immediately. Prefer domain types over long lists of primitives, and never use output parameters by mutating an arbitrary holder when a return value is clearer.
