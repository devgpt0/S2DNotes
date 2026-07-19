# Comprehensive Map Worksheet (All Concepts)

**Source**: collectionFramework/map (all notes 01-15)  
**Weightage**: HashMap (35%) | TreeMap (15%) | LinkedHashMap (10%) | ConcurrentHashMap (10%) | Map Operations (15%) | Specialized Maps (10%) | Immutable (5%)

---

## LEVEL 1 - FUNDAMENTALS

### 1.1 Predict the Output (35 Questions)

#### HashMap Basics (12 questions)
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
m.put("a", 1);
m.put("b", 2);
System.out.println(m.size());
```
Answer: _____________

4.
```java
Map<String, Integer> m = new HashMap<>();
m.put("key", 100);
System.out.println(m.remove("key"));
System.out.println(m.containsKey("key"));
```
Answer: _____________

5.
```java
Map<Integer, String> m = new HashMap<>();
m.put(1, "a");
m.put(2, "b");
m.put(1, "c");
System.out.println(m.size());
```
Answer: _____________

6.
```java
Map<String, Integer> m = new HashMap<>();
System.out.println(m.get("nonexistent"));
System.out.println(m.getOrDefault("nonexistent", 99));
```
Answer: _____________

7.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
System.out.println(m.containsKey("a"));
System.out.println(m.containsValue(1));
```
Answer: _____________

8.
```java
Map<String, Integer> m = new HashMap<>();
m.put("x", 1);
m.put("y", 2);
for (String key : m.keySet()) System.out.print(key);
```
Answer: _____________

9.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("b", 2);
for (Integer val : m.values()) System.out.print(val);
```
Answer: _____________

10.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("b", 2);
for (Map.Entry<String, Integer> e : m.entrySet()) 
    System.out.print(e.getKey() + e.getValue());
```
Answer: _____________

11.
```java
Map<String, Integer> m = new HashMap<>();
m.put("java", 1);
m.put("python", 2);
m.clear();
System.out.println(m.isEmpty());
```
Answer: _____________

12.
```java
Map<String, String> m1 = new HashMap<>(Map.of("a", "1"));
Map<String, String> m2 = new HashMap<>(Map.of("b", "2"));
m1.putAll(m2);
System.out.println(m1);
```
Answer: _____________

#### TreeMap (Sorted) (8 questions)
13.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.firstKey());
```
Answer: _____________

14.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.lastKey());
```
Answer: _____________

15.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.ceilingKey(21));
```
Answer: _____________

16.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(10, "A");
tm.put(20, "B");
tm.put(30, "C");
System.out.println(tm.floorKey(25));
```
Answer: _____________

17.
```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("b", 2);
tm.put("a", 1);
tm.put("c", 3);
System.out.println(tm.headMap("b"));
```
Answer: _____________

18.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(10, "A");
tm.put(20, "B");
tm.put(30, "C");
System.out.println(tm.subMap(10, 30));
```
Answer: _____________

19.
```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("c", 3);
tm.put("a", 1);
tm.put("b", 2);
for (String key : tm.keySet()) System.out.print(key);
```
Answer: _____________

20.
```java
TreeMap<Integer, String> tm = new TreeMap<>(Collections.reverseOrder());
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.firstKey());
```
Answer: _____________

#### LinkedHashMap (Insertion Order) (5 questions)
21.
```java
Map<Integer, String> m = new LinkedHashMap<>();
m.put(2, "B");
m.put(1, "A");
m.put(3, "C");
System.out.println(m.keySet());
```
Answer: _____________

22.
```java
Map<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(1); // access-order
System.out.println(m.keySet());
```
Answer: _____________

23.
```java
Map<String, Integer> m = new LinkedHashMap<>();
m.put("x", 1);
m.put("y", 2);
m.put("z", 3);
m.remove("y");
System.out.println(m.keySet());
```
Answer: _____________

24.
```java
LinkedHashMap<String, Integer> lhm = new LinkedHashMap<>();
lhm.put("a", 1);
lhm.put("b", 2);
for (String key : lhm.keySet()) System.out.print(key);
```
Answer: _____________

25.
```java
Map<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.get(1);
m.put(2, "B2"); // update existing
for (Integer key : m.keySet()) System.out.print(key);
```
Answer: _____________

#### ConcurrentHashMap & Thread-Safety (5 questions)
26.
```java
Map<String, Integer> m = new ConcurrentHashMap<>();
m.put("A", 1);
System.out.println(m.put(null, 2));
```
Answer: _____________

27.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("java", 1);
m.putIfAbsent("java", 2);
System.out.println(m.get("java"));
```
Answer: _____________

28.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("x", 1);
System.out.println(m.replace("x", 1, 99));
System.out.println(m.get("x"));
```
Answer: _____________

29.
```java
Map<String, Integer> m = new ConcurrentHashMap<>();
m.put("A", 1);
m.put(null, 2); // throws NPE
```
Answer: _____________

30.
```java
ConcurrentHashMap<String, List<Integer>> m = new ConcurrentHashMap<>();
m.putIfAbsent("key", new ArrayList<>()).add(10);
System.out.println(m.get("key"));
```
Answer: _____________

#### Map Operations (merge, compute, etc) (5 questions)
31.
```java
Map<String, Integer> m = new HashMap<>();
m.merge("k", 1, Integer::sum);
m.merge("k", 2, Integer::sum);
System.out.println(m.get("k"));
```
Answer: _____________

32.
```java
Map<String, List<Integer>> m = new HashMap<>();
m.computeIfAbsent("A", k -> new ArrayList<>()).add(10);
m.computeIfAbsent("A", k -> new ArrayList<>()).add(20);
System.out.println(m.get("A"));
```
Answer: _____________

33.
```java
Map<String, Integer> m = new HashMap<>();
m.put("A", 10);
m.computeIfPresent("A", (k, v) -> v + 5);
m.computeIfPresent("B", (k, v) -> 1);
System.out.println(m);
```
Answer: _____________

34.
```java
Map<String, Integer> m = new HashMap<>();
m.put("x", 1);
m.remove("x", 2);
System.out.println(m.containsKey("x"));
```
Answer: _____________

35.
```java
Map<String, Integer> m = new HashMap<>();
m.put("A", 1);
m.put("B", 2);
m.replaceAll((k, v) -> v + k.length());
System.out.println(m.get("A"));
```
Answer: _____________

---

### 1.2 MCQ Theory (35 Questions)

#### HashMap Concepts (12 questions)
1. `HashMap` average complexity for put/get/remove:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

2. Key uniqueness in HashMap is decided by:
```text
A) hashCode() only
B) equals() only
C) hashCode() + equals() match
D) compareTo()
```

3. HashMap collision handling:
```text
A) linear probing
B) chaining in buckets
C) open addressing
D) rehashing always
```

4. Load factor in HashMap:
```text
A) ratio of entries to capacity
B) determines resize threshold
C) default 0.75
D) all above
```

5. HashMap initial capacity:
```text
A) 10
B) 16
C) 8
D) dynamic
```

6. Worst case HashMap complexity:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2) if poor hash
```

7. Iterating over HashMap with entrySet():
```text
A) most efficient
B) least efficient
C) same as keySet
D) always O(n^2)
```

8. HashMap null key/value:
```text
A) both allowed
B) key allowed, value not
C) key not allowed, value allowed
D) neither allowed
```

9. HashMap thread-safety:
```text
A) inherently thread-safe
B) not thread-safe
C) requires synchronization
D) synchronized at method level
```

10. Resizing HashMap:
```text
A) happens automatically
B) triggered at load factor
C) rehashes all entries
D) all above
```

11. Pre-sizing HashMap:
```text
A) no benefit
B) reduces resizes
C) improves performance
D) both B and C
```

12. Equals contract for HashMap keys:
```text
A) only equals() needed
B) only hashCode() needed
C) both must be consistent
D) neither required
```

#### TreeMap Concepts (8 questions)
13. TreeMap internal structure:
```text
A) hash table
B) red-black tree
C) linked list
D) array
```

14. TreeMap ordering:
```text
A) insertion order
B) natural order of keys
C) access order
D) random
```

15. TreeMap complexity for put/get:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

16. TreeMap supports:
```text
A) firstKey(), lastKey()
B) ceilingKey(), floorKey()
C) headMap(), tailMap()
D) all above
```

17. TreeMap natural ordering requires:
```text
A) Comparator
B) Comparable on keys
C) custom hashCode()
D) equals() override
```

18. TreeMap with custom Comparator:
```text
A) Comparable ignored
B) Comparator used
C) both applied
D) error
```

19. TreeMap subMap behavior:
```text
A) new independent map
B) view backed by original
C) immutable
D) copy
```

20. TreeMap empty on no keys:
```text
A) not allowed
B) throws exception
C) allowed, empty map
D) requires initial key
```

#### LinkedHashMap Concepts (5 questions)
21. LinkedHashMap ordering:
```text
A) always insertion order
B) insertion or access order
C) sorted order
D) random
```

22. LinkedHashMap access-order creation:
```text
A) new LinkedHashMap<>()
B) new LinkedHashMap<>(16, 0.75f, true)
C) setAccessOrder()
D) cannot enable
```

23. LinkedHashMap LRU cache pattern:
```text
A) not suitable
B) can override removeEldestEntry()
C) not efficient
D) only for small maps
```

24. LinkedHashMap vs HashMap iteration:
```text
A) same order
B) LinkedHashMap maintains insertion order
C) same performance
D) HashMap faster always
```

25. LinkedHashMap memory overhead:
```text
A) same as HashMap
B) extra doubly linked list
C) minimal difference
D) unpredictable
```

#### ConcurrentHashMap Concepts (5 questions)
26. ConcurrentHashMap thread-safety:
```text
A) synchronized methods
B) segment/bucket level locking
C) lock-free
D) not thread-safe
```

27. ConcurrentHashMap null restrictions:
```text
A) both key and value allowed
B) neither allowed
C) only value allowed
D) key allowed, value not
```

28. ConcurrentHashMap concurrency level:
```text
A) fixed always
B) tunable at construction
C) based on processors
D) not configurable
```

29. putIfAbsent() behavior:
```text
A) always puts
B) puts only if key absent
C) replaces always
D) throws if absent
```

30. Iterator on ConcurrentHashMap:
```text
A) snapshot at creation
B) reflects concurrent changes
C) throws ConcurrentModificationException
D) blocks updates
```

#### Map Operations (3 questions)
31. `merge()` with remapping function:
```text
A) always replaces
B) combines old and new value
C) ignores new value
D) returns null always
```

32. `computeIfAbsent()` vs `putIfAbsent()`:
```text
A) same behavior
B) compute uses function, put uses value
C) compute more flexible
D) both A and B
```

33. `replaceAll()` with lambda:
```text
A) creates new map
B) modifies entries in-place
C) returns new map
D) cannot use lambda
```

#### Specialized Maps (2 questions)
34. EnumMap use case:
```text
A) any key type
B) enum constants only
C) compact and fast
D) both B and C
```

35. WeakHashMap behavior:
```text
A) keys weakly referenced
B) values removed if keys unreferenced
C) GC can remove entries
D) all above
```

---

### 1.3 Interview Questions (15 Questions)

1. **What is a HashMap? How does it achieve O(1) average time complexity?**

2. **Explain the concept of hashing: hash code, bucket, collision.**

3. **What is the equals-hashCode contract? Why are both needed?**

4. **Explain load factor and resizing in HashMap. What happens at 0.75 threshold?**

5. **When would you use TreeMap instead of HashMap? Explain the trade-off.**

6. **What is LinkedHashMap and how does access-order mode work?**

7. **When is ConcurrentHashMap preferred over Collections.synchronizedMap()? Why?**

8. **Explain Map iteration: why use entrySet() instead of keySet() or values()?**

9. **What does `merge()` do? Show a frequency counting example.**

10. **Explain `computeIfAbsent()` and `computeIfPresent()`. Use cases?**

11. **Design an LRU (Least Recently Used) cache using LinkedHashMap.**

12. **What are null key/value restrictions in different map implementations?**

13. **Explain the difference between ConcurrentHashMap and synchronizing a HashMap.**

14. **How does TreeMap maintain sorted order? What data structure does it use?**

15. **When would you use specialized maps like EnumMap or WeakHashMap?**

---

## LEVEL 2 - ADVANCED

### 2.1 Predict the Output (35 Questions)

#### Complex HashMap Scenarios (8 questions)
1.
```java
Map<String, Integer> m = new HashMap<>();
for (String s : new String[]{"a", "a", "b", "c", "c", "c"}) {
    m.merge(s, 1, Integer::sum);
}
System.out.println(m);
```
Answer: _____________

2.
```java
Map<String, List<String>> m = new HashMap<>();
m.computeIfAbsent("java", k -> new ArrayList<>()).add("good");
m.computeIfAbsent("java", k -> new ArrayList<>()).add("fast");
m.computeIfAbsent("python", k -> new ArrayList<>()).add("readable");
System.out.println(m);
```
Answer: _____________

3.
```java
Map<String, Integer> m = new HashMap<>(Map.of("a", 1, "b", 2));
m.replaceAll((k, v) -> v * 2);
System.out.println(m);
```
Answer: _____________

4.
```java
Map<Integer, String> m = new HashMap<>();
m.put(1, "a");
m.put(2, "b");
String old = m.replace(1, "X");
System.out.println(old + " " + m.get(1));
```
Answer: _____________

5.
```java
Map<String, Integer> m = new HashMap<>();
m.put("x", 1);
m.remove("x", 2);
System.out.println(m.containsKey("x"));
```
Answer: _____________

6.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
System.out.println(m.getOrDefault("b", 99));
System.out.println(m.getOrDefault("a", 99));
```
Answer: _____________

7.
```java
Map<String, Integer> freq = new HashMap<>();
String s = "hello";
for (char c : s.toCharArray()) {
    freq.merge(String.valueOf(c), 1, Integer::sum);
}
System.out.println(freq);
```
Answer: _____________

8.
```java
Map<String, String> m = new HashMap<>();
m.put("name", "John");
m.put("age", "25");
m.forEach((k, v) -> System.out.print(k + "=" + v + " "));
```
Answer: _____________

#### TreeMap Advanced (8 questions)
9.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
tm.put(15, "D");
System.out.println(tm.subMap(10, 25));
```
Answer: _____________

10.
```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("apple", 1);
tm.put("apricot", 2);
tm.put("banana", 3);
System.out.println(tm.headMap("b"));
```
Answer: _____________

11.
```java
TreeMap<Integer, String> tm = new TreeMap<>(Collections.reverseOrder());
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm.firstKey() + " " + tm.lastKey());
```
Answer: _____________

12.
```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("c", 3);
tm.put("a", 1);
tm.put("b", 2);
NavigableMap<String, Integer> view = tm.descendingMap();
System.out.println(view.keySet());
```
Answer: _____________

13.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(10, "A");
tm.put(20, "B");
tm.put(30, "C");
System.out.println(tm.ceilingEntry(15));
```
Answer: _____________

14.
```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("z", 26);
tm.put("a", 1);
tm.put("m", 13);
System.out.println(tm.lowerKey("m"));
```
Answer: _____________

15.
```java
TreeMap<Integer, String> tm = new TreeMap<>();
for (int i = 1; i <= 5; i++) {
    tm.put(i * 10, String.valueOf(i));
}
NavigableMap<Integer, String> sub = tm.subMap(15, false, 35, false);
System.out.println(sub);
```
Answer: _____________

16.
```java
TreeMap<Character, Integer> freq = new TreeMap<>();
String s = "hello";
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}
System.out.println(freq);
```
Answer: _____________

#### LinkedHashMap Advanced (5 questions)
17.
```java
LinkedHashMap<String, Integer> lhm = new LinkedHashMap<>(16, 0.75f, true);
lhm.put("a", 1);
lhm.put("b", 2);
lhm.put("c", 3);
lhm.get("a");
System.out.println(new ArrayList<>(lhm.keySet()));
```
Answer: _____________

18.
```java
class LRUCache extends LinkedHashMap<String, String> {
    protected boolean removeEldestEntry(Map.Entry eldest) {
        return size() > 2;
    }
}
LRUCache cache = new LRUCache();
cache.put("a", "1");
cache.put("b", "2");
cache.put("c", "3");
System.out.println(cache);
```
Answer: _____________

19.
```java
LinkedHashMap<Integer, String> lhm = new LinkedHashMap<>();
lhm.put(3, "C");
lhm.put(1, "A");
lhm.put(2, "B");
lhm.remove(1);
lhm.put(1, "A_new");
System.out.println(new ArrayList<>(lhm.keySet()));
```
Answer: _____________

20.
```java
Map<String, Integer> m = new LinkedHashMap<>(16, 0.75f, true);
m.put("x", 1);
m.put("y", 2);
m.put("z", 3);
m.put("x", 99); // update existing
System.out.println(new ArrayList<>(m.keySet()));
```
Answer: _____________

21.
```java
LinkedHashMap<String, Integer> lhm = new LinkedHashMap<>();
lhm.put("first", 1);
lhm.put("second", 2);
Iterator<String> it = lhm.keySet().iterator();
System.out.println(it.next() + " " + it.next());
```
Answer: _____________

#### ConcurrentHashMap Advanced (5 questions)
22.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("a", 1);
m.putIfAbsent("a", 99);
System.out.println(m.get("a"));
```
Answer: _____________

23.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("a", 1);
boolean replaced = m.replace("a", 1, 99);
System.out.println(replaced + " " + m.get("a"));
```
Answer: _____________

24.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("key", 10);
m.computeIfPresent("key", (k, v) -> v + 5);
System.out.println(m.get("key"));
```
Answer: _____________

25.
```java
ConcurrentHashMap<String, List<Integer>> m = new ConcurrentHashMap<>();
m.putIfAbsent("list", new ArrayList<>());
m.get("list").add(1);
m.get("list").add(2);
System.out.println(m.get("list"));
```
Answer: _____________

26.
```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.put("x", 5);
m.replace("x", 5, 10);
m.replace("y", 1, 2);
System.out.println(m);
```
Answer: _____________

#### Specialized Maps & Collections (4 questions)
27.
```java
enum Color { RED, GREEN, BLUE }
Map<Color, Integer> m = new EnumMap<>(Color.class);
m.put(Color.RED, 1);
m.put(Color.GREEN, 2);
m.put(Color.BLUE, 3);
System.out.println(m);
```
Answer: _____________

28.
```java
Map<String, Integer> m = Map.of("a", 1, "b", 2);
m.put("c", 3);
```
Answer: _____________

29.
```java
Map<String, String> original = new HashMap<>(Map.of("x", "y"));
Map<String, String> immutable = Collections.unmodifiableMap(original);
original.put("z", "w");
System.out.println(immutable);
```
Answer: _____________

30.
```java
Map<String, Integer> m = new HashMap<>(Map.of("a", 1));
Map<String, Integer> copy = Map.copyOf(m);
m.put("b", 2);
System.out.println(copy);
```
Answer: _____________

#### Complex Map Patterns (4 questions)
31.
```java
Map<String, Map<String, Integer>> nested = new HashMap<>();
nested.computeIfAbsent("outer", k -> new HashMap<>())
    .put("inner", 42);
System.out.println(nested);
```
Answer: _____________

32.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("b", 2);
m.entrySet().stream()
    .filter(e -> e.getValue() > 1)
    .forEach(e -> System.out.println(e.getKey()));
```
Answer: _____________

33.
```java
Map<Character, Integer> freq = new HashMap<>();
"Mississippi".chars()
    .forEach(c -> freq.merge((char)c, 1, Integer::sum));
System.out.println(freq.get('s'));
```
Answer: _____________

34.
```java
List<String> words = List.of("apple", "app", "apricot");
Map<Integer, List<String>> grouped = words.stream()
    .collect(Collectors.groupingBy(String::length));
System.out.println(grouped);
```
Answer: _____________

35.
```java
Map<String, String> m = new HashMap<>();
m.put("a", "1");
m.put("b", "2");
m.replaceAll((k, v) -> k + v);
System.out.println(m);
```
Answer: _____________

---

### 2.2 MCQ Advanced (35 Questions)

#### Collision & Hash Strategies (5 questions)
1. Hash collision occurs:
```text
A) when two keys have same hash code
B) when two keys hash to same bucket
C) multiple entries in one bucket
D) all above
```

2. Bucket threshold for tree conversion (Java 8+):
```text
A) when bucket reaches 8
B) when bucket reaches 16
C) never converts
D) implementation dependent
```

3. Performance impact of many collisions:
```text
A) still O(1) average
B) degrades toward O(n)
C) always O(log n)
D) no impact
```

4. Hash function properties needed:
```text
A) distributes keys uniformly
B) deterministic (same key = same hash)
C) efficient to compute
D) all above
```

5. Rehashing on resize:
```text
A) recalculates hash codes
B) redistributes to new buckets
C) may change bucket positions
D) all above
```

#### TreeMap Navigation (6 questions)
6. `ceilingKey()` returns:
```text
A) smallest key >= given
B) smallest key > given
C) largest key <= given
D) largest key < given
```

7. `floorKey()` returns:
```text
A) smallest key >= given
B) smallest key > given
C) largest key <= given
D) largest key < given
```

8. `headMap()` includes:
```text
A) all keys < toKey
B) all keys <= toKey
C) depends on exclusive flag
D) all keys > toKey
```

9. `subMap()` behavior:
```text
A) independent copy
B) view backed by original
C) immutable
D) linked structure
```

10. NavigableMap reverse iteration:
```text
A) not possible
B) use descendingMap()
C) use Collections.reverse()
D) manual reversal needed
```

11. TreeMap with custom Comparator:
```java
new TreeMap<>(Comparator.reverseOrder())
```
This creates:
```text
A) ascending then descending
B) descending order
C) requires implementation
D) error
```

#### LinkedHashMap LRU Pattern (5 questions)
12. LRU cache eviction:
```text
A) manually implemented
B) override removeEldestEntry()
C) automatic after size
D) both B and C
```

13. Access-order LinkedHashMap:
```text
A) changes iteration order
B) on get/put
C) reflects recently accessed
D) all above
```

14. Performance of LinkedHashMap:
```text
A) slower than HashMap
B) extra list overhead
C) similar O(1) operations
D) O(log n)
```

15. LRU capacity limit:
```text
A) automatic always
B) configured in constructor
C) manual via removeEldestEntry()
D) fixed always
```

16. LinkedHashMap deep copy:
```text
A) shares internal list
B) independent copy
C) modifies affect both
D) not possible
```

#### ConcurrentHashMap Fine-Grained Locking (5 questions)
17. ConcurrentHashMap segments:
```text
A) each locked independently
B) faster concurrent updates
C) tradeoff with iteration
D) all above
```

18. ConcurrentHashMap iteration safety:
```text
A) snapshot guarantee
B) no structural guarantee
C) WeaklyConsistent
D) both B and C
```

19. ConcurrentHashMap capacity must be:
```text
A) power of 2
B) any integer
C) > concurrency level
D) any even number
```

20. putIfAbsent atomicity:
```text
A) not atomic
B) atomic operation
C) requires external lock
D) conditional atomic
```

21. Advantage over synchronizedMap():
```text
A) better concurrency
B) allows reads during writes
C) no bucket-level locking
D) both A and B
```

#### Specialized Map Implementations (5 questions)
22. EnumMap benefits:
```text
A) constant time access
B) memory efficient for enums
C) compact representation
D) all above
```

23. WeakHashMap use case:
```text
A) caching with auto cleanup
B) holding weak references
C) keys can be GC'd
D) all above
```

24. IdentityHashMap behavior:
```text
A) uses equals for comparison
B) uses == for key identity
C) different from HashMap
D) both B and C
```

25. Collections.unmodifiableMap():
```text
A) blocks modifications
B) throws exception on change
C) read-only view
D) all above
```

26. Map.of() and Map.copyOf():
```text
A) same behavior
B) copyOf creates new copy
C) both immutable
D) factory methods
```

#### Streaming Map Operations (4 questions)
27. Grouping by with counting:
```java
map.entrySet().stream()
    .collect(Collectors.groupingBy(
        e -> e.getKey(),
        Collectors.counting()))
```
Result type:
```text
A) Map<K, V>
B) Map<K, Long>
C) Map<K, List<V>>
D) List<Map>
```

28. Sorting Map by values:
```text
A) direct sort on map
B) extract to list and sort
C) convert to stream
D) B and C
```

29. Filter and transform stream:
```text
A) filter then map
B) map then filter
C) order doesn't matter
D) both orders
```

30. Terminal operation on Map.entrySet():
```text
A) forEach()
B) toList()
C) collect()
D) all terminal
```

#### Null Handling Differences (3 questions)
31. HashMap null handling:
```text
A) one null key allowed
B) multiple null values ok
C) no null restrictions
D) A and B
```

32. ConcurrentHashMap null behavior:
```text
A) same as HashMap
B) neither key nor value
C) security by design
D) synchronization requirement
```

33. TreeMap null restriction:
```text
A) natural ordering needs comparison
B) NPE on null key
C) by design of Comparable
D) all above
```

#### Complex Patterns (2 questions)
34. Map-reduce pattern:
```text
A) groupBy then reduce
B) flatMap then collect
C) functional transformation
D) all above
```

35. Cached computation pattern:
```text
A) computeIfAbsent best approach
B) manual get-compute-put
C) reduce repeated work
D) A and C
```

---

### 2.2 Advanced Interview Questions (15 Questions)

1. **Explain HashMap's hash collision handling: chaining, tree conversion, and performance implications.**

2. **Design frequency counter for large dataset: HashMap vs TreeMap vs stream.collect(groupingBy). Explain trade-offs.**

3. **Implement LRU cache using LinkedHashMap with access-order and removeEldestEntry() override.**

4. **Why is ConcurrentHashMap preferred for concurrent updates? How does segment-level locking improve performance?**

5. **Explain the null key/value restrictions across HashMap, TreeMap, ConcurrentHashMap. Design scenario for each.**

6. **TreeMap navigation methods: ceilingKey, floorKey, subMap. Provide use cases and show view behavior.**

7. **Design a multi-level map for hierarchical data (Map<K1, Map<K2, V>>). Handle computeIfAbsent safely.**

8. **Compare HashMap iteration (keySet vs entrySet vs values). Explain why entrySet is most efficient.**

9. **Implement merge() pattern for counting, grouping, and aggregation. Show frequency counter and group by examples.**

10. **Explain equals-hashCode contract violation: show what breaks when violated, implications for containsKey().**

11. **Design a case-insensitive HashMap wrapper for String keys. Override hashCode() and equals() properly.**

12. **Show Stream API grouping patterns: groupingBy(), groupingByConcurrent(), with collectors. Partition example.**

13. **Explain the performance tradeoff: HashMap (O(1) average, unordered) vs TreeMap (O(log n), sorted).**

14. **Design a thread-safe counter cache: ConcurrentHashMap with merge() vs atomic fields. When to use each?**

15. **Explain Map.of() immutability: is it unmodifiable? Can backing array be modified? Design defensive copying.**

---

## LEVEL 3 - EXPERT PATTERNS

### Advanced Map Patterns

#### Pattern 1: Frequency Counter
```java
String text = "hello world";
Map<Character, Integer> freq = new HashMap<>();
for (char c : text.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}
// or with streams:
Map<Character, Integer> freq2 = text.chars()
    .boxed()
    .map(c -> (char)c.intValue())
    .collect(Collectors.groupingBy(
        Function.identity(),
        Collectors.summingInt(e -> 1)
    ));
```

#### Pattern 2: Grouping with Multiple Levels
```java
Map<String, Map<String, List<Employee>>> grouped = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.groupingBy(
            Employee::getTeam,
            Collectors.toList()
        )
    ));
```

#### Pattern 3: LRU Cache Implementation
```java
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    
    public LRUCache(int capacity) {
        super(16, 0.75f, true); // access-order
        this.capacity = capacity;
    }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry eldest) {
        return size() > capacity;
    }
}
```

#### Pattern 4: Compute and Store Pattern
```java
Map<String, List<Integer>> groups = new HashMap<>();
items.forEach(item ->
    groups.computeIfAbsent(item.category, k -> new ArrayList<>())
        .add(item.value)
);
```

#### Pattern 5: Merge for Aggregation
```java
Map<String, Integer> totals = new HashMap<>();
transactionMaps.forEach(txMap ->
    txMap.forEach((key, value) ->
        totals.merge(key, value, Integer::sum)
    )
);
```

---

## ANSWERS KEY

### Level 1 Answers
1. null, 1, 5
2. null, true
3. 2
4. 100, false
5. 1
6. null, 99
7. true, true
8. xy or yx (no guaranteed order)
9. 12 or 21 (no guaranteed order)
10. a1b2 or b2a1 (no guaranteed order)
11. true
12. {a=1, b=2}
13. 10
14. 30
15. 30
16. 20
17. {a=1}
18. {10=A, 20=B}
19. abc
20. 30
21. [2, 1, 3]
22. [2, 1, 3] or [3, 2, 1] depending on access pattern
23. [x, z]
24. ab
25. [1, 2]
26. NullPointerException (null key not allowed)
27. 1
28. true, 99
29. NullPointerException
30. [10]
31. 3
32. [10, 20]
33. {A=15}
34. true
35. 2

### Level 2 Answers
1. {a=2, b=1, c=3}
2. {java=[good, fast], python=[readable]}
3. {a=2, b=4}
4. a, X
5. true
6. 99, 1
7. {h=1, e=1, l=2, o=1}
8. (varies, depends on hash function ordering)
9. {10=A, 20=B, 15=D}
10. {apple=1, apricot=2}
11. 30, 10
12. [c, b, a]
13. 20=B
14. a
15. {20=B, 30=C}
16. {e=1, h=1, l=2, o=1}
17. [b, c, a]
18. {b=2, c=3}
19. [3, 1, 2] or [2, 1]
20. [y, z, x]
21. first, second
22. 1
23. true, 99
24. 15
25. [1, 2]
26. {x=10}
27. {RED=1, GREEN=2, BLUE=3}
28. UnsupportedOperationException
29. {x=y, z=w}
30. {a=1}
31. {outer={inner=42}}
32. b
33. 4
34. {3=[app], 5=[apple], 7=[apricot]}
35. {a=a1, b=b2}

---

