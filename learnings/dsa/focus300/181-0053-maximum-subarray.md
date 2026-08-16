# Focus300 181: LeetCode 53 - Maximum Subarray

**Source:** [LeetCode 53](https://leetcode.com/problems/maximum-subarray/)  
**Difficulty:** Medium  
**Pattern:** Kadane's prefix-state dynamic programming

## Exact contract

Given a nonempty integer array, return the largest sum of any nonempty
contiguous subarray. The source permits up to 100,000 elements.

## First principles

The best subarray ending at the current value either starts there or extends
the best subarray ending immediately before it. No other earlier information
affects that decision. A separate maximum records the best ending state seen
anywhere.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- All-negative input returns its largest element, not zero.
- The chosen subarray must be nonempty and contiguous.
- A negative running prefix is discarded before the next element.
- The best answer may end before the array does.
- Initialize from the first element rather than an artificial zero.

## Brute force: sum every subarray

```python
def maximum_subarray_sum_brute(numbers: list[int]) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 100_000:
        raise ValueError("numbers length must be between 1 and 100000")

    answer = numbers[0]
    for left in range(len(numbers)):
        total = 0
        for right in range(left, len(numbers)):
            total += numbers[right]
            answer = max(answer, total)
    return answer
```

This takes `O(n^2)` time and `O(1)` auxiliary space.

## Better approach: divide around the midpoint

The maximum lies wholly left, wholly right, or crosses the midpoint. Recursing
and scanning the crossing prefixes takes `O(n log n)` time and `O(log n)`
stack space. Kadane's state removes repeated scans.

## Expert solution: roll the best ending sum

```python
def maximum_subarray_sum(numbers: list[int]) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 100_000:
        raise ValueError("numbers length must be between 1 and 100000")

    best_ending = numbers[0]
    answer = numbers[0]
    for value in numbers[1:]:
        best_ending = max(value, best_ending + value)
        answer = max(answer, best_ending)
    return answer
```

`best_ending` is optimal among exactly the subarrays ending at the current
index. Taking the maximum of those exhaustive ending choices proves the result.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
