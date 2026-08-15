# Focus300 236: LeetCode 146 - LRU Cache

**Source:** [LeetCode 146](https://leetcode.com/problems/lru-cache/)  
**Difficulty:** Medium  
**Pattern:** hash map plus doubly linked list

## Exact contract

Implement an LRU cache with `get` and `put` operations that both run in constant amortized time.

## First principles

The cache needs fast key lookup and fast recency updates. A hash map gives direct access by key, while a doubly linked list gives constant-time movement of the most and least recent entries.

## Cases that decide correctness

- Updating an existing key should refresh its recency.
- The least recently used key must be evicted when capacity is exceeded.
- A missing key should return the sentinel result required by the API.
- Both operations must stay constant-time on average.

## Brute force

```python
def lru_cache_brute(capacity):
    class LRUCache:
        def __init__(self, capacity):
            self.capacity = capacity
            self.data = []

        def get(self, key):
            for i, (k, v) in enumerate(self.data):
                if k == key:
                    self.data.append(self.data.pop(i))
                    return v
            return -1

        def put(self, key, value):
            for i, (k, _) in enumerate(self.data):
                if k == key:
                    self.data.pop(i)
                    break
            self.data.append((key, value))
            if len(self.data) > self.capacity:
                self.data.pop(0)

    return LRUCache(capacity)
```

Store entries in a plain list and scan it whenever a key is touched or evicted.

## Better insight

Pair a dictionary with a recency list so lookup and reordering are both constant-time.

## Expert solution

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)
```

Keep the most recent entry near one end of a doubly linked list, move touched nodes to that end, and evict from the opposite end when full.

**Complexity:** O(1) average time per operation and O(capacity) space.
