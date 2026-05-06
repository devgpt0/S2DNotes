# 12 - Map Design Patterns

## 1) Frequency Counter

```java
Map<String, Integer> freq = new HashMap<>();
for (String w : words) {
    freq.merge(w, 1, Integer::sum);
}
```

## 2) Group By Key

```java
Map<String, List<String>> groups = new HashMap<>();
for (String w : words) {
    String key = w.substring(0, 1);
    groups.computeIfAbsent(key, k -> new ArrayList<>()).add(w);
}
```

## 3) Index Builder

```java
Map<Long, User> byId = users.stream()
    .collect(Collectors.toMap(User::id, u -> u));
```

Handle duplicate key safely:

```java
Collectors.toMap(User::id, u -> u, (oldV, newV) -> oldV);
```

## 4) Multi-Level Aggregation

```java
Map<String, Map<String, Integer>> stats = new HashMap<>();
stats.computeIfAbsent("teamA", k -> new HashMap<>())
     .merge("success", 1, Integer::sum);
```

## 5) LRU Cache Pattern

Use `LinkedHashMap` with `accessOrder=true` + `removeEldestEntry`.

See [01-linkedhashmap-core.md](./01-linkedhashmap-core.md) for complete implementation.
