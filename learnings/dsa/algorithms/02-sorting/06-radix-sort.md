# Radix Sort

## Idea

Radix sort processes fixed-width integer digits from least significant to most
significant using a stable digit sort. This reference handles non-negative
32-bit integers in four base-256 passes.

## Classroom board: sort one digit at a time

```text
values: 21, 13, 12

ones digit stable sort: 21, 12, 13
tens digit stable sort: 12, 13, 21
```

The second pass keeps `12` before `13`, the order established by the ones
digit. That is why the digit sort must be stable.

## Steps

1. Stable-sort by the lowest digit.
2. Repeat for every more significant digit.
3. Keep the output of one pass as input to the next.

## First-principles derivation

A large key can be ordered one digit at a time. Stable sorting by the next more
significant digit preserves the order already established by less significant
digits.

After processing digit `d`, values are correctly ordered by their last
`d + 1` digits.

## Pattern recognition

Use it for many fixed-width keys when the digit alphabet is small and
comparison sorting is too slow.

### C++

```cpp
void radixSort(std::vector<unsigned int>& values) {
    std::vector<unsigned int> output(values.size());
    for (int shift = 0; shift < 32; shift += 8) {
        std::array<int, 256> count{};
        for (unsigned int value : values) ++count[(value >> shift) & 255U];
        for (int digit = 1; digit < 256; ++digit) count[digit] += count[digit - 1];
        for (int index = static_cast<int>(values.size()) - 1; index >= 0; --index) {
            const int digit = (values[index] >> shift) & 255U;
            output[--count[digit]] = values[index];
        }
        values.swap(output);
    }
}
```

### Python

```python
def radix_sort(values: list[int]) -> list[int]:
    result = values.copy()
    for shift in range(0, 32, 8):
        buckets: list[list[int]] = [[] for _ in range(256)]
        for value in result:
            buckets[(value >> shift) & 255].append(value)
        result = [value for bucket in buckets for value in bucket]
    return result
```

### Java

```java
static void radixSort(int[] values) {
    int[] output = new int[values.length];
    for (int shift = 0; shift < 32; shift += 8) {
        int[] count = new int[256];
        for (int value : values) count[(value >>> shift) & 255]++;
        for (int digit = 1; digit < 256; digit++) count[digit] += count[digit - 1];
        for (int index = values.length - 1; index >= 0; index--) {
            int digit = (values[index] >>> shift) & 255;
            output[--count[digit]] = values[index];
        }
        System.arraycopy(output, 0, values, 0, values.length);
    }
}
```

## Why it works

Stability preserves the ordering from lower digits while the next pass orders
by a higher digit.

## Complexity

With a fixed four passes, time is `O(n)` and auxiliary space is `O(n + 256)`.
The shown ordering is unsigned; signed integers require flipping the sign bit
for ordering or separating negatives. Prefer library sorting unless constraints
prove radix sort is necessary.

## Common mistakes

- Using an unstable digit sort.
- Treating signed integers as unsigned without adjusting the sign bit.
- Forgetting that the buffers swap roles after each pass.
