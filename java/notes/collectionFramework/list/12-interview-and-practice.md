# 12 - Interview and Practice (List Mastery)

## 1) High-Frequency Interview Questions (With Crisp Answers)

### Q1. `ArrayList` vs `LinkedList`?

- `ArrayList`: dynamic array, fast random access, slower middle insert/remove
- `LinkedList`: node-based, good end operations, slow random index access

### Q2. Why does `CopyOnWriteArrayList` exist?

- to provide thread-safe, snapshot-based iteration in read-heavy concurrent scenarios
- writes are expensive (`O(n)` copy each time)

### Q3. Difference: `List.of`, `Arrays.asList`, `new ArrayList<>(...)`?

- `List.of`: immutable
- `Arrays.asList`: fixed-size view
- `new ArrayList<>(...)`: mutable independent copy

### Q4. Why can `remove(2)` be dangerous in `List<Integer>`?

- because it removes by index, not by value
- use `remove(Integer.valueOf(2))` for value removal

### Q5. What causes `ConcurrentModificationException`?

- structural modification outside iterator contract during fail-fast iteration

### Q6. Is `Vector` fully thread-safe for all use?

- per-method synchronized, but multi-step compound actions are still not atomic

### Q7. Binary search precondition?

- list must be sorted with same ordering/comparator used in search

### Q8. `Comparable` vs `Comparator`?

- comparable: natural order in class
- comparator: external/custom order(s)

### Q9. Why choose `ArrayDeque` over `Stack`?

- modern API, better design, avoids legacy `Vector` inheritance

### Q10. How to safely expose internal list from class?

- return immutable snapshot (`List.copyOf(internal)`) or unmodifiable view depending on contract

## 2) Coding Practice Set (Must Solve)

1. Remove duplicates while preserving first occurrence order.
2. Rotate list right by `k`.
3. Merge two sorted lists into sorted output.
4. Group strings by length.
5. Sort employees by salary desc then name asc.
6. Find first non-repeating element from list.
7. Chunk list into size `n` blocks.
8. Top-k frequent numbers.
9. Partition positives and negatives preserving relative order.
10. Sliding-window max sum of size `k`.

## 3) Solved Practice 1: Remove Duplicates Preserving Order

Concept taught: Demonstrates 3) Solved Practice 1: Remove Duplicates Preserving Order in practice.

```java
List<Integer> nums = List.of(4, 2, 4, 3, 2, 1, 1);
List<Integer> unique = new ArrayList<>(new LinkedHashSet<>(nums));
System.out.println(unique);
```

Expected output:

```text
[4, 2, 3, 1]
```

## 4) Solved Practice 2: Rotate Right by `k`

Concept taught: Demonstrates 4) Solved Practice 2: Rotate Right by `k` in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5));
int k = 2;
Collections.rotate(nums, k);
System.out.println(nums);
```

Expected output:

```text
[4, 5, 1, 2, 3]
```

## 5) Solved Practice 3: Group Strings by Length

Concept taught: Demonstrates 5) Solved Practice 3: Group Strings by Length in practice.

```java
List<String> words = List.of("a", "to", "tea", "java", "go");
Map<Integer, List<String>> grouped = words.stream()
    .collect(Collectors.groupingBy(String::length));
System.out.println(grouped);
```

Possible output:

```text
{1=[a], 2=[to, go], 3=[tea], 4=[java]}
```

## 6) Solved Practice 4: Top-K Frequent Elements

Concept taught: Demonstrates 6) Solved Practice 4: Top-K Frequent Elements in practice.

```java
List<Integer> nums = List.of(1, 1, 1, 2, 2, 3, 3, 3, 3, 4);
int k = 2;

Map<Integer, Long> freq = nums.stream()
    .collect(Collectors.groupingBy(n -> n, Collectors.counting()));

List<Integer> top = freq.entrySet().stream()
    .sorted(Map.Entry.<Integer, Long>comparingByValue().reversed())
    .limit(k)
    .map(Map.Entry::getKey)
    .toList();

System.out.println(top);
```

Expected output:

```text
[3, 1]
```

## 7) Solved Practice 5: Merge Two Sorted Lists

Concept taught: Demonstrates 7) Solved Practice 5: Merge Two Sorted Lists in practice.

```java
List<Integer> a = List.of(1, 3, 5, 7);
List<Integer> b = List.of(2, 4, 6, 8);
List<Integer> out = new ArrayList<>();

int i = 0, j = 0;
while (i < a.size() && j < b.size()) {
    if (a.get(i) <= b.get(j)) out.add(a.get(i++));
    else out.add(b.get(j++));
}
while (i < a.size()) out.add(a.get(i++));
while (j < b.size()) out.add(b.get(j++));

System.out.println(out);
```

Expected output:

```text
[1, 2, 3, 4, 5, 6, 7, 8]
```

## 8) Advanced Scenario Challenge

Given `List<Transaction(userId, amount, status, timestamp)>`:

1. keep `SUCCESS` only
2. aggregate total amount per user
3. sort users by total desc
4. return top 5 users

Do this both ways:

- loop-based imperative
- stream-based declarative

## 9) Interview Drill Checklist

Before interview, rehearse aloud:

- complexity of common list operations
- mutability contracts (`List.of`, `Arrays.asList`, `copyOf`)
- fail-fast iteration explanation
- comparator chaining and binary search rules
- why default choice is `ArrayList`

## 10) Summary

If you can solve the practice set and explain each answer with complexity + API contract, you are interview-ready for most list questions.
