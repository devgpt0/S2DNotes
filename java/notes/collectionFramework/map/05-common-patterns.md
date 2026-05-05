# 05 - Common Patterns With Map

## 1) Frequency Counter

```java
Map<Character, Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) {
    freq.merge(c, 1, Integer::sum);
}
```

## 2) Grouping

```java
Map<String, List<String>> groups = new HashMap<>();
for (String word : words) {
    char[] arr = word.toCharArray();
    Arrays.sort(arr);
    String key = new String(arr);
    groups.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
}
```

## 3) Two Sum

```java
Map<Integer, Integer> pos = new HashMap<>();
for (int i = 0; i < nums.length; i++) {
    int need = target - nums[i];
    if (pos.containsKey(need)) {
        return new int[]{pos.get(need), i};
    }
    pos.put(nums[i], i);
}
```

## 4) LRU Cache (LinkedHashMap)

```java
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```
