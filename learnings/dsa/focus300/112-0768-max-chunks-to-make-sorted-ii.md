# Focus300 112: LeetCode 768 - Max Chunks To Make Sorted II

**Source:** [LeetCode 768](https://leetcode.com/problems/max-chunks-to-make-sorted-ii/)  
**Difficulty:** Hard  
**Pattern:** valid boundaries from prefix maxima and suffix minima

## Exact contract

Split a nonempty integer array into the maximum number of contiguous chunks so
that sorting every chunk independently and concatenating them produces the
fully sorted array. Duplicates are allowed. Return the number of chunks; the
source length is at most 2,000.

## First principles

A cut after index `i` is valid exactly when every value on its left is no
greater than every value on its right. Otherwise at least one cross-boundary
inversion remains after sorting the chunks. This condition is summarized by
`max(array[:i+1]) <= min(array[i+1:])`.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- A nonempty array always permits one whole-array chunk.
- Equal values may lie on both sides of a valid boundary.
- Using `<` instead of `<=` incorrectly rejects duplicate boundaries.
- A locally increasing pair does not prove that the entire prefix can be cut.
- Each returned boundary must be independently valid against all later values.

## Brute force: enumerate every set of cuts

```python
def maximum_sorted_chunks_brute(values: list[int]) -> int:
    if type(values) is not list or any(type(value) is not int for value in values):
        raise TypeError("values must be a list of integers")
    if not 1 <= len(values) <= 2_000:
        raise ValueError("values length must be between 1 and 2000")

    target = sorted(values)
    answer = 1
    for cut_mask in range(1 << (len(values) - 1)):
        concatenated: list[int] = []
        chunk_start = 0
        chunk_count = 1
        for index in range(len(values) - 1):
            if cut_mask & (1 << index):
                concatenated.extend(sorted(values[chunk_start : index + 1]))
                chunk_start = index + 1
                chunk_count += 1
        concatenated.extend(sorted(values[chunk_start:]))
        if concatenated == target:
            answer = max(answer, chunk_count)
    return answer
```

There are `2^(n-1)` cut sets, and each requires `O(n log n)` sorting work.

## Better approach: compare prefix multisets with the sorted target

```python
from collections import Counter


def maximum_sorted_chunks_counter(values: list[int]) -> int:
    if type(values) is not list or any(type(value) is not int for value in values):
        raise TypeError("values must be a list of integers")
    if not 1 <= len(values) <= 2_000:
        raise ValueError("values length must be between 1 and 2000")

    difference: Counter[int] = Counter()
    chunks = 0
    for original, expected in zip(values, sorted(values), strict=True):
        difference[original] += 1
        if difference[original] == 0:
            del difference[original]
        difference[expected] -= 1
        if difference[expected] == 0:
            del difference[expected]
        if not difference:
            chunks += 1
    return chunks
```

An empty multiset difference proves that the current original prefix contains
exactly the values required by the sorted prefix. This takes `O(n log n)` time
and `O(n)` space.

## Expert solution: test every boundary in constant time

```python
def maximum_sorted_chunks(values: list[int]) -> int:
    if type(values) is not list or any(type(value) is not int for value in values):
        raise TypeError("values must be a list of integers")
    if not 1 <= len(values) <= 2_000:
        raise ValueError("values length must be between 1 and 2000")

    suffix_minimum = [0] * len(values)
    suffix_minimum[-1] = values[-1]
    for index in range(len(values) - 2, -1, -1):
        suffix_minimum[index] = min(values[index], suffix_minimum[index + 1])

    chunks = 1
    prefix_maximum = values[0]
    for index in range(len(values) - 1):
        prefix_maximum = max(prefix_maximum, values[index])
        if prefix_maximum <= suffix_minimum[index + 1]:
            chunks += 1
    return chunks
```

The precomputed suffix minima and running prefix maximum test the necessary
and sufficient cross-boundary condition once per possible cut.

**Complexity:** `O(n)` time and `O(n)` space.
