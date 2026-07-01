# 12 - Map Design Patterns (Production-Oriented)

## 1) Frequency Counter Pattern

Concept taught: Counting events safely with `merge`.

```java
List<String> events = List.of("login", "logout", "login", "login");
Map<String, Integer> freq = new HashMap<>();
for (String e : events) {
    freq.merge(e, 1, Integer::sum);
}
System.out.println(freq);
```

Expected output:

```text
{logout=1, login=3}
```

## 2) Group-By Pattern

Concept taught: Building `key -> list` groups lazily.

```java
List<String> words = List.of("ant", "apple", "bat", "ball");
Map<Character, List<String>> groups = new HashMap<>();
for (String w : words) {
    groups.computeIfAbsent(w.charAt(0), k -> new ArrayList<>()).add(w);
}
System.out.println(groups);
```

Possible output:

```text
{a=[ant, apple], b=[bat, ball]}
```

## 3) Index Builder Pattern

Concept taught: Fast by-id lookup map from object list.

```java
record User(long id, String name) {}
List<User> users = List.of(new User(1, "A"), new User(2, "B"));
Map<Long, User> byId = users.stream()
    .collect(Collectors.toMap(User::id, u -> u));
System.out.println(byId.get(2));
```

Expected output:

```text
User[id=2, name=B]
```

For duplicate keys, provide merge function.

Concept taught: Duplicate-key safe `toMap` collector.

```java
Map<Long, User> byIdSafe = users.stream().collect(
    Collectors.toMap(User::id, u -> u, (oldV, newV) -> oldV)
);
System.out.println(byIdSafe.size());
```

Expected output:

```text
2
```

## 4) Multi-Level Aggregation Pattern

Concept taught: Nested map updates with chained `computeIfAbsent` + `merge`.

```java
record Tx(String user, String type, int amount) {}
List<Tx> txs = List.of(
    new Tx("u1", "food", 100),
    new Tx("u1", "food", 50),
    new Tx("u1", "travel", 200),
    new Tx("u2", "food", 70)
);

Map<String, Map<String, Integer>> agg = new HashMap<>();
for (Tx t : txs) {
    agg.computeIfAbsent(t.user(), k -> new HashMap<>())
       .merge(t.type(), t.amount(), Integer::sum);
}
System.out.println(agg);
```

Possible output:

```text
{u1={travel=200, food=150}, u2={food=70}}
```

## 5) LRU Cache Pattern

Concept taught: Access-ordered `LinkedHashMap` with eviction policy.

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

LRU<Integer, String> cache = new LRU<>(2);
cache.put(1, "A");
cache.put(2, "B");
cache.get(1);
cache.put(3, "C");
System.out.println(cache);
```

Expected output:

```text
{1=A, 3=C}
```

## 6) Reverse Index Pattern

Concept taught: Maintain `value -> keys` for fast reverse lookup.

```java
Map<Integer, String> idToDept = Map.of(1, "IT", 2, "HR", 3, "IT");
Map<String, Set<Integer>> deptToIds = new HashMap<>();

for (Map.Entry<Integer, String> e : idToDept.entrySet()) {
    deptToIds.computeIfAbsent(e.getValue(), k -> new LinkedHashSet<>()).add(e.getKey());
}

System.out.println(deptToIds);
```

Possible output:

```text
{IT=[1, 3], HR=[2]}
```

## 7) Idempotent Upsert Pattern

Concept taught: Upsert (insert/update) with `compute`.

```java
Map<String, Integer> score = new HashMap<>();
score.compute("A", (k, v) -> v == null ? 10 : v + 10);
score.compute("A", (k, v) -> v == null ? 10 : v + 10);
System.out.println(score);
```

Expected output:

```text
{A=20}
```

## 8) Summary

Map design patterns are mostly combinations of `merge`, `computeIfAbsent`, and clean key modeling. Master these and most business aggregation problems become straightforward.
