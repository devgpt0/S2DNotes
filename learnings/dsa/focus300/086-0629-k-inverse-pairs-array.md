# Focus300 086: LeetCode 629 - K Inverse Pairs Array

**Source:** [LeetCode 629](https://leetcode.com/problems/k-inverse-pairs-array/)  
**Difficulty:** Hard  
**Pattern:** dynamic programming with a sliding prefix sum

## Exact contract

For `1 <= n <= 1000` and `0 <= k <= 1000`, count permutations of
`[1, 2, ..., n]` containing exactly `k` inverse pairs. An inverse pair is
`i < j` with `permutation[i] > permutation[j]`. Return the count modulo
`1_000_000_007`.

## First principles

Insert the new largest value `size` into a permutation of `size - 1`. Placing
it zero, one, ..., `size - 1` positions from the right adds exactly that many
inversions. Therefore the new count for `j` is a window sum of the previous
row from `j - size + 1` through `j`.

## Cases that decide correctness

- Exactly one sorted permutation has zero inversions.
- No permutation exceeds `n * (n - 1) / 2` inversions.
- Each DP layer may add at most `size - 1` inversions.
- Sliding-window subtraction must be reduced modulo the source modulus.
- Boolean inputs are rejected instead of being accepted as integers.

## Brute force: enumerate every permutation

```python
from itertools import permutations


MODULO = 1_000_000_007


def inverse_pairs_count_brute(size: int, target: int) -> int:
    if type(size) is not int or type(target) is not int:
        raise TypeError("size and target must be integers")
    if not 1 <= size <= 1000 or not 0 <= target <= 1000:
        raise ValueError("size must be 1..1000 and target must be 0..1000")

    answer = 0
    for permutation in permutations(range(1, size + 1)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        answer += inversions == target
    return answer % MODULO
```

This takes `O(n! * n^2)` time and `O(n)` permutation space.

## Better approach: sum every insertion choice

```python
MODULO = 1_000_000_007


def inverse_pairs_count_cubic(size: int, target: int) -> int:
    if type(size) is not int or type(target) is not int:
        raise TypeError("size and target must be integers")
    if not 1 <= size <= 1000 or not 0 <= target <= 1000:
        raise ValueError("size must be 1..1000 and target must be 0..1000")
    if target > size * (size - 1) // 2:
        return 0

    previous = [0] * (target + 1)
    previous[0] = 1
    for current_size in range(1, size + 1):
        current = [0] * (target + 1)
        for inversions in range(target + 1):
            current[inversions] = (
                sum(
                    previous[inversions - added]
                    for added in range(min(inversions, current_size - 1) + 1)
                )
                % MODULO
            )
        previous = current
    return previous[target]
```

This direct recurrence is `O(n^2 k)` time and `O(k)` space.

## Expert solution: maintain the insertion window

```python
MODULO = 1_000_000_007


def inverse_pairs_count(size: int, target: int) -> int:
    if type(size) is not int or type(target) is not int:
        raise TypeError("size and target must be integers")
    if not 1 <= size <= 1000 or not 0 <= target <= 1000:
        raise ValueError("size must be 1..1000 and target must be 0..1000")
    if target > size * (size - 1) // 2:
        return 0

    previous = [0] * (target + 1)
    previous[0] = 1
    for current_size in range(1, size + 1):
        current = [0] * (target + 1)
        window = 0
        for inversions in range(target + 1):
            window += previous[inversions]
            if inversions >= current_size:
                window -= previous[inversions - current_size]
            current[inversions] = window % MODULO
        previous = current
    return previous[target]
```

The running window is exactly the sum over all legal positions of the new
largest value. Each DP cell is therefore computed in constant time.

**Complexity:** `O(nk)` time and `O(k)` space.
