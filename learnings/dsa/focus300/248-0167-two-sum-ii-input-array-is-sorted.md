# Focus300 248: LeetCode 167 - Two Sum II - Input Array Is Sorted

**Source:** [LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)  
**Difficulty:** Medium  
**Pattern:** two-pointer search on a sorted array

## Exact contract

Return the one-based indices of two numbers in the sorted array whose sum equals the target.

## First principles

The array is sorted, so the sum moves predictably when either pointer changes. That makes a two-pointer sweep enough to pin down the unique pair.


## Classroom board: improve a pair-sum solution

```text
    Find how many index pairs in [1, 5, 3, 3] sum to 6.

    Brute force checks all 6 pairs:
    (1,5) yes  (1,3) no  (1,3) no
    (5,3) no   (5,3) no  (3,3) yes
    answer = 2

    Repeated work: comparing many pairs.
    Useful structure: after sorting, a small sum needs a larger left value;
    a large sum needs a smaller right value.

    sorted: [1, 3, 3, 5]
             L        R  -> 1 + 5 = 6, count 1
                L  R     -> 3 + 3 = 6, count 2
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

- Exactly one pair is guaranteed by the usual problem contract.
- The answer is one-based, not zero-based.
- Moving the left pointer increases the sum; moving the right pointer decreases it.
- Duplicates are fine as long as the index pair is correct.

## Brute force

```python
def two_sum_brute(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
```

Try every pair of indices.

## Better insight

Start at both ends and move inward according to the current sum.

## Expert solution

```python
def two_sum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
```

Use one pointer at the left and one at the right, and adjust the side that makes the sum move toward the target.

**Complexity:** O(n) time and O(1) space.
