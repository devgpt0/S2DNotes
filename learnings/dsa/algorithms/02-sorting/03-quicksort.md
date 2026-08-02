# Quicksort

## Idea

Quicksort partitions values into regions below and above a pivot, then sorts
the regions. It is typically fast and in place, but a bad pivot sequence causes
`O(n^2)` time.

This three-way partition handles duplicates well:

```text
[ values < pivot | values == pivot | unknown | values > pivot ]
```

## Classroom board: three-way partition

```text
values = [4, 2, 4, 7, 1], pivot = 4

inspect 4 -> equal region
inspect 2 -> smaller region [2]
inspect 4 -> equal region [4,4]
inspect 7 -> larger region [7]
inspect 1 -> smaller region [2,1]

partition: [2,1 | 4,4 | 7]
```

Only the left and right regions still need sorting.

## Steps

1. Choose a pivot.
2. Partition values into smaller, equal, and larger regions.
3. Recursively sort the smaller and larger regions.

## First-principles derivation

Choose a pivot and classify every value as smaller, equal, or larger. Once
partitioned, no value from the left belongs after a value from the right.

The pivot partition is fixed; only the two independent sides still need
sorting.

## Pattern recognition

Know quicksort for partition reasoning and in-place average-case sorting. Use
the language library unless implementing it is required.

### C++

```cpp
void quickSort(std::vector<int>& values, int left, int right) {
    if (right - left <= 1) return;
    const int pivot = values[left + (right - left) / 2];
    int lower = left;
    int current = left;
    int upper = right;
    while (current < upper) {
        if (values[current] < pivot) {
            std::swap(values[lower++], values[current++]);
        } else if (values[current] > pivot) {
            std::swap(values[current], values[--upper]);
        } else {
            ++current;
        }
    }
    quickSort(values, left, lower);
    quickSort(values, upper, right);
}
```

### Python

```python
def quick_sort(values: list[int], left: int, right: int) -> None:
    if right - left <= 1:
        return
    pivot = values[left + (right - left) // 2]
    lower = current = left
    upper = right
    while current < upper:
        if values[current] < pivot:
            values[lower], values[current] = values[current], values[lower]
            lower += 1
            current += 1
        elif values[current] > pivot:
            upper -= 1
            values[current], values[upper] = values[upper], values[current]
        else:
            current += 1
    quick_sort(values, left, lower)
    quick_sort(values, upper, right)
```

### Java

```java
static void quickSort(int[] values, int left, int right) {
    if (right - left <= 1) return;
    int pivot = values[left + (right - left) / 2];
    int lower = left;
    int current = left;
    int upper = right;
    while (current < upper) {
        if (values[current] < pivot) {
            swap(values, lower++, current++);
        } else if (values[current] > pivot) {
            swap(values, current, --upper);
        } else {
            current++;
        }
    }
    quickSort(values, left, lower);
    quickSort(values, upper, right);
}

static void swap(int[] values, int first, int second) {
    int temporary = values[first];
    values[first] = values[second];
    values[second] = temporary;
}
```

## Why it works

Partitioning fixes the pivot region's relative place. Only the two independent
outer regions remain unsorted.

## Complexity

Expected time with well-distributed or randomized pivots is `O(n log n)`;
worst case is `O(n^2)`. Expected stack space is `O(log n)`. Use the standard
library sort in contests unless implementing quicksort is the task.

## Common mistakes

- Failing to advance through values equal to the pivot.
- Recursing on an unchanged pivot region.
- Claiming worst-case `O(n log n)` without a pivot guarantee.
