# 03 - LinkedList Core

## 1) Internal Idea

`LinkedList` is a doubly linked list.

Each node keeps:

- data
- next pointer
- prev pointer

## 2) Complexity

- `addFirst/addLast/removeFirst/removeLast`: `O(1)`
- `get(index)`: `O(n)`
- `add(index, e)`: `O(n)` (traversal)
- `remove(index)`: `O(n)` (traversal)
- `contains(value)`: `O(n)`

## 3) Extra Capability

`LinkedList` also implements `Deque`, so queue/deque operations are available.

```java
LinkedList<Integer> q = new LinkedList<>();
q.offerLast(10);
q.offerFirst(5);
System.out.println(q.pollFirst()); // 5
```

## 4) When To Use

- frequent insertion/removal near ends
- deque-style operations

## 5) Pitfall

Do not use `LinkedList` for heavy random index access.

## 6) Useful Methods

```java
list.remove("Rajiv");
list.removeFirstOccurrence("A");
list.removeLastOccurrence("A");
list.removeIf(s -> s.length() > 3);
list.addFirst("X");
list.addLast("Y");
```

If using as stack with tail:

- push: `addLast`
- peek: `getLast`
- pop: `removeLast`

## 7) Quick Construction and `removeAll`

```java
LinkedList<String> ls = new LinkedList<>(Arrays.asList("Karan", "Aditya", "Adarsh", "Chirag"));
LinkedList<String> removeLs = new LinkedList<>(Arrays.asList("Aditya", "Adarsh"));
ls.removeAll(removeLs); // [Karan, Chirag]
```

`Arrays.asList(...)` is fixed-size view, but `new LinkedList<>(...)` creates new mutable list.

## 8) In-Place vs New Object

- in-place: `add`, `addFirst`, `addLast`, `remove`, `removeFirst`, `removeLast`, `removeFirstOccurrence`, `removeLastOccurrence`, `removeIf`, `removeAll`, `clear`
- new object: `new LinkedList<>(...)`, `toArray(...)`
