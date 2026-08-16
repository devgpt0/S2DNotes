# Focus300 122: LeetCode 805 - Split Array With Same Average

**Source:** [LeetCode 805](https://leetcode.com/problems/split-array-with-same-average/)  
**Difficulty:** Hard  
**Pattern:** zero-sum transformation with meet-in-the-middle

## Exact contract

Given `1..30` nonnegative integers, decide whether they can be partitioned into
two nonempty groups with equal arithmetic mean. Elements are distinguished by
index even when values repeat.

## First principles

For total sum `S`, length `n`, subset sum `s`, and subset size `k`, equal means
are equivalent to `s*n = S*k`. Transform every value `x` into `x*n - S`; a
nonempty proper subset has the required mean exactly when its transformed sum
is zero.

Splitting the transformed array in half reduces subset enumeration from `2^n`
to about `2^(n/2)` states per side.


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

- A one-element array cannot be split into two nonempty groups.
- The chosen subset must not be the full array.
- Duplicate values still represent separate selectable indices.
- A feasible size must satisfy `(S*k) % n == 0`.
- Zero values and an all-equal array are valid inputs.

## Brute force: enumerate subsets by size

```python
from itertools import combinations


def split_same_average_brute(numbers: list[int]) -> bool:
    if type(numbers) is not list or not 1 <= len(numbers) <= 30:
        raise ValueError("numbers length must be between 1 and 30")
    if any(type(value) is not int or not 0 <= value <= 10_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")

    length = len(numbers)
    total = sum(numbers)
    for subset_size in range(1, length // 2 + 1):
        if total * subset_size % length != 0:
            continue
        target = total * subset_size // length
        if any(sum(values) == target for values in combinations(numbers, subset_size)):
            return True
    return False
```

Complement symmetry limits sizes to `n//2`, but the search remains exponential.

## Better insight: transform average equality into zero-sum selection

Enumerate all subset sums in each half. A solution is a zero-sum subset within
one half or two nonempty half-subsets whose sums cancel. The sole forbidden
combination is taking both halves in full.

## Expert solution: meet-in-the-middle transformed sums

```python
def split_same_average(numbers: list[int]) -> bool:
    if type(numbers) is not list or not 1 <= len(numbers) <= 30:
        raise ValueError("numbers length must be between 1 and 30")
    if any(type(value) is not int or not 0 <= value <= 10_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")

    length = len(numbers)
    if length == 1:
        return False
    total = sum(numbers)
    if not any(total * size % length == 0 for size in range(1, length // 2 + 1)):
        return False

    transformed = [value * length - total for value in numbers]
    middle = length // 2
    left = transformed[:middle]
    right = transformed[middle:]

    left_sums: set[int] = set()
    proper_left_sums: set[int] = set()
    full_left_mask = (1 << len(left)) - 1
    for mask in range(1, full_left_mask + 1):
        subset_sum = sum(left[index] for index in range(len(left)) if mask >> index & 1)
        if subset_sum == 0:
            return True
        left_sums.add(subset_sum)
        if mask != full_left_mask:
            proper_left_sums.add(subset_sum)

    full_right_mask = (1 << len(right)) - 1
    for mask in range(1, full_right_mask + 1):
        subset_sum = sum(
            right[index] for index in range(len(right)) if mask >> index & 1
        )
        if subset_sum == 0:
            return True
        allowed_left_sums = proper_left_sums if mask == full_right_mask else left_sums
        if -subset_sum in allowed_left_sums:
            return True
    return False
```

Every nonempty proper subset has a unique pair of half-masks, and the full/full
exception prevents accepting the entire array's always-zero transformed sum.

**Complexity:** `O(n * 2^(n/2))` time and `O(2^(n/2))` space.
