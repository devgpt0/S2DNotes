# Focus300 160: LeetCode 16 - 3Sum Closest

**Source:** [LeetCode 16](https://leetcode.com/problems/3sum-closest/)  
**Difficulty:** Medium  
**Pattern:** sorted two pointers with a best-distance invariant

## Exact contract

Choose three distinct indices whose values have the sum closest to `target` and
return that sum. The source guarantees exactly one closest sum.

## First principles

Sort a copy and fix one value. For the two remaining pointers, a sum below the
target can become closer only by increasing the left value; a sum above the
target can become closer only by decreasing the right value. Record the best
distance before that forced move.

## Cases that decide correctness

- An exact target match can return immediately.
- Negative values and targets follow the same pointer rule.
- Three elements have one forced sum.
- Distinct indices may hold equal values.
- Sorting must not mutate the input list.

## Brute force: evaluate every index triple

```python
def three_sum_closest_brute(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or not 3 <= len(numbers) <= 500:
        raise ValueError("numbers length must be between 3 and 500")
    if any(type(value) is not int or not -1_000 <= value <= 1_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    best_sum = numbers[0] + numbers[1] + numbers[2]
    for first in range(len(numbers)):
        for second in range(first + 1, len(numbers)):
            for third in range(second + 1, len(numbers)):
                total = numbers[first] + numbers[second] + numbers[third]
                distance = abs(total - target)
                best_distance = abs(best_sum - target)
                if (
                    distance < best_distance
                    or distance == best_distance
                    and total < best_sum
                ):
                    best_sum = total
    return best_sum
```

This checks `O(n^3)` triples and uses `O(1)` auxiliary space.

## Better insight: sorted pair sums move monotonically

For a fixed first value, only one pointer direction can improve a non-exact
sum. That reduces every inner search from quadratic to linear.

## Expert solution: update the closest sum during a two-pointer scan

```python
def three_sum_closest(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or not 3 <= len(numbers) <= 500:
        raise ValueError("numbers length must be between 3 and 500")
    if any(type(value) is not int or not -1_000 <= value <= 1_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    ordered = sorted(numbers)
    best_sum = ordered[0] + ordered[1] + ordered[2]
    for first in range(len(ordered) - 2):
        left = first + 1
        right = len(ordered) - 1
        while left < right:
            total = ordered[first] + ordered[left] + ordered[right]
            distance = abs(total - target)
            best_distance = abs(best_sum - target)
            if (
                distance < best_distance
                or distance == best_distance
                and total < best_sum
            ):
                best_sum = total
            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                return target
    return best_sum
```

The best-distance invariant retains the closest visited sum, while monotonic
pointer moves ensure no skipped pair can improve it.

**Complexity:** `O(n^2)` time and `O(n)` space for the sorted copy.
