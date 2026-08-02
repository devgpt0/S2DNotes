# Counting Sort

## Idea

Counting sort avoids comparisons by counting each integer key. It is useful
only when the key range is reasonably small.

## Classroom board: count instead of compare

```text
values:     [3, 1, 2, 1]
frequency:   1->2, 2->1, 3->1

emit 1 twice -> [1,1]
emit 2 once  -> [1,1,2]
emit 3 once  -> [1,1,2,3]
```

This is fast only because the possible key range is small.

## Steps

1. Allocate one counter per key.
2. Count every input value.
3. Emit keys from minimum to maximum using their frequencies.

## First-principles derivation

Comparison sorting discovers order by comparisons. When the value range is
small, count how many copies of each value exist and rebuild values in numeric
order.

The frequency array is a complete lossless description when only values, not
record identity, matter.

## Pattern recognition

Use it when integer keys occupy a small known range and `n + keyRange` fits.

### C++

```cpp
std::vector<int> countingSort(const std::vector<int>& values, int minimum, int maximum) {
    std::vector<int> frequency(maximum - minimum + 1, 0);
    for (int value : values) ++frequency[value - minimum];
    std::vector<int> result;
    result.reserve(values.size());
    for (int key = 0; key < static_cast<int>(frequency.size()); ++key) {
        result.insert(result.end(), frequency[key], key + minimum);
    }
    return result;
}
```

### Python

```python
def counting_sort(values: list[int], minimum: int, maximum: int) -> list[int]:
    frequency = [0] * (maximum - minimum + 1)
    for value in values:
        frequency[value - minimum] += 1
    result: list[int] = []
    for key, count in enumerate(frequency, start=minimum):
        result.extend([key] * count)
    return result
```

### Java

```java
static int[] countingSort(int[] values, int minimum, int maximum) {
    int[] frequency = new int[maximum - minimum + 1];
    for (int value : values) frequency[value - minimum]++;
    int[] result = new int[values.length];
    int write = 0;
    for (int key = 0; key < frequency.length; key++) {
        for (int count = frequency[key]; count > 0; count--) {
            result[write++] = key + minimum;
        }
    }
    return result;
}
```

## Why it works

The table stores the exact multiplicity of every ordered key, so emitting from
small to large recreates the sorted multiset.

## Complexity

For `n` values and key range `k = maximum - minimum + 1`, time is `O(n + k)`
and space is `O(k + n)` including output.

> [!WARNING]
> Validate that `k` fits memory before allocating. Values near `-10^9` and
> `10^9` make counting sort inappropriate even if `n` is small.

## Common mistakes

- Forgetting the minimum offset for negative keys.
- Allocating a huge key range.
- Calling the simple emission version stable for attached records.
