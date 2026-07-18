# Collection Framework - Common Code Snippets and Solved Questions

## 1) Word Frequency While Preserving First-Seen Order

```java
List<String> words = List.of("java", "sql", "java", "spring");
Map<String, Integer> frequency = new LinkedHashMap<>();
for (String word : words) {
    frequency.merge(word, 1, Integer::sum);
}
System.out.println(frequency);
// Output: {java=2, sql=1, spring=1}
```

Complexity: O(n) average time and O(k) space for k distinct words.

## 2) First Non-Repeated Character

```java
static Optional<Character> firstUnique(String value) {
    Map<Character, Integer> counts = new LinkedHashMap<>();
    for (char character : value.toCharArray()) {
        counts.merge(character, 1, Integer::sum);
    }
    return counts.entrySet().stream()
            .filter(entry -> entry.getValue() == 1)
            .map(Map.Entry::getKey)
            .findFirst();
}

System.out.println(firstUnique("swiss").orElseThrow());
// Output: w
```

Clarify whether full Unicode code points and case normalization are required.

## 3) Remove Duplicates While Preserving Order

```java
List<Integer> values = List.of(3, 1, 3, 2, 1);
List<Integer> unique = new ArrayList<>(new LinkedHashSet<>(values));
System.out.println(unique);
// Output: [3, 1, 2]
```

## 4) Find Intersection of Two Lists

```java
Set<Integer> right = new HashSet<>(List.of(2, 3, 4));
Set<Integer> intersection = new LinkedHashSet<>();
for (int value : List.of(1, 2, 2, 3)) {
    if (right.contains(value)) intersection.add(value);
}
System.out.println(intersection);
// Output: [2, 3]
```

The result uses set semantics. Ask whether duplicate counts should be preserved.

## 5) Sort Objects by Multiple Fields

```java
record Employee(String department, String name, int salary) {}
List<Employee> employees = new ArrayList<>(List.of(
        new Employee("IT", "Ravi", 100),
        new Employee("IT", "Asha", 100),
        new Employee("HR", "Anu", 90)));
employees.sort(Comparator.comparing(Employee::department)
        .thenComparing(Comparator.comparingInt(Employee::salary).reversed())
        .thenComparing(Employee::name));
System.out.println(employees);
// Output: [Employee[department=HR, name=Anu, salary=90], Employee[department=IT, name=Asha, salary=100], Employee[department=IT, name=Ravi, salary=100]]
```

## 6) Top K Values with a Heap

```java
static List<Integer> topK(List<Integer> values, int k) {
    if (k < 0) throw new IllegalArgumentException("k must be non-negative");
    PriorityQueue<Integer> heap = new PriorityQueue<>(k + 1);
    for (int value : values) {
        heap.offer(value);
        if (heap.size() > k) heap.poll();
    }
    List<Integer> result = new ArrayList<>(heap);
    result.sort(Comparator.reverseOrder());
    return result;
}

System.out.println(topK(List.of(5, 1, 9, 3, 8), 3));
// Output: [9, 8, 5]
```

Complexity: O(n log k) time and O(k) space.

## 7) Small LRU Cache

```java
final class LruCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    LruCache(int capacity) {
        super(capacity, 0.75f, true);
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be positive");
        this.capacity = capacity;
    }
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}

Map<Integer, String> cache = new LruCache<>(2);
cache.put(1, "A"); cache.put(2, "B"); cache.get(1); cache.put(3, "C");
System.out.println(cache);
// Output: {1=A, 3=C}
```

This is not thread-safe and has no expiry/metrics; production caches need a proven cache library and explicit policy.

## Quick Interview Questions

- HashMap vs TreeMap? Average O(1) unordered hashing vs O(log n) sorted keys.
- ArrayList vs LinkedList? ArrayList usually wins for locality/index/iteration; LinkedList helps only specific node-end operations.
- HashSet uniqueness depends on what? Correct `equals` and `hashCode`.
- Why use ArrayDeque instead of Stack? Modern unsynchronized Deque API with better design/performance.
- Collection vs Collections? Core interface vs utility class.
- Collection vs Map? Elements vs key-value associations; Map does not extend Collection.
- List vs Set? Ordered duplicates/indexed sequence vs uniqueness contract.
- HashMap nulls? One null key and multiple null values; not thread-safe.
- HashMap collision? Entries share a bucket and modern high-collision buckets may treeify under conditions.
- Why immutable map key? Mutating equality/hash fields can make the entry unreachable by lookup.
- LinkedHashMap use? Predictable insertion/access order and LRU-style policies.
- Hashtable vs ConcurrentHashMap? Legacy whole-operation synchronization/no nulls vs scalable modern concurrent map/no nulls.
- Fail-fast iterator? Best-effort ConcurrentModificationException on unsafe structural modification, not a thread-safety guarantee.
- CopyOnWriteArrayList use? Small read-heavy listener snapshots; writes copy entire array.
- Comparable vs Comparator? Natural ordering inside type vs external/multiple orderings.
- PriorityQueue order? Only head is guaranteed minimum/maximum by comparator; iteration is not sorted.
- Unmodifiable vs immutable? Wrapper may reflect backing mutation; immutable copy owns stable content.
- ConcurrentHashMap check-then-put? Not atomic; use computeIfAbsent/putIfAbsent/compute.
- Big-O HashMap? Average O(1), but hashing/collisions/key cost and worst cases matter.
