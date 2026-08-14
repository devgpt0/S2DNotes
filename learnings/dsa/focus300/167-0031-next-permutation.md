# Focus300 167: LeetCode 31 - Next Permutation

**Source:** [LeetCode 31](https://leetcode.com/problems/next-permutation/)  
**Difficulty:** Medium  
**Pattern:** rightmost ascent, minimal successor, reversed suffix

## Exact contract

Transform an integer list in place into the lexicographically next greater
permutation of the same multiset. If no greater permutation exists, transform
it into the lexicographically smallest order. Use only constant auxiliary space.

## First principles

The longest nonincreasing suffix is already its greatest arrangement. The first
element before it is the rightmost pivot that can increase. Swap that pivot with
the smallest suffix value greater than it—the rightmost such value in the sorted-
descending suffix—then reverse the suffix to make the remaining arrangement as
small as possible.

## Cases that decide correctness

- A fully nonincreasing list wraps to ascending order.
- Duplicate values require a strictly greater successor.
- A one-element list is unchanged.
- The transformation must mutate the original list.
- Reversing, not sorting, the nonincreasing suffix gives constant extra space.

## Brute force: enumerate and sort every distinct permutation

```python
from itertools import permutations


def next_permutation_brute(numbers: list[int]) -> None:
    if type(numbers) is not list or not 1 <= len(numbers) <= 100:
        raise ValueError("numbers length must be between 1 and 100")
    if any(type(value) is not int or not 0 <= value <= 100 for value in numbers):
        raise ValueError("numbers must be integers from 0 through 100")

    arrangements = sorted(set(permutations(numbers)))
    current_index = arrangements.index(tuple(numbers))
    numbers[:] = arrangements[(current_index + 1) % len(arrangements)]
```

This is factorial in length and exists only as a specification baseline.

## Better insight: preserve the longest possible prefix

The next permutation must change the rightmost position that can increase. Any
earlier change would be lexicographically larger than necessary.

## Expert solution: pivot, successor, suffix reversal

```python
def next_permutation(numbers: list[int]) -> None:
    if type(numbers) is not list or not 1 <= len(numbers) <= 100:
        raise ValueError("numbers length must be between 1 and 100")
    if any(type(value) is not int or not 0 <= value <= 100 for value in numbers):
        raise ValueError("numbers must be integers from 0 through 100")

    pivot = len(numbers) - 2
    while pivot >= 0 and numbers[pivot] >= numbers[pivot + 1]:
        pivot -= 1
    if pivot >= 0:
        successor = len(numbers) - 1
        while numbers[successor] <= numbers[pivot]:
            successor -= 1
        numbers[pivot], numbers[successor] = numbers[successor], numbers[pivot]

    left = pivot + 1
    right = len(numbers) - 1
    while left < right:
        numbers[left], numbers[right] = numbers[right], numbers[left]
        left += 1
        right -= 1
```

The pivot swap makes the smallest possible prefix increase, and the suffix
reversal supplies the smallest completion for that prefix.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
