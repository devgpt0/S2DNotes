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

## 4) Inverted Index (value -> keys)

```java
Map<String, List<Integer>> inv = new HashMap<>();
for (Map.Entry<Integer, String> e : input.entrySet()) {
    inv.computeIfAbsent(e.getValue(), k -> new ArrayList<>()).add(e.getKey());
}
```

## 5) LRU Cache (LinkedHashMap)

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private static final long serialVersionUID = 1L;

    private final int capacity;

    public LRUCache(int capacity) {
        // accessOrder = true => recently accessed entries move to end
        super(Math.max(16, capacity), 0.75f, true);
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be > 0");
        }
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }

    public int capacity() {
        return capacity;
    }

    // Optional convenience methods
    public V putValue(K key, V value) {
        return super.put(key, value);
    }

    public V getValue(K key) {
        return super.get(key);
    }

    public boolean containsKeyValue(K key) {
        return super.containsKey(key);
    }

    public V removeValue(K key) {
        return super.remove(key);
    }

    public static void main(String[] args) {
        LRUCache<Integer, String> cache = new LRUCache<>(3);

        cache.putValue(1, "A");
        cache.putValue(2, "B");
        cache.putValue(3, "C");
        System.out.println(cache); // {1=A, 2=B, 3=C}

        cache.getValue(1);         // 1 becomes most recently used
        cache.putValue(4, "D");    // evicts key 2 (least recently used)
        System.out.println(cache); // {3=C, 1=A, 4=D}
    }
}

```
