# LinkedList Notes

## Imports

```java
import java.util.LinkedList;
import java.util.Arrays;
```

`LinkedList` in Java is a doubly linked list implementation of `List` (and also `Deque`).

## Node Concept

A doubly linked list node conceptually stores:
- `value`
- `next` pointer
- `prev` pointer

This is why insertion/deletion near ends or at known node positions is efficient.

## Performance Basics

- Better than `ArrayList` for frequent insert/remove at beginning or middle (when position is already known)
- Slower than `ArrayList` for random index access (`get(i)`)
- Extra memory overhead per element because of node links

Typical complexity:
- `addFirst`, `addLast`, `removeFirst`, `removeLast`: `O(1)`
- `add(index, value)`, `remove(index)`: `O(n)` (needs traversal)
- `get(index)`: `O(n)`
- `contains(value)`: `O(n)`

## Common Methods

```java
LinkedList<String> list = new LinkedList<>();
list.add("Ad");
list.add("Raj");
list.add("Rajiv");
list.add("Rama");
list.add("Ad");
```
- `add(value)`: append at end (`in-place`)
- `add(index, value)`: insert at index (`in-place`)
- `addFirst(value)`: insert at head (`in-place`)
- `addLast(value)`: insert at tail (`in-place`)
- `remove(value)`: remove first matching value (`in-place`)
- `removeFirst()`, `removeLast()`: remove from ends (`in-place`)
- `removeFirstOccurrence(value)`: remove first matching occurrence (`in-place`)
- `removeLastOccurrence(value)`: remove last matching occurrence (`in-place`)
- `removeIf(predicate)`: remove elements matching condition (`in-place`)

Example:

```java
list.remove("Rajiv");
list.addFirst("Adarsh");
list.addLast("AD");
list.removeFirst();
list.removeLast();
list.removeFirstOccurrence("Ad");
list.removeLastOccurrence("Ad");
list.removeIf(s -> s.length() > 3);
```

## Create LinkedList Quickly (Without Multiple add Calls)

```java
LinkedList<String> ls = new LinkedList<>(
    Arrays.asList("Karan", "Aditya", "Adarsh", "Chirag")
);
```

- `Arrays.asList(...)` gives a fixed-size list view.
- Wrapping it with `new LinkedList<>(...)` creates a new mutable `LinkedList`.

## removeAll Example

```java
LinkedList<String> ls = new LinkedList<>(
    Arrays.asList("Karan", "Aditya", "Adarsh", "Chirag")
);

LinkedList<String> removeLs = new LinkedList<>(
    Arrays.asList("Aditya", "Adarsh")
);

ls.removeAll(removeLs); // removes all matching elements from ls
System.out.println(ls); // [Karan, Chirag]
```
## In-Place vs New Object

- In-place (same list changes): `add`, `addFirst`, `addLast`, `remove`, `removeFirst`, `removeLast`, `removeFirstOccurrence`, `removeLastOccurrence`, `removeIf`, `removeAll`, `clear`
- New object creation: `new LinkedList<>(...)`, `toArray(...)`
