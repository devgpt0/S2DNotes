# Focus300 064: LeetCode 432 - All O`one Data Structure

**Source:** [LeetCode 432](https://leetcode.com/problems/all-oone-data-structure/)  
**Difficulty:** Hard  
**Pattern:** hash map plus doubly linked frequency buckets

## Exact contract

Implement `inc(key)`, `dec(key)`, `getMaxKey()`, and `getMinKey()` in average
`O(1)` time. New keys begin at count one. `dec` is called only for existing
keys and removes a key whose count becomes zero. Min/max may return any tied
key, or an empty string when no key exists.

## First principles

Keys with equal counts share one bucket. Buckets are kept in strictly increasing
count order in a doubly linked list. Increment and decrement move a key only to
an adjacent count, creating that bucket if absent. A key-to-bucket map gives
direct access, and empty buckets are removed immediately.

Sentinel endpoints make min and max the first and last real buckets.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- Incrementing a new key creates or reuses count-one.
- Decrementing count one removes the key entirely.
- Moving the last key out of a bucket removes that bucket.
- Tied min/max keys may be returned arbitrarily.
- Empty state returns `""` for both queries.

## Brute force: scan a count dictionary for min and max

```python
class AllOneBrute:
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def inc(self, key: str) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1

    def dec(self, key: str) -> None:
        count = self.counts[key] - 1
        if count:
            self.counts[key] = count
        else:
            del self.counts[key]

    def getMaxKey(self) -> str:
        return max(self.counts, key=lambda key: self.counts[key]) if self.counts else ""

    def getMinKey(self) -> str:
        return min(self.counts, key=lambda key: self.counts[key]) if self.counts else ""
```

Updates are constant time, but min/max queries scan all keys.

## Better insight: counts change by exactly one

Because an update moves only to an adjacent frequency, a linked ordered bucket
list needs no tree or heap. Hash maps supply direct key and bucket access.

## Expert solution: ordered buckets with constant-time moves

```python
class Bucket:
    def __init__(self, count: int) -> None:
        self.count = count
        self.keys: set[str] = set()
        self.previous: Bucket | None = None
        self.next: Bucket | None = None


class AllOne:
    def __init__(self) -> None:
        self.head = Bucket(0)
        self.tail = Bucket(0)
        self.head.next = self.tail
        self.tail.previous = self.head
        self.key_bucket: dict[str, Bucket] = {}

    @staticmethod
    def _insert_after(current: Bucket, new_bucket: Bucket) -> None:
        following = current.next
        if following is None:
            raise RuntimeError("bucket list is not terminated")
        new_bucket.previous = current
        new_bucket.next = following
        current.next = new_bucket
        following.previous = new_bucket

    @staticmethod
    def _remove(bucket: Bucket) -> None:
        previous = bucket.previous
        following = bucket.next
        if previous is None or following is None:
            raise RuntimeError("cannot remove a sentinel")
        previous.next = following
        following.previous = previous

    def inc(self, key: str) -> None:
        current = self.key_bucket.get(key)
        if current is None:
            target = self.head.next
            if target is None:
                raise RuntimeError("bucket list is not terminated")
            if target is self.tail or target.count != 1:
                target = Bucket(1)
                self._insert_after(self.head, target)
        else:
            target = current.next
            if target is None:
                raise RuntimeError("bucket list is not terminated")
            if target is self.tail or target.count != current.count + 1:
                target = Bucket(current.count + 1)
                self._insert_after(current, target)
            current.keys.remove(key)
            if not current.keys:
                self._remove(current)
        target.keys.add(key)
        self.key_bucket[key] = target

    def dec(self, key: str) -> None:
        current = self.key_bucket[key]
        if current.count == 1:
            del self.key_bucket[key]
        else:
            target = current.previous
            if target is None:
                raise RuntimeError("bucket list has no head")
            if target is self.head or target.count != current.count - 1:
                target = Bucket(current.count - 1)
                previous = current.previous
                if previous is None:
                    raise RuntimeError("bucket list has no head")
                self._insert_after(previous, target)
            target.keys.add(key)
            self.key_bucket[key] = target
        current.keys.remove(key)
        if not current.keys:
            self._remove(current)

    def getMaxKey(self) -> str:
        bucket = self.tail.previous
        if bucket is None or bucket is self.head:
            return ""
        return next(iter(bucket.keys))

    def getMinKey(self) -> str:
        bucket = self.head.next
        if bucket is None or bucket is self.tail:
            return ""
        return next(iter(bucket.keys))
```

The bucket list contains one node per active count and each operation changes a
constant number of hash-table entries and links.

**Complexity:** average `O(1)` per operation and `O(number_of_keys)` space.
