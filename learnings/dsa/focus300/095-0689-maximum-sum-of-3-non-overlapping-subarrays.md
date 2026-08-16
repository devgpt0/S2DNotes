# Focus300 095: LeetCode 689 - Maximum Sum of 3 Non-Overlapping Subarrays

**Source:** [LeetCode 689](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/)  
**Difficulty:** Hard  
**Pattern:** sliding-window sums with prefix and suffix argmax

## Exact contract

Given a positive integer array and a window length `k`, choose exactly three
pairwise non-overlapping length-`k` subarrays. Return their starting indices in
increasing order, maximizing the total sum. Break ties by the lexicographically
smallest index triple.

## First principles

Fixing the middle window separates the remaining choices: the best left window
must end before it, and the best right window must start after it. Prefix and
suffix argmax arrays answer those independent choices in constant time.

Tie direction is part of the algorithm. The left scan keeps the earlier index;
the right scan, moving right-to-left, replaces on equality to keep the earlier
index.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- Exactly `3*k` numbers forces starts `[0, k, 2*k]`.
- Windows may touch at endpoints but may not share an element.
- Equal sums require the lexicographically smallest triple.
- Positive values make every complete window sum positive.
- The input array must not be mutated.

## Brute force: enumerate every legal triple of starts

```python
def maximum_three_windows_brute(numbers: list[int], window_size: int) -> list[int]:
    if type(numbers) is not list or not 3 <= len(numbers) <= 20_000:
        raise ValueError("numbers length must be between 3 and 20,000")
    if any(type(value) is not int or not 1 <= value <= 65_535 for value in numbers):
        raise ValueError("numbers must contain positive source-range integers")
    if type(window_size) is not int or not 1 <= window_size <= len(numbers) // 3:
        raise ValueError("window_size must allow three complete windows")

    window_sums = [sum(numbers[:window_size])]
    for start in range(1, len(numbers) - window_size + 1):
        window_sums.append(
            window_sums[-1] - numbers[start - 1] + numbers[start + window_size - 1]
        )

    best_total = -1
    best_indices = [-1, -1, -1]
    for first in range(len(window_sums)):
        for second in range(first + window_size, len(window_sums)):
            for third in range(second + window_size, len(window_sums)):
                total = window_sums[first] + window_sums[second] + window_sums[third]
                if total > best_total:
                    best_total = total
                    best_indices = [first, second, third]
    return best_indices
```

Natural loop order visits triples lexicographically, so retaining the first
maximum handles ties. The running time is `O(n^3)` after window sums.

## Better insight: condition on the middle window

For every middle start, one prefix lookup and one suffix lookup produce the
best compatible triple. Only `O(n)` middle starts exist.

## Expert solution: prefix/suffix best windows

```python
def maximum_three_windows(numbers: list[int], window_size: int) -> list[int]:
    if type(numbers) is not list or not 3 <= len(numbers) <= 20_000:
        raise ValueError("numbers length must be between 3 and 20,000")
    if any(type(value) is not int or not 1 <= value <= 65_535 for value in numbers):
        raise ValueError("numbers must contain positive source-range integers")
    if type(window_size) is not int or not 1 <= window_size <= len(numbers) // 3:
        raise ValueError("window_size must allow three complete windows")

    window_sums = [sum(numbers[:window_size])]
    for start in range(1, len(numbers) - window_size + 1):
        window_sums.append(
            window_sums[-1] - numbers[start - 1] + numbers[start + window_size - 1]
        )

    window_count = len(window_sums)
    best_left = [0] * window_count
    for index in range(1, window_count):
        previous = best_left[index - 1]
        best_left[index] = (
            index if window_sums[index] > window_sums[previous] else previous
        )

    best_right = [0] * window_count
    best_right[-1] = window_count - 1
    for index in range(window_count - 2, -1, -1):
        following = best_right[index + 1]
        best_right[index] = (
            index if window_sums[index] >= window_sums[following] else following
        )

    best_total = -1
    answer = [-1, -1, -1]
    for middle in range(window_size, window_count - window_size):
        left = best_left[middle - window_size]
        right = best_right[middle + window_size]
        total = window_sums[left] + window_sums[middle] + window_sums[right]
        if total > best_total:
            best_total = total
            answer = [left, middle, right]
    return answer
```

For each middle window the two lookup arrays supply optimal compatible sides;
their tie rules and the increasing middle scan preserve lexicographic order.

**Complexity:** `O(n)` time and `O(n)` space.
