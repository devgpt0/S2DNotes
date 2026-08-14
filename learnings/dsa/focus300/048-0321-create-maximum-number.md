# Focus300 048: LeetCode 321 - Create Maximum Number

**Source:** [LeetCode 321](https://leetcode.com/problems/create-maximum-number/)  
**Difficulty:** Hard  
**Pattern:** monotonic subsequence selection and lexicographic merge

## Exact contract

Given two nonempty arrays of decimal digits and `k` from 1 through their total
length, create the lexicographically largest length-`k` digit array. Chosen
digits must preserve their relative order within each original array, but the
two chosen subsequences may be interleaved arbitrarily.

## First principles

Fix how many digits come from the first array. The best subsequence of a fixed
length is found by greedily dropping smaller digits while enough later digits
remain. The two best subsequences must then be merged by choosing the
lexicographically larger remaining suffix, not merely the larger next digit.

## Cases that decide correctness

- Every feasible split of `k` between the arrays must be considered.
- Equal leading digits require comparing later suffix digits.
- Zeros are ordinary digits and may lead the result.
- Relative order inside each input cannot change.
- One split may take zero digits from an array.

## Brute force: enumerate subsequences and interleavings

```python
from itertools import combinations


def create_maximum_number_brute(
    first: list[int], second: list[int], length: int
) -> list[int]:
    if (
        not first
        or not second
        or any(not 0 <= digit <= 9 for digit in first + second)
        or not 1 <= length <= len(first) + len(second)
    ):
        raise ValueError("invalid digit arrays or length")

    def subsequences(values: list[int], size: int) -> list[list[int]]:
        return [
            [values[index] for index in indices]
            for indices in combinations(range(len(values)), size)
        ]

    def interleavings(left: list[int], right: list[int]) -> list[list[int]]:
        answers: list[list[int]] = []

        def build(left_index: int, right_index: int, current: list[int]) -> None:
            if left_index == len(left) and right_index == len(right):
                answers.append(current.copy())
                return
            if left_index < len(left):
                current.append(left[left_index])
                build(left_index + 1, right_index, current)
                current.pop()
            if right_index < len(right):
                current.append(right[right_index])
                build(left_index, right_index + 1, current)
                current.pop()

        build(0, 0, [])
        return answers

    answer: list[int] = []
    minimum_first = max(0, length - len(second))
    maximum_first = min(length, len(first))
    for first_size in range(minimum_first, maximum_first + 1):
        for left in subsequences(first, first_size):
            for right in subsequences(second, length - first_size):
                answer = max(answer, *interleavings(left, right))
    return answer
```

This is exponential in both subsequence selection and interleaving.

## Better transition: optimize each fixed split independently

A decreasing stack produces the maximum fixed-length subsequence. During the
merge, compare remaining suffixes whenever the next digits tie; the larger
suffix must contribute the next digit in any maximum result.

## Expert solution: greedy selection plus suffix-aware merge

```python
def create_maximum_number(
    first: list[int], second: list[int], length: int
) -> list[int]:
    if (
        not first
        or not second
        or any(not 0 <= digit <= 9 for digit in first + second)
        or not 1 <= length <= len(first) + len(second)
    ):
        raise ValueError("invalid digit arrays or length")

    def maximum_subsequence(values: list[int], size: int) -> list[int]:
        drop = len(values) - size
        stack: list[int] = []
        for value in values:
            while drop and stack and stack[-1] < value:
                stack.pop()
                drop -= 1
            stack.append(value)
        return stack[:size]

    def suffix_greater(
        left: list[int], left_index: int, right: list[int], right_index: int
    ) -> bool:
        while (
            left_index < len(left)
            and right_index < len(right)
            and left[left_index] == right[right_index]
        ):
            left_index += 1
            right_index += 1
        return right_index == len(right) or (
            left_index < len(left) and left[left_index] > right[right_index]
        )

    def merge(left: list[int], right: list[int]) -> list[int]:
        result: list[int] = []
        left_index = 0
        right_index = 0
        while left_index < len(left) or right_index < len(right):
            if suffix_greater(left, left_index, right, right_index):
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        return result

    answer: list[int] = []
    minimum_first = max(0, length - len(second))
    maximum_first = min(length, len(first))
    for first_size in range(minimum_first, maximum_first + 1):
        candidate = merge(
            maximum_subsequence(first, first_size),
            maximum_subsequence(second, length - first_size),
        )
        answer = max(answer, candidate)
    return answer
```

For a fixed split, exchange arguments prove the stack subsequences are maximal.
At each merge position, choosing the greater remaining suffix gives the best
possible first differing digit. Maximizing across all feasible splits therefore
exhausts every valid source allocation.

**Complexity:** `O((m+n) * k^2)` worst-case time with direct suffix comparisons
and `O(m+n)` auxiliary space.
