# 05 - Common Patterns With Map (Complete)

## 1) Frequency Counter

Concept taught: Counting occurrences with `merge`.

```java
String s = "banana";
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}
System.out.println(freq);
```

Possible output:

```text
{a=3, b=1, n=2}
```

## 2) Grouping Words by Anagram Signature

Concept taught: Grouping with `computeIfAbsent`.

```java
List<String> words = List.of("eat", "tea", "tan", "ate", "nat", "bat");
Map<String, List<String>> groups = new HashMap<>();

for (String word : words) {
    char[] arr = word.toCharArray();
    Arrays.sort(arr);
    String key = new String(arr);
    groups.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
}

System.out.println(groups);
```

Possible output:

```text
{aet=[eat, tea, ate], ant=[tan, nat], abt=[bat]}
```

## 3) Two Sum (Index Map)

Concept taught: Using map for complement lookup in linear time.

```java
int[] nums = {2, 7, 11, 15};
int target = 9;
Map<Integer, Integer> pos = new HashMap<>();

for (int i = 0; i < nums.length; i++) {
    int need = target - nums[i];
    if (pos.containsKey(need)) {
        System.out.println(Arrays.toString(new int[]{pos.get(need), i}));
        break;
    }
    pos.put(nums[i], i);
}
```

Expected output:

```text
[0, 1]
```

## 4) Inverted Index (`value -> list of keys`)

Concept taught: Reverse mapping and multi-value accumulation.

```java
Map<Integer, String> src = Map.of(1, "A", 2, "B", 3, "A");
Map<String, List<Integer>> inv = new HashMap<>();

for (Map.Entry<Integer, String> e : src.entrySet()) {
    inv.computeIfAbsent(e.getValue(), k -> new ArrayList<>()).add(e.getKey());
}

System.out.println(inv);
```

Possible output:

```text
{A=[1, 3], B=[2]}
```

## 5) Merge Two Maps (Sum on Common Keys)

Concept taught: `merge` simplifies conflict resolution.

```java
Map<String, Integer> a = new HashMap<>(Map.of("x", 1, "y", 2));
Map<String, Integer> b = Map.of("y", 5, "z", 9);

for (Map.Entry<String, Integer> e : b.entrySet()) {
    a.merge(e.getKey(), e.getValue(), Integer::sum);
}

System.out.println(a);
```

Possible output:

```text
{x=1, y=7, z=9}
```

## 6) Top-K Frequent Elements (Map + Heap)

Concept taught: Combine frequency map with priority queue.

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

## 7) Nested Aggregation (User -> Category -> Amount)

Concept taught: Multi-level maps with chained `computeIfAbsent` + `merge`.

```java
record Tx(String user, String category, int amount) {}
List<Tx> txs = List.of(
    new Tx("u1", "food", 100),
    new Tx("u1", "travel", 200),
    new Tx("u1", "food", 50),
    new Tx("u2", "food", 70)
);

Map<String, Map<String, Integer>> stats = new HashMap<>();
for (Tx t : txs) {
    stats.computeIfAbsent(t.user(), k -> new HashMap<>())
         .merge(t.category(), t.amount(), Integer::sum);
}

System.out.println(stats);
```

Possible output:

```text
{u1={travel=200, food=150}, u2={food=70}}
```

## 8) LRU Cache Pattern (`LinkedHashMap`)

Concept taught: Access-order eviction via `removeEldestEntry`.

```java
class LRU<K, V> extends LinkedHashMap<K, V> {
    private final int cap;
    LRU(int cap) {
        super(Math.max(16, cap), 0.75f, true);
        this.cap = cap;
    }
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > cap;
    }
}

LRU<Integer, String> cache = new LRU<>(3);
cache.put(1, "A");
cache.put(2, "B");
cache.put(3, "C");
cache.get(1);
cache.put(4, "D");
System.out.println(cache);
```

Expected output:

```text
{3=C, 1=A, 4=D}
```

## 9) Summary

These map patterns (counting, grouping, joining, top-k, LRU) cover most interview and real service-layer map problems.
