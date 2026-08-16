# Focus300 047: LeetCode 315 - Count of Smaller Numbers After Self

**Source:** [LeetCode 315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)  
**Difficulty:** Hard  
**Pattern:** right-to-left Fenwick tree with coordinate compression

## Exact contract

For every integer in a nonempty list, return how many later elements are
strictly smaller than it. Equal later values do not count.

## First principles

Scan from right to left so the data structure contains exactly the later
values. After compressing values to sorted ranks, a prefix-frequency query up
to `rank - 1` counts all strictly smaller values; then insert the current rank.


## Classroom board: walk the tree once

```text
choose the root condition, then push the relevant subtree state down as
you recurse or iterate.
```



## Step-by-step transformation

1. Traverse the structure and keep the pointer, node, or subtree state that matters.
2. Rewire links or combine child results without losing the part of the structure you still need.
3. Carry the surviving state forward to the next node or subtree.
4. Return the rebuilt structure, node value, or accumulated traversal result.

These notes work by preserving the structure while changing just the links or the returned subtree results that lead to the final answer.


## Diagram: walk and reconnect pointers

```text

            original nodes
                |
                v
            read or split the structure
                |
                v
            reconnect links or combine child results
                |
                v
            rebuilt list / tree / value
```

The algorithm walks the structure, keeps only the needed pointers or subtree results, and returns the rebuilt output.

## Cases that decide correctness

- Equal values are not smaller.
- Negative and repeated values are valid.
- The final element always receives zero.
- Compression must preserve strict numeric order.
- Query before insertion prevents counting the current element.

## Brute force: compare every later pair

```python
def count_smaller_brute(numbers: list[int]) -> list[int]:
    if not numbers:
        raise ValueError("numbers must be nonempty")
    return [
        sum(later < number for later in numbers[index + 1 :])
        for index, number in enumerate(numbers)
    ]
```

This takes `O(n^2)` time and `O(n)` output space.

## Better approach: count crossings during merge sort

```python
def count_smaller_merge_sort(numbers: list[int]) -> list[int]:
    if not numbers:
        raise ValueError("numbers must be nonempty")

    indices = list(range(len(numbers)))
    answers = [0] * len(numbers)

    def sort(left: int, right: int) -> None:
        if right - left <= 1:
            return
        middle = (left + right) // 2
        sort(left, middle)
        sort(middle, right)
        first = left
        second = middle
        moved_from_right = 0
        merged: list[int] = []
        while first < middle and second < right:
            if numbers[indices[second]] < numbers[indices[first]]:
                merged.append(indices[second])
                second += 1
                moved_from_right += 1
            else:
                answers[indices[first]] += moved_from_right
                merged.append(indices[first])
                first += 1
        while first < middle:
            answers[indices[first]] += moved_from_right
            merged.append(indices[first])
            first += 1
        merged.extend(indices[second:right])
        indices[left:right] = merged

    sort(0, len(numbers))
    return answers
```

A right-half value crossing before a left-half value is exactly one later,
strictly smaller element.

## Expert solution: compressed Fenwick frequencies

```python
from bisect import bisect_left


def count_smaller(numbers: list[int]) -> list[int]:
    if not numbers:
        raise ValueError("numbers must be nonempty")

    coordinates = sorted(set(numbers))
    tree = [0] * (len(coordinates) + 1)

    def add(index: int) -> None:
        index += 1
        while index < len(tree):
            tree[index] += 1
            index += index & -index

    def prefix(length: int) -> int:
        answer = 0
        while length:
            answer += tree[length]
            length -= length & -length
        return answer

    answers: list[int] = []
    for number in reversed(numbers):
        rank = bisect_left(coordinates, number)
        answers.append(prefix(rank))
        add(rank)
    answers.reverse()
    return answers
```

The tree stores frequencies of exactly the processed suffix. `prefix(rank)`
excludes the current value's rank and therefore counts precisely the smaller
suffix values.

**Complexity:** `O(n log n)` time and `O(n)` space.
