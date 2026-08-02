# Coordinate Compression

## Idea

Coordinate compression replaces large, sparse values by their sorted ranks
while preserving equality and order.

## Visual model

```text
values:  [1000000000, -5, 1000000000, 20]
unique:  [-5, 20, 1000000000]
ranks:   [2, 0, 2, 1]
```

It enables array-indexed structures such as Fenwick trees without allocating
up to the largest coordinate.

## Classroom board: replace values by rank

```text
original: [1000, -5, 1000, 20]
sort unique values: [-5, 20, 1000]

-5   -> rank 0
20   -> rank 1
1000 -> rank 2

compressed original: [2, 0, 2, 1]
```

Order and equality remain correct. Actual distances do not: ranks `1` and `2`
are adjacent even though `20` and `1000` are far apart.

## Steps

1. Copy, sort, and remove duplicate coordinates.
2. Map each unique value to its index in that sorted list.
3. Replace every original value with its rank.

## First-principles derivation

Many algorithms care about value order, not the numeric gaps between values.
Replace each distinct value by its position in sorted order.

The invariant is order preservation: `a < b` exactly when
`rank(a) < rank(b)`.

## Pattern recognition

Use compression when coordinates are huge but only their relative order or
equality matters, especially before a Fenwick or segment tree.

## Implementation

### C++

```cpp
std::vector<int> compress(const std::vector<long long>& values) {
    std::vector<long long> sorted = values;
    std::sort(sorted.begin(), sorted.end());
    sorted.erase(std::unique(sorted.begin(), sorted.end()), sorted.end());

    std::vector<int> ranks;
    ranks.reserve(values.size());
    for (long long value : values) {
        ranks.push_back(std::lower_bound(sorted.begin(), sorted.end(), value) - sorted.begin());
    }
    return ranks;
}
```

### Python

```python
def compress(values: list[int]) -> list[int]:
    unique_values = sorted(set(values))
    rank = {value: index for index, value in enumerate(unique_values)}
    return [rank[value] for value in values]
```

### Java

```java
static int[] compress(long[] values) {
    long[] sorted = Arrays.stream(values).distinct().sorted().toArray();
    Map<Long, Integer> rank = new HashMap<>();
    for (int index = 0; index < sorted.length; index++) {
        rank.put(sorted[index], index);
    }
    int[] result = new int[values.length];
    for (int index = 0; index < values.length; index++) {
        result[index] = rank.get(values[index]);
    }
    return result;
}
```

## Why it works

Sorting unique values gives increasing ranks. Equal values receive the same
rank, and smaller original values always receive smaller ranks.

## Complexity

Time is `O(n log n)` and space is `O(n)`.

> [!CAUTION]
> Compression preserves order, not distances. Ranks `2` and `3` differ by one
> even when their original values differ by a billion. For interval geometry,
> preserve lengths or insert gap markers explicitly.

## Common mistakes

- Treating rank gaps as original distances.
- Giving duplicate values different ranks.
- Forgetting to include query coordinates that will be used later.
