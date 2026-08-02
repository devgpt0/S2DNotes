# Merge Sort

## Idea

Merge sort recursively sorts two halves, then merges them. Its key invariant
is that both input halves of the merge are already sorted.

```text
[8 3 2 9] -> [8 3] [2 9] -> [3 8] [2 9] -> [2 3 8 9]
```

## Classroom board: merge two sorted halves

```text
left  = [3, 8]
right = [2, 9]

fronts 3 and 2 -> take 2   result [2]
fronts 3 and 9 -> take 3   result [2,3]
fronts 8 and 9 -> take 8   result [2,3,8]
right remains 9            result [2,3,8,9]
```

Merge sort's only real operation is this merge; recursion merely prepares the
two sorted halves.

## Steps

1. Stop when a range has at most one value.
2. Split it into two halves and sort both.
3. Merge by repeatedly taking the smaller front value.

## First-principles derivation

A large unsorted range is difficult; one item is already sorted. Recursively
sort two halves, then merge them by repeatedly taking the smaller front.

During merging, the output prefix is sorted and contains the smallest items
seen so far.

## Pattern recognition

Use merge sort when stable `O(n log n)` worst-case sorting matters or when the
merge step can count cross-half relationships.

### C++

```cpp
void mergeSort(std::vector<int>& values, std::vector<int>& buffer, int left, int right) {
    if (right - left <= 1) return;
    const int middle = left + (right - left) / 2;
    mergeSort(values, buffer, left, middle);
    mergeSort(values, buffer, middle, right);

    int first = left;
    int second = middle;
    int write = left;
    while (first < middle || second < right) {
        if (second == right || (first < middle && values[first] <= values[second])) {
            buffer[write++] = values[first++];
        } else {
            buffer[write++] = values[second++];
        }
    }
    std::copy(buffer.begin() + left, buffer.begin() + right, values.begin() + left);
}

void mergeSort(std::vector<int>& values) {
    std::vector<int> buffer(values.size());
    mergeSort(values, buffer, 0, values.size());
}
```

### Python

```python
def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged: list[int] = []
    first = second = 0
    while first < len(left) and second < len(right):
        if left[first] <= right[second]:
            merged.append(left[first])
            first += 1
        else:
            merged.append(right[second])
            second += 1
    return merged + left[first:] + right[second:]
```

### Java

```java
static void mergeSort(int[] values) {
    mergeSort(values, new int[values.length], 0, values.length);
}

static void mergeSort(int[] values, int[] buffer, int left, int right) {
    if (right - left <= 1) return;
    int middle = left + (right - left) / 2;
    mergeSort(values, buffer, left, middle);
    mergeSort(values, buffer, middle, right);
    int first = left;
    int second = middle;
    int write = left;
    while (first < middle || second < right) {
        if (second == right || (first < middle && values[first] <= values[second])) {
            buffer[write++] = values[first++];
        } else {
            buffer[write++] = values[second++];
        }
    }
    System.arraycopy(buffer, left, values, left, right - left);
}
```

## Why it works

The smallest remaining value must be at the front of one sorted half, so every
merge choice is correct.

## Complexity

Time is always `O(n log n)` and auxiliary space is `O(n)`. Choosing from the
left on equality makes it stable. The merge step also powers inversion
counting and offline divide-and-conquer algorithms.

## Common mistakes

- Dropping leftover values after one half ends.
- Allocating a full buffer in every recursive call.
- Losing stability by choosing from the right on equality.
