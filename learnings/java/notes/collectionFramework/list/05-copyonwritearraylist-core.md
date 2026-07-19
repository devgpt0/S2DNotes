# 05 - CopyOnWriteArrayList Core (Complete)

## 1) What It Is

`CopyOnWriteArrayList` is a thread-safe list from `java.util.concurrent`.

Core idea:

- every structural write (`add/remove/set`) creates a fresh array copy
- readers read from stable snapshots without locking contention in most cases

This gives very safe iteration in concurrent read-heavy scenarios.

## 2) Why It Exists

Problem with normal lists:

- `ArrayList` and `LinkedList` are not thread-safe
- concurrent iteration + modification can throw `ConcurrentModificationException`

`CopyOnWriteArrayList` trades expensive writes for very cheap, safe reads.

## 3) Complexity and Cost Model

- `get(index)`: `O(1)`
- iteration: very fast stable snapshot iteration
- `add/remove/set`: `O(n)` due to full-array copy on each write
- memory churn: high for frequent writes (new arrays)

If writes are frequent, this class is usually a bad choice.

## 4) Basic Example with Output

Concept taught: Demonstrates 4) Basic Example with Output in practice.

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("A");
list.add("B");
list.add("C");
System.out.println(list);

list.remove("B");
System.out.println(list);
```

Expected output:

```text
[A, B, C]
[A, C]
```

## 5) Snapshot Iteration Behavior

Concept taught: Demonstrates 5) Snapshot Iteration Behavior in practice.

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>(List.of("one", "two"));

for (String s : list) {
    System.out.println("Seen: " + s);
    if (s.equals("one")) {
        list.add("three");
    }
}

System.out.println("After loop: " + list);
```

Expected output:

```text
Seen: one
Seen: two
After loop: [one, two, three]
```

Explanation:

- iterator sees snapshot taken at iteration start
- new element `three` is not seen during same loop
- no `ConcurrentModificationException`

## 6) Iterator Limitations

`CopyOnWriteArrayList` iterator does not support mutating iterator methods like `remove()`.

Concept taught: Demonstrates 6) Iterator Limitations in practice.

```java
CopyOnWriteArrayList<Integer> list = new CopyOnWriteArrayList<>(List.of(1, 2, 3));
Iterator<Integer> it = list.iterator();
it.next();
// it.remove(); // throws UnsupportedOperationException
```

## 7) Concurrent Example (Reader + Writer)

Concept taught: Demonstrates 7) Concurrent Example (Reader + Writer) in practice.

```java
CopyOnWriteArrayList<String> shared = new CopyOnWriteArrayList<>(List.of("L1", "L2"));

Thread reader = new Thread(() -> {
    for (String s : shared) {
        System.out.println("Reader sees: " + s);
        try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }
});

Thread writer = new Thread(() -> {
    shared.add("L3");
    shared.remove("L1");
    System.out.println("Writer updated: " + shared);
});

reader.start();
writer.start();
```

Possible output (order varies):

```text
Reader sees: L1
Reader sees: L2
Writer updated: [L2, L3]
```

## 8) Useful Specialized Methods

Concept taught: Demonstrates 8) Useful Specialized Methods in practice.

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.addIfAbsent("A");
list.addIfAbsent("A");
list.addAllAbsent(List.of("A", "B", "C"));
System.out.println(list);
```

Expected output:

```text
[A, B, C]
```

Explanation:

- useful when duplicates should be avoided in concurrent registration-style lists

## 9) Java 21+ Sequenced Methods

Because it is a `List`, modern first/last methods are available.

Concept taught: Demonstrates 9) Java 21+ Sequenced Methods in practice.

```java
CopyOnWriteArrayList<Integer> nums = new CopyOnWriteArrayList<>(List.of(2, 3));
nums.addFirst(1);  // still copy-on-write
nums.addLast(4);   // still copy-on-write
System.out.println(nums.getFirst());
System.out.println(nums.getLast());
System.out.println(nums.reversed());
```

Expected output:

```text
1
4
[4, 3, 2, 1]
```

Cost note:

- even `addLast` is `O(n)` here (copy), unlike amortized `O(1)` append behavior in `ArrayList`

## 10) Best Use Cases

Excellent for:

- event listeners
- subscribers/observers
- routing tables read very frequently but changed rarely
- configuration snapshots read by many threads

Bad for:

- queues with continuous high write volume
- frequent random updates

## 11) Common Mistakes

- choosing it as a “default thread-safe list” without workload analysis
- expecting iterator to reflect latest writes instantly
- mutating inside hot write loop (huge allocation pressure)

## 12) Summary

Use `CopyOnWriteArrayList` only when read operations dominate and consistent snapshot iteration is exactly what you need.
