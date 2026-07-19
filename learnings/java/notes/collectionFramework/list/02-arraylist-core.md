# 02 - ArrayList Core (Complete)

## 1) Internal Model

`ArrayList` is backed by a resizable array.

Internally:

- maintains `size` (logical element count)
- maintains internal array capacity (physical storage)
- grows array when full (copy to larger array)

This is why indexed reads are fast and middle inserts/removes are expensive.

## 2) Time Complexity (Practical)

- `get(index)`: `O(1)`
- `set(index, e)`: `O(1)`
- `add(e)` end: `O(1)` amortized
- `add(index, e)`: `O(n)` due to shifting
- `remove(index)`: `O(n)` due to shifting
- `remove(value)`: `O(n)` search + shift
- `contains/indexOf`: `O(n)`
- iteration: `O(n)`

## 3) Capacity vs Size

Concept taught: Demonstrates 3) Capacity vs Size in practice.

```java
ArrayList<Integer> list = new ArrayList<>(2);
System.out.println(list.size());
list.add(10);
list.add(20);
System.out.println(list.size());
list.ensureCapacity(100);
list.trimToSize();
```

Expected output:

```text
0
2
```

Explanation:

- `size` is visible element count
- capacity is internal and not directly printed in `ArrayList`
- `ensureCapacity` helps when you know large upcoming inserts
- `trimToSize` can release extra buffer after growth-heavy phases

## 4) Essential Methods with Output

Concept taught: Demonstrates 4) Essential Methods with Output in practice.

```java
List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
list.add(1, "X");
System.out.println(list);

System.out.println(list.get(2));
list.set(0, "AA");
System.out.println(list);

list.remove("X");
System.out.println(list);
```

Expected output:

```text
[A, X, B]
B
[AA, X, B]
[AA, B]
```

## 5) Java 21+ Sequenced Methods on `ArrayList`

Concept taught: Demonstrates 5) Java 21+ Sequenced Methods on `ArrayList` in practice.

```java
ArrayList<Integer> nums = new ArrayList<>(List.of(20, 30));
nums.addFirst(10);   // shifts right
nums.addLast(40);    // append
System.out.println(nums.getFirst());
System.out.println(nums.getLast());
System.out.println(nums);

nums.removeFirst();
nums.removeLast();
System.out.println(nums);
```

Expected output:

```text
10
40
[10, 20, 30, 40]
[20, 30]
```

Complexity note:

- `addFirst/removeFirst`: `O(n)` (shift)
- `addLast/removeLast`: append/remove tail (`addLast` amortized)

## 6) `remove` Overload Trap

Concept taught: Demonstrates 6) `remove` Overload Trap in practice.

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 2));
list.remove(2); // remove index 2 (value 3)
System.out.println(list);

list.remove(Integer.valueOf(2)); // remove first occurrence of value 2
System.out.println(list);
```

Expected output:

```text
[1, 2, 2]
[1, 2]
```

## 7) Iteration Choices for `ArrayList`

### Index loop (fast enough + index available)

Concept taught: Demonstrates Index loop (fast enough + index available) in practice.

```java
List<String> list = List.of("a", "b", "c");
for (int i = 0; i < list.size(); i++) {
    System.out.println(i + " -> " + list.get(i));
}
```

Output:

```text
0 -> a
1 -> b
2 -> c
```

### Enhanced for

Concept taught: Demonstrates Enhanced for in practice.

```java
for (String s : list) {
    System.out.println(s);
}
```

## 8) `subList` Is a View (Important)

Concept taught: Demonstrates 8) `subList` Is a View (Important) in practice.

```java
List<String> base = new ArrayList<>(List.of("A", "B", "C", "D"));
List<String> view = base.subList(1, 3); // [B, C]
view.set(0, "BB");
System.out.println(base);
System.out.println(view);
```

Expected output:

```text
[A, BB, C, D]
[BB, C]
```

Explanation:

- `subList` is backed by parent list
- structural changes in parent outside view rules can invalidate operations and may throw `ConcurrentModificationException`

## 9) ArrayList + Streams

Concept taught: Demonstrates 9) ArrayList + Streams in practice.

```java
List<String> names = new ArrayList<>(List.of("  ram", "shyam", "ram", ""));
List<String> clean = names.stream()
    .map(String::trim)
    .filter(s -> !s.isEmpty())
    .distinct()
    .sorted()
    .toList();

System.out.println(clean);
System.out.println(names);
```

Expected output:

```text
[ram, shyam]
[  ram, shyam, ram, ]
```

Explanation:

- stream pipeline produced a new result list
- source `names` remains unchanged

## 10) `Arrays.asList`, `List.of`, `List.copyOf`

Concept taught: Demonstrates 10) `Arrays.asList`, `List.of`, `List.copyOf` in practice.

```java
List<String> fixed = Arrays.asList("x", "y");
fixed.set(0, "X");
System.out.println(fixed);

List<String> immutable = List.of("a", "b");
System.out.println(immutable);

List<String> copy = List.copyOf(fixed);
System.out.println(copy);
```

Expected output:

```text
[X, y]
[a, b]
[X, y]
```

Rules:

- `Arrays.asList`: fixed-size view
- `List.of`: immutable, rejects `null`
- `List.copyOf`: immutable snapshot copy

## 11) When `ArrayList` Is Best

Use it when:

- you need frequent indexed reads
- you mostly append at end
- memory efficiency matters more than frequent middle insertion

Avoid it when:

- heavy insert/remove at front is required
- lock-free concurrent writes are needed

## 12) Mini Real Example

Concept taught: Demonstrates 12) Mini Real Example in practice.

```java
List<Integer> scores = new ArrayList<>();
scores.addAll(List.of(72, 88, 91, 88, 67));

scores.removeIf(s -> s < 70);
scores.sort(Comparator.reverseOrder());

System.out.println(scores);
System.out.println("Top score: " + scores.getFirst());
```

Expected output:

```text
[91, 88, 88, 72]
Top score: 91
```

## 13) Summary

`ArrayList` is the default list in most Java codebases because it offers the best balance of speed, memory, and simplicity for typical workloads.
