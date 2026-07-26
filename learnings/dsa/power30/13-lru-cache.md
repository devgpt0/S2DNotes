# Problem 13: LRU Cache (LeetCode #146)

**Difficulty:** Medium · **Pattern:** Hash map + doubly linked list

## Problem Statement

Implement `get(key)` and `put(key, value)` with least-recently-used eviction, each in `O(1)` average time.

## Example

With capacity `2`, `put(1,1), put(2,2), get(1), put(3,3)` evicts key `2`.

## Observation

A hash map provides fast lookup but cannot track recency. A doubly linked list
tracks recency but cannot find a key quickly. Combining them gives both
operations in constant time.

## Learning diagram

```text
map key -> list node; HEAD <-> most recent ... least recent <-> TAIL
```

## Algorithm for the optimal approach

Use a map for lookup and a doubly linked list for constant-time recency changes.

## Pattern to remember

> O(1) lookup plus O(1) ordering -> map + doubly linked list.

## Solution 1: Brute Force

### Observation

Use a list and linearly locate keys. Time: `O(capacity)` per operation.

### Algorithm

1. Store cache entries in a list ordered from most to least recently used.
2. For `get`, linearly find the key and move it to the front.
3. For `put`, linearly find and update an existing key, or insert a new front
   entry.
4. Remove the last entry when capacity is exceeded.

### C++ code

```cpp
class LRUCache {
   private:
    int capacity;
    vector<pair<int, int>> entries;

   public:
    explicit LRUCache(int capacity) : capacity(capacity) {}

    int get(int key) {
        for (int index = 0; index < static_cast<int>(entries.size()); ++index) {
            if (entries[index].first == key) {
                int value = entries[index].second;
                entries.erase(entries.begin() + index);
                entries.insert(entries.begin(), {key, value});
                return value;
            }
        }
        return -1;
    }

    void put(int key, int value) {
        for (int index = 0; index < static_cast<int>(entries.size()); ++index) {
            if (entries[index].first == key) {
                entries.erase(entries.begin() + index);
                break;
            }
        }

        entries.insert(entries.begin(), {key, value});
        if (static_cast<int>(entries.size()) > capacity) {
            entries.pop_back();
        }
    }
};
```

### Complexity

- Time: `O(capacity)` per operation
- Space: `O(capacity)`

## How we derive the optimal solution

```text
One list stores recency, but key lookup is linear
                 |
                 v
A hash map finds keys in O(1), but does not maintain order
                 |
                 v
Need both lookup and constant-time move/remove operations
                 |
                 v
Map key -> node in a doubly linked list
                 |
                 v
O(1) average get and put
```

## Optimized and Competitive Programming Approach — Map + Recency List

Map each key to a list node. Move accessed nodes to the front and evict from the tail. Time: `O(1)` average per operation. Space: `O(capacity)`.

### C++

```cpp
class LRUCache {
    int cap;
    list<pair<int, int>> order;
    unordered_map<int, list<pair<int, int>>::iterator> pos;

   public:
    LRUCache(int c) : cap(c) {}
    int get(int k) {
        auto it = pos.find(k);
        if (it == pos.end()) return -1;
        order.splice(order.begin(), order, it->second);
        return it->second->second;
    }
    void put(int k, int v) {
        auto it = pos.find(k);
        if (it != pos.end()) {
            it->second->second = v;
            order.splice(order.begin(), order, it->second);
            return;
        }
        order.push_front({k, v});
        pos[k] = order.begin();
        if ((int)order.size() > cap) {
            pos.erase(order.back().first);
            order.pop_back();
        }
    }
};
```

### Python

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity, self.items = capacity, OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.items:
            return -1
        self.items.move_to_end(key)
        return self.items[key]

    def put(self, key: int, value: int) -> None:
        if key in self.items:
            self.items.move_to_end(key)
        self.items[key] = value
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)
```

### Java

```java
class LRUCache {
    private final int capacity;
    private final LinkedHashMap<Integer, Integer> cache;

    LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>(capacity, 0.75f, true);
    }

    int get(int key) {
        return cache.getOrDefault(key, -1);
    }

    void put(int key, int value) {
        cache.put(key, value);

        if (cache.size() > capacity) {
            int leastRecentlyUsed = cache.keySet().iterator().next();
            cache.remove(leastRecentlyUsed);
        }
    }
}
```

### Go

```go
type LRUCache struct {
	cap   int
	items map[int]*list.Element
	order *list.List
}
type entry struct{ key, value int }

func NewLRU(c int) *LRUCache { return &LRUCache{c, map[int]*list.Element{}, list.New()} }
func (c *LRUCache) Get(k int) int {
	e, ok := c.items[k]
	if !ok {
		return -1
	}
	c.order.MoveToFront(e)
	return e.Value.(entry).value
}
func (c *LRUCache) Put(k, v int) {
	if e, ok := c.items[k]; ok {
		e.Value = entry{k, v}
		c.order.MoveToFront(e)
		return
	}
	c.items[k] = c.order.PushFront(entry{k, v})
	if c.order.Len() > c.cap {
		e := c.order.Back()
		delete(c.items, e.Value.(entry).key)
		c.order.Remove(e)
	}
}
```

## Key Invariant

The front is most recently used; every map entry points to exactly one list element.
