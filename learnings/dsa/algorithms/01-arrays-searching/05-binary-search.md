# Binary Search

## Idea

Binary search locates a boundary in sorted or monotone data. Prefer the
half-open interval `[left, right)`; it gives one loop condition and avoids
special-case neighbors.

## Visual model: lower bound

Find the first index whose value is at least `target`. The invariant is:

- every index before `left` has value `< target`;
- every index at or after `right` has value `>= target`;
- `[left, right)` is still unknown.

## Classroom board: first value at least 6

```text
values = [1, 3, 6, 6, 9], target = 6

[left,right)  middle  value  decision
[0,5)            2      6    answer is at 2 or left -> right=2
[0,2)            1      3    too small             -> left=2

left == right == 2; first value >= 6 is index 2
```

We do not stop at equality because there might be another `6` farther left.

## Steps

1. Start with the whole half-open range `[0, n)`.
2. Inspect the middle value.
3. Discard the half that cannot contain the first valid index.
4. When `left == right`, return that boundary.

## First-principles derivation

Linear search removes one candidate per comparison. A sorted or monotone space
lets one comparison reject half of the remaining candidates.

The invariant keeps the answer inside one chosen interval; every update must
make that interval strictly smaller.

## Pattern recognition

Use binary search for sorted data or any yes/no condition that changes only
once from false to true (or true to false).

## Implementation

### C++

```cpp
int lowerBound(const std::vector<int>& values, int target) {
    int left = 0;
    int right = static_cast<int>(values.size());
    while (left < right) {
        const int middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left;
}
```

### Python

```python
def lower_bound(values: list[int], target: int) -> int:
    left, right = 0, len(values)
    while left < right:
        middle = left + (right - left) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left
```

### Java

```java
static int lowerBound(int[] values, int target) {
    int left = 0;
    int right = values.length;
    while (left < right) {
        int middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left;
}
```

## Why it works

Every comparison discards only indices that are proven too small or already
large enough, so the first valid position remains inside the unknown range.

## Complexity

Time is `O(log n)`, space is `O(1)`. Equality search succeeds exactly when the
returned index is in range and equals the target. Upper bound changes the
comparison to `values[middle] <= target`.

## Common mistakes

- Searching unsorted, non-monotone data.
- Mixing inclusive and exclusive `right` boundaries.
- Returning immediately on equality when the first/last occurrence is needed.
- Computing `(left + right) / 2` in a fixed-width type that can overflow.
