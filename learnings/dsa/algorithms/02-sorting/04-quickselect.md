# Quickselect

## Idea

Quickselect finds the value that would appear at index `k` in sorted order
without sorting everything. Partitioning discards the region that cannot
contain `k`.

The implementation uses three-way partitioning, which is important when many
values equal the pivot.

## Classroom board: find sorted index 3

```text
partition gives [1,2 | 4,4 | 7]
sorted indexes:     0 1   2 3   4

k = 3 lies inside the equal-to-4 region -> answer is 4
```

If `k` were `0`, only `[1,2]` could contain it. We discard every other value
instead of sorting it.

## Steps

1. Partition around a pivot.
2. Keep the only region that can contain index `k`.
3. Return the pivot when `k` lies in the equal region.

## First-principles derivation

To find one rank, fully sorting both sides is wasted work. Partition around a
pivot, learn the pivot's final rank, and continue only in the side containing
the requested rank.

Every discarded partition is proven not to contain the answer.

## Pattern recognition

Use quickselect for one or a few order statistics when full sorting is
unnecessary and expected linear time is acceptable.

### C++

```cpp
int quickselect(std::vector<int> values, int k) {
    int left = 0;
    int right = values.size();
    while (true) {
        const int pivot = values[left + (right - left) / 2];
        int lower = left;
        int current = left;
        int upper = right;
        while (current < upper) {
            if (values[current] < pivot) std::swap(values[lower++], values[current++]);
            else if (values[current] > pivot) std::swap(values[current], values[--upper]);
            else ++current;
        }
        if (k < lower) right = lower;
        else if (k >= upper) left = upper;
        else return pivot;
    }
}
```

### Python

```python
def quickselect(values: list[int], k: int) -> int:
    items = values.copy()
    left, right = 0, len(items)
    while True:
        pivot = items[left + (right - left) // 2]
        lower = current = left
        upper = right
        while current < upper:
            if items[current] < pivot:
                items[lower], items[current] = items[current], items[lower]
                lower += 1
                current += 1
            elif items[current] > pivot:
                upper -= 1
                items[current], items[upper] = items[upper], items[current]
            else:
                current += 1
        if k < lower:
            right = lower
        elif k >= upper:
            left = upper
        else:
            return pivot
```

### Java

```java
static int quickselect(int[] input, int k) {
    int[] values = input.clone();
    int left = 0;
    int right = values.length;
    while (true) {
        int pivot = values[left + (right - left) / 2];
        int lower = left;
        int current = left;
        int upper = right;
        while (current < upper) {
            if (values[current] < pivot) swap(values, lower++, current++);
            else if (values[current] > pivot) swap(values, current, --upper);
            else current++;
        }
        if (k < lower) right = lower;
        else if (k >= upper) left = upper;
        else return pivot;
    }
}

static void swap(int[] values, int first, int second) {
    int value = values[first];
    values[first] = values[second];
    values[second] = value;
}
```

## Why it works

Partitioning determines the final rank range of all pivot-equal values, so at
most one outer region can contain `k`.

## Complexity

Expected time is `O(n)` with good pivot selection; worst case is `O(n^2)`.
The contract requires `0 <= k < n`. For many order-statistic queries, sort
once or use a different data structure.

## Common mistakes

- Mixing one-based and zero-based `k`.
- Keeping both partition sides.
- Mishandling many values equal to the pivot.
