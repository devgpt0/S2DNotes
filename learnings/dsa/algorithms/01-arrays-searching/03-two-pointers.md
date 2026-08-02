# Two Pointers

## Idea

Two pointers replace repeated scanning when movement is monotone. Typical
forms are opposite ends of a sorted array and a slow/fast pair.

## Visual model: pair sum in a sorted array

```text
[1, 2, 4, 7, 11], target 9
 L           R       1 + 11 too large -> move R left
 L        R          1 + 7 too small  -> move L right
    L     R          2 + 7 == 9
```

Moving `left` right is safe because it is the only way to increase the sum;
moving `right` left is the only way to decrease it.

## Classroom board: move only the useful pointer

```text
values = [1, 2, 4, 7, 11], target = 9

L=1, R=11 -> sum 12 is too large -> move R left
L=1, R=7  -> sum  8 is too small -> move L right
L=2, R=7  -> sum  9 -> found
```

Why can we discard `11` in the first step? Pairing it with any value between
the pointers is at least `1 + 11 = 12`, already too large.

## Steps

1. Put one pointer at each end of the sorted array.
2. Compare their sum with the target.
3. Move `left` to increase the sum or `right` to decrease it.
4. Stop when a pair is found or the pointers meet.

## First-principles derivation

Brute force tries every pair. Sorting creates direction: if a sum is too small,
only moving the smaller side can increase it; if too large, move the larger
side.

The invariant is that every skipped pair is proven unable to satisfy the
target.

## Pattern recognition

Look for sorted data, a pair/range condition, and pointer movements that can be
proved safe without moving backward.

## Implementation

### C++

```cpp
std::pair<int, int> findPairSum(const std::vector<int>& values, int target) {
    int left = 0;
    int right = static_cast<int>(values.size()) - 1;
    while (left < right) {
        const long long sum = static_cast<long long>(values[left]) + values[right];
        if (sum == target) {
            return {left, right};
        }
        if (sum < target) {
            ++left;
        } else {
            --right;
        }
    }
    return {-1, -1};
}
```

### Python

```python
def find_pair_sum(values: list[int], target: int) -> tuple[int, int]:
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return -1, -1
```

### Java

```java
static int[] findPairSum(int[] values, int target) {
    int left = 0;
    int right = values.length - 1;
    while (left < right) {
        long sum = (long) values[left] + values[right];
        if (sum == target) {
            return new int[] {left, right};
        }
        if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return new int[] {-1, -1};
}
```

## Why it works

If the sum is too small, the current smallest value cannot work with any
remaining right value. The symmetric argument holds when the sum is too large.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Recognition clues

- sorted input and a pair/triplet condition;
- remove duplicates in place;
- compare from both ends;
- merge two sorted sequences;
- one pointer advances while another never retreats.

## Common mistakes

- Using opposite pointers before sorting.
- Moving the wrong pointer after comparing the sum.
- Forgetting that sorting loses original indices unless they are stored.
- Applying the pattern when movement is not monotone.
