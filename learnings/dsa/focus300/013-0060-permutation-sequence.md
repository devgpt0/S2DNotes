# Focus300 013: LeetCode 60 - Permutation Sequence

**Source:** [LeetCode 60](https://leetcode.com/problems/permutation-sequence/)  
**Difficulty:** Hard  
**Pattern:** factorial number system selection

## Exact contract

For `1 <= n <= 9`, consider the permutations of `1..n` in lexicographic order.
Given one-based `k` with `1 <= k <= n!`, return the `k`th permutation as a
string.

## First principles

Permutations with the same first digit form a block of `(n-1)!` entries. After
choosing the block containing `k`, remove its leading digit and repeat with the
offset inside that block. Converting `k-1` to factorial digits makes every
choice zero-based.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- `k` is one-based, so subtract one before division.
- `k = 1` returns increasing order.
- `k = n!` returns decreasing order.
- A selected digit is removed and cannot appear again.
- `n <= 9`, so concatenated decimal digits are unambiguous.

## Brute force: materialize all permutations

```python
from itertools import permutations
from math import factorial


def get_permutation_brute(size: int, position: int) -> str:
    if not 1 <= size <= 9 or not 1 <= position <= factorial(size):
        raise ValueError("position must lie in the permutation range")
    ordered = list(permutations(range(1, size + 1)))
    return "".join(map(str, ordered[position - 1]))
```

This takes `O(n! * n)` time and space.

## Better approach: advance one permutation at a time

```python
from math import factorial


def get_permutation_iterative(size: int, position: int) -> str:
    if not 1 <= size <= 9 or not 1 <= position <= factorial(size):
        raise ValueError("position must lie in the permutation range")

    values = list(range(1, size + 1))
    for _ in range(position - 1):
        pivot = size - 2
        while values[pivot] > values[pivot + 1]:
            pivot -= 1
        successor = size - 1
        while values[successor] < values[pivot]:
            successor -= 1
        values[pivot], values[successor] = values[successor], values[pivot]
        values[pivot + 1 :] = reversed(values[pivot + 1 :])
    return "".join(map(str, values))
```

This uses `O(n)` space but may still perform `k-1` transitions.

## Expert solution: select factorial blocks directly

```python
from math import factorial


def get_permutation(size: int, position: int) -> str:
    if not 1 <= size <= 9 or not 1 <= position <= factorial(size):
        raise ValueError("position must lie in the permutation range")

    available = list(range(1, size + 1))
    offset = position - 1
    answer: list[str] = []
    for remaining in range(size, 0, -1):
        block_size = factorial(remaining - 1)
        block, offset = divmod(offset, block_size)
        answer.append(str(available.pop(block)))
    return "".join(answer)
```

At each position, `block` identifies the leading digit of the only factorial
block containing the requested offset. `divmod` leaves the exact offset within
that block, so induction over positions yields the requested permutation.

**Complexity:** `O(n^2)` time because list deletion shifts elements and `O(n)`
space.
