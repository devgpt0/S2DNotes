# 14 - Map Practice Problems (Beginner to Expert)

## 1) Beginner Practice

1. Count frequency of each character in a string.
2. Find first non-repeating character.
3. Build `id -> name` map from two arrays.
4. Print entries sorted by key.
5. Merge two maps with overwrite policy.

## 2) Intermediate Practice

1. Group words by anagram.
2. Build inverted index (`value -> list of keys`).
3. Solve two-sum with map.
4. Merge maps by summing common keys.
5. Sort map entries by value descending.
6. Build `category -> totalAmount` from transaction list.

## 3) Advanced Practice

1. Implement fixed-size LRU cache.
2. Top-k frequent elements using map + heap.
3. Sliding-window longest substring with at most K distinct chars.
4. Build thread-safe hit counter per endpoint.
5. Multi-level aggregation (`user -> category -> total`).

## 4) Solved Problem 1: Character Frequency

Concept taught: Basic frequency counting with `merge`.

```java
String s = "aabca";
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) freq.merge(c, 1, Integer::sum);
System.out.println(freq);
```

Possible output:

```text
{a=3, b=1, c=1}
```

## 5) Solved Problem 2: Merge Maps by Sum

Concept taught: Conflict resolution on common keys.

```java
Map<String, Integer> a = new HashMap<>(Map.of("x", 1, "y", 2));
Map<String, Integer> b = Map.of("y", 3, "z", 4);
for (Map.Entry<String, Integer> e : b.entrySet()) {
    a.merge(e.getKey(), e.getValue(), Integer::sum);
}
System.out.println(a);
```

Possible output:

```text
{x=1, y=5, z=4}
```

## 6) Solved Problem 3: Entry Sort by Value Desc

Concept taught: Sorting map entries by value using stream.

```java
Map<String, Integer> m = Map.of("A", 3, "B", 1, "C", 2);
List<Map.Entry<String, Integer>> sorted = m.entrySet().stream()
    .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
    .toList();
System.out.println(sorted);
```

Expected output:

```text
[A=3, C=2, B=1]
```

## 7) Solved Problem 4: Top-K Frequent

Concept taught: Frequency map + min heap for top-k.

```java
int[] nums = {1,1,1,2,2,3,3,3,3,4};
int k = 2;
Map<Integer, Integer> freq = new HashMap<>();
for (int n : nums) freq.merge(n, 1, Integer::sum);

PriorityQueue<Map.Entry<Integer, Integer>> pq =
    new PriorityQueue<>(Map.Entry.comparingByValue());

for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
    pq.offer(e);
    if (pq.size() > k) pq.poll();
}

List<Integer> ans = new ArrayList<>();
while (!pq.isEmpty()) ans.add(pq.poll().getKey());
Collections.reverse(ans);
System.out.println(ans);
```

Expected output:

```text
[3, 1]
```

## 8) Expert Challenge

Given transactions (`userId`, `category`, `amount`, `status`, `timestamp`):

1. filter `SUCCESS`
2. group by user
3. inside user, group by category
4. total amount per category
5. sort users by total spend and return top 3

Do both:

- imperative loops
- streams + collectors

## 9) Interview Drill Advice

For each solved problem, always explain:

- data structure choice
- time complexity
- space complexity
- edge cases

## 10) Summary

Solve these in order and you cover almost all map-style coding interview patterns.
