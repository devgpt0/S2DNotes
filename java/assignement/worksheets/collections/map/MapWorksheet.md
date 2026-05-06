# Map Worksheet

Source: collectionFramework/map (unified notes)

## Tricky Predict the Output (15)

1.
```java
Map<String, Integer> m = new HashMap<>();
System.out.println(m.put("A", 1));
System.out.println(m.put("A", 5));
System.out.println(m.get("A"));
```
Answer: _____________

2.
```java
Map<String, Integer> m = new HashMap<>();
m.put("x", null);
System.out.println(m.get("x"));
System.out.println(m.containsKey("x"));
```
Answer: _____________

3.
```java
Map<String, Integer> m = new HashMap<>();
m.merge("k", 1, Integer::sum);
m.merge("k", 2, Integer::sum);
System.out.println(m.get("k"));
```
Answer: _____________

4.
```java
Map<String, List<Integer>> m = new HashMap<>();
m.computeIfAbsent("A", k -> new ArrayList<>()).add(10);
m.computeIfAbsent("A", k -> new ArrayList<>()).add(20);
System.out.println(m.get("A"));
```
Answer: _____________

5.
```java
Map<String, Integer> m = new HashMap<>();
m.put("A", 10);
m.computeIfPresent("A", (k, v) -> v + 5);
m.computeIfPresent("B", (k, v) -> 1);
System.out.println(m);
```
Answer: _____________

6.
```java
Map<Integer, String> m = new LinkedHashMap<>();
m.put(2, "B");
m.put(1, "A");
m.put(3, "C");
System.out.println(m);
```
Answer: _____________

7.
```java
Map<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(1);
System.out.println(m);
```
Answer: _____________

8.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.ceilingKey(21));
```
Answer: _____________

9.
```java
Map<String, Integer> m = Map.of("A", 1, "B", 2);
m.put("C", 3);
```
Answer: _____________

10.
```java
Map<String, Integer> m = new ConcurrentHashMap<>();
m.put("A", 1);
m.put(null, 2);
```
Answer: _____________

11.
```java
enum Status { NEW, DONE }
Map<Status, Integer> m = new EnumMap<>(Status.class);
m.put(Status.DONE, 2);
m.put(Status.NEW, 1);
System.out.println(m);
```
Answer: _____________

12.
```java
Map<String, Integer> m = new TreeMap<>();
m.put("b", 2);
m.put("a", 1);
System.out.println(m.firstKey() + ":" + m.lastKey());
```
Answer: _____________

13.
```java
Map<Integer, String> m = new HashMap<>();
m.put(1, "A");
m.put(2, "B");
m.replaceAll((k, v) -> v + k);
System.out.println(m.get(2));
```
Answer: _____________

14.
```java
Map<String, Integer> m = new HashMap<>();
m.put("x", 1);
m.remove("x", 2);
System.out.println(m.containsKey("x"));
```
Answer: _____________

15.
```java
Map<String, Integer> m = new HashMap<>();
m.put("A", 1);
m.put("B", 2);
for (Map.Entry<String, Integer> e : m.entrySet()) {
  if (e.getKey().equals("A")) e.setValue(99);
}
System.out.println(m.get("A"));
```
Answer: _____________

## MCQ Theory (15)

1. `HashMap` average `put/get/remove` complexity:
```text
A) O(log n)
B) O(1)
C) O(n)
D) O(n^2)
```

2. `HashMap` key uniqueness is decided by:
```text
A) hashCode only
B) equals only
C) hash bucket + equals match
D) value compare
```

3. `LinkedHashMap` can maintain:
```text
A) insertion/access order
B) only sorted order
C) random order
D) hash order only
```

4. `TreeMap` is based on:
```text
A) hash table
B) red-black tree
C) array
D) skip list
```

5. `ConcurrentHashMap` null key/value:
```text
A) both allowed
B) key allowed only
C) neither allowed
D) value allowed only
```

6. Best method for counting frequency:
```text
A) containsValue
B) merge
C) clear
D) keySet
```

7. Best method for grouping with list initialization:
```text
A) computeIfAbsent
B) remove
C) getOrDefault only
D) replace
```

8. `Map.of(...)` maps are:
```text
A) mutable
B) thread-local
C) immutable
D) synchronized mutable
```

9. `WeakHashMap` keys are:
```text
A) strong references only
B) weak references
C) soft references only
D) primitive only
```

10. `IdentityHashMap` compares keys using:
```text
A) equals
B) compareTo
C) ==
D) hash only
```

11. `EnumMap` best use case:
```text
A) string keys
B) enum keys
C) object identity keys
D) null-heavy keys
```

12. Correct check when null values are possible:
```text
A) map.get(k) != null
B) map.containsKey(k)
C) map.values().contains(k)
D) map.size() > 0
```

13. `containsValue` is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

14. LRU using map is commonly built on:
```text
A) TreeMap
B) LinkedHashMap with accessOrder
C) Hashtable
D) WeakHashMap
```

15. For both key and value iteration, best practice:
```text
A) values()
B) keySet()
C) entrySet()
D) forEach key only
```

## Interview Questions (10)

1. Explain `HashMap` internals: bucket, collision, resize, threshold.
2. Why must custom key classes override both `equals` and `hashCode`?
3. Compare `HashMap`, `LinkedHashMap`, and `TreeMap` with use cases.
4. Explain `computeIfAbsent`, `computeIfPresent`, and `merge` with examples.
5. Why is `ConcurrentHashMap` preferred over `Hashtable` in modern code?
6. Explain null handling differences across map implementations.
7. How does `LinkedHashMap` enable LRU cache?
8. When would you choose `EnumMap`, `WeakHashMap`, and `IdentityHashMap`?
9. How would you debug a map bug where `containsKey` fails unexpectedly?
10. What tests would you write for a map-heavy component?

