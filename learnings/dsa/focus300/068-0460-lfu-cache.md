# Focus300 068: LeetCode 460 - LFU Cache

**Source:** [LeetCode 460](https://leetcode.com/problems/lfu-cache/)  
**Difficulty:** Hard  
**Pattern:** frequency buckets with LRU order inside each bucket

## Exact contract

Implement a fixed-capacity cache with `get(key)` and `put(key,value)` in average
`O(1)`. Both a successful get and updating an existing key increase its use
frequency. When full, evict the least frequently used key; break frequency ties
by least recent use. `get` returns `-1` for a missing key.

## First principles

Map each key to `(value,frequency)`. For every frequency, maintain keys in LRU
order. Touching a key removes it from its current frequency bucket and appends
it to frequency plus one. Track the minimum active frequency so eviction needs
no scan.

An insertion always has frequency one and becomes the new minimum. An
`OrderedDict` supplies constant-time delete, append, and oldest-key removal.

## Cases that decide correctness

- Capacity zero stores nothing.
- Updating an existing key counts as use.
- A successful get changes recency within the new frequency bucket.
- Eviction uses LRU only among keys tied at minimum frequency.
- Removing the last key in the minimum bucket advances the minimum frequency.

## Brute force: scan all entries at eviction time

```python
class LFUCacheBrute:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.clock = 0
        self.entries: dict[int, tuple[int, int, int]] = {}

    def get(self, key: int) -> int:
        if key not in self.entries:
            return -1
        value, frequency, _ = self.entries[key]
        self.clock += 1
        self.entries[key] = (value, frequency + 1, self.clock)
        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.entries:
            _, frequency, _ = self.entries[key]
            self.clock += 1
            self.entries[key] = (value, frequency + 1, self.clock)
            return
        if len(self.entries) == self.capacity:
            victim = min(
                self.entries,
                key=lambda candidate: (
                    self.entries[candidate][1],
                    self.entries[candidate][2],
                ),
            )
            del self.entries[victim]
        self.clock += 1
        self.entries[key] = (value, 1, self.clock)
```

Get and update are constant time, but eviction scans `O(capacity)` entries.

## Better insight: eviction needs only the oldest key at the minimum frequency

Separate LRU ordering by frequency. Then no global ordering is maintained and
every touch moves between exactly two buckets.

## Expert solution: hash maps of ordered frequency buckets

```python
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.minimum_frequency = 0
        self.values: dict[int, tuple[int, int]] = {}
        self.frequency_keys: dict[int, OrderedDict[int, None]] = defaultdict(
            OrderedDict
        )

    def _touch(self, key: int, value: int, frequency: int) -> None:
        bucket = self.frequency_keys[frequency]
        del bucket[key]
        if not bucket:
            del self.frequency_keys[frequency]
            if self.minimum_frequency == frequency:
                self.minimum_frequency += 1
        next_frequency = frequency + 1
        self.frequency_keys[next_frequency][key] = None
        self.values[key] = (value, next_frequency)

    def get(self, key: int) -> int:
        entry = self.values.get(key)
        if entry is None:
            return -1
        value, frequency = entry
        self._touch(key, value, frequency)
        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        entry = self.values.get(key)
        if entry is not None:
            _, frequency = entry
            self._touch(key, value, frequency)
            return
        if len(self.values) == self.capacity:
            bucket = self.frequency_keys[self.minimum_frequency]
            victim, _ = bucket.popitem(last=False)
            del self.values[victim]
            if not bucket:
                del self.frequency_keys[self.minimum_frequency]
        self.values[key] = (value, 1)
        self.frequency_keys[1][key] = None
        self.minimum_frequency = 1
```

Every API call performs a constant number of hash and ordered-bucket
operations, while the minimum-frequency pointer identifies the eviction bucket.

**Complexity:** average `O(1)` per operation and `O(capacity)` space.
