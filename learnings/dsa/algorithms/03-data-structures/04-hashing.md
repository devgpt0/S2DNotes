# Hash Tables and Frequency Maps

## Idea

A hash table stores key-to-value relationships with expected `O(1)` lookup.
A set stores only keys; a map can store counts, indices, or other information.

## Visual model

```text
key -> hash -> bucket -> stored value
```

## Classroom board: count pairs summing to 6

```text
values = [1, 5, 1, 5]

value  need  earlier frequency  pairs added
1      5     0                  0
5      1     1                  1
1      5     1                  1
5      1     2                  2
total = 4 pairs
```

Count before inserting the current value so it can pair only with earlier
positions.

## Steps

1. Decide what fact must be remembered for each key.
2. Look up the needed key in the table.
3. Insert or update the current key.

## First-principles derivation

Linear search repeatedly asks whether a key was seen. Hashing computes a bucket
from the key so membership and frequency updates avoid scanning all keys.

The table remains the source of truth for the current key-to-value mapping;
operations are expected `O(1)`, not guaranteed worst-case `O(1)`.

## Pattern recognition

Look for fast membership, duplicates, frequencies, complements, grouping, or
remembering the first/last position of a value.

## Implementation: count target-sum pairs

### C++

```cpp
long long countPairs(const std::vector<int>& values, int target) {
    std::unordered_map<int, int> frequency;
    long long answer = 0;
    for (int value : values) {
        answer += frequency[target - value];
        ++frequency[value];
    }
    return answer;
}
```

### Python

```python
def count_pairs(values: list[int], target: int) -> int:
    frequency: dict[int, int] = {}
    answer = 0
    for value in values:
        answer += frequency.get(target - value, 0)
        frequency[value] = frequency.get(value, 0) + 1
    return answer
```

### Java

```java
static long countPairs(int[] values, int target) {
    Map<Integer, Integer> frequency = new HashMap<>();
    long answer = 0;
    for (int value : values) {
        answer += frequency.getOrDefault(target - value, 0);
        frequency.merge(value, 1, Integer::sum);
    }
    return answer;
}
```

## Why it works

When reading `value`, the map contains exactly the earlier values. Each earlier
matching complement forms one unique pair and is counted once.

## Complexity

Expected time is `O(n)` and space is `O(n)`. Worst-case hash behavior can be
linear per operation.

## Common mistakes

- Inserting before counting when an element must not pair with itself.
- Using a set when duplicate counts matter.
- Relying on hash-map iteration order.
- Using mutable objects as keys.
