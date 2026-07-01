# 11 - Common Bugs and Best Practices (List)

## 1) Bug: `ConcurrentModificationException`

### Wrong

Concept taught: Demonstrates Wrong in practice.

```java
List<String> list = new ArrayList<>(List.of("A", "", "B"));
for (String s : list) {
    if (s.isBlank()) {
        list.remove(s); // unsafe structural change during enhanced for
    }
}
```

Typical result:

```text
Throws ConcurrentModificationException
```

### Correct options

Concept taught: Demonstrates Correct options in practice.

```java
list.removeIf(String::isBlank);
```

or:

Concept taught: Demonstrates Correct options in practice.

```java
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().isBlank()) it.remove();
}
```

## 2) Bug: `remove(int)` vs `remove(Object)`

Concept taught: Demonstrates 2) Bug: `remove(int)` vs `remove(Object)` in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 2));
nums.remove(2); // index 2, removes value 3
System.out.println(nums);

nums.remove(Integer.valueOf(2)); // removes by value
System.out.println(nums);
```

Expected output:

```text
[1, 2, 2]
[1, 2]
```

## 3) Bug: Wrong Equality Check

Concept taught: Demonstrates 3) Bug: Wrong Equality Check in practice.

```java
String a = new String("java");
String b = new String("java");
System.out.println(a == b);
System.out.println(a.equals(b));
```

Output:

```text
false
true
```

For list lookup/removal of objects, rely on `equals`, not `==`.

## 4) Bug: Missing `equals/hashCode` in Custom Objects

Concept taught: Demonstrates 4) Bug: Missing `equals/hashCode` in Custom Objects in practice.

```java
class User {
    String id;
    User(String id) { this.id = id; }
}

List<User> users = new ArrayList<>(List.of(new User("u1")));
System.out.println(users.contains(new User("u1"))); // false without equals/hashCode
```

Fix: implement `equals` and `hashCode` properly.

## 5) Bug: UnsupportedOperationException from Wrong List Type

Concept taught: Demonstrates 5) Bug: UnsupportedOperationException from Wrong List Type in practice.

```java
List<String> a = List.of("x", "y");
// a.add("z"); // throws UnsupportedOperationException

List<String> b = Arrays.asList("x", "y");
// b.remove(0); // throws UnsupportedOperationException
```

Always know whether your list is mutable, fixed-size, unmodifiable view, or immutable snapshot.

## 6) Bug: IndexOutOfBoundsException

Concept taught: Demonstrates 6) Bug: IndexOutOfBoundsException in practice.

```java
List<Integer> nums = List.of(10, 20);
// nums.get(2); // invalid: valid indexes are 0 and 1
```

Best practice:

- guard with `isEmpty()` for first/last operations
- validate index boundaries in API methods

## 7) Bug: Using `LinkedList` with Index Loop

Concept taught: Demonstrates 7) Bug: Using `LinkedList` with Index Loop in practice.

```java
List<Integer> linked = new LinkedList<>();
for (int i = 0; i < 10000; i++) linked.add(i);

for (int i = 0; i < linked.size(); i++) {
    linked.get(i); // expensive repeated traversal
}
```

Prefer iterator/for-each for linked structures.

## 8) Bug: Exposing Internal Mutable List

Concept taught: Demonstrates 8) Bug: Exposing Internal Mutable List in practice.

```java
class BadOrder {
    private final List<String> items = new ArrayList<>();
    List<String> getItems() { return items; } // unsafe exposure
}
```

Better:

Concept taught: Demonstrates 8) Bug: Exposing Internal Mutable List in practice.

```java
class GoodOrder {
    private final List<String> items = new ArrayList<>();
    List<String> getItems() { return List.copyOf(items); }
}
```

## 9) Bug: Assuming List Thread Safety

`ArrayList` and `LinkedList` are not thread-safe.

If multiple threads write/read same list:

- external synchronization required
- or use specialized concurrent collection

## 10) Best-Practice Checklist

- declare as interface: `List<T> list = new ArrayList<>()`
- avoid raw types
- avoid structural mutation during enhanced for
- use `removeIf` / iterator remove
- document mutability in APIs
- defensive copy at boundaries
- measure performance with realistic workloads
- choose structure by operation profile, not myths

## 11) Debugging Tips

When list logic fails unexpectedly:

1. print list type (`list.getClass().getName()`)
2. print size and sample contents before/after each step
3. verify mutability contract
4. verify `equals/hashCode` on custom objects
5. isolate mutation points in iteration code

## 12) Summary

Most list bugs are contract bugs: wrong mutability assumption, wrong equality semantics, or unsafe iteration-time mutation. Fixing contracts fixes most runtime surprises.
