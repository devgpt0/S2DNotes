# Focus300 278: LeetCode 229 - Majority Element II

**Source:** [LeetCode 229](https://leetcode.com/problems/majority-element-ii/)  
**Difficulty:** Medium  
**Pattern:** generalized Boyer-Moore voting

## Exact contract

Return every value that appears more than `n/3` times.

## First principles

At most two values can exceed the `n/3` threshold. A pair of candidate slots with vote cancellation is enough to retain those possible majorities.

## Cases that decide correctness

- There can be zero, one, or two valid answers.
- The candidates from the voting pass still need verification.
- Values that are not majorities may temporarily occupy candidate slots.
- The final answer must be filtered by exact counts.

## Brute force

```python
from collections import Counter

def majority_element_brute(nums):
    return [num for num, count in Counter(nums).items() if count > len(nums) // 3]
```

Count every value with a hash map.

## Better insight

Use two candidate counters to eliminate non-majority values in one pass.

## Expert solution

```python
def majority_element(nums):
    cand1 = cand2 = None
    cnt1 = cnt2 = 0
    for num in nums:
        if num == cand1:
            cnt1 += 1
        elif num == cand2:
            cnt2 += 1
        elif cnt1 == 0:
            cand1, cnt1 = num, 1
        elif cnt2 == 0:
            cand2, cnt2 = num, 1
        else:
            cnt1 -= 1
            cnt2 -= 1
    result = []
    for cand in (cand1, cand2):
        if cand is not None and nums.count(cand) > len(nums) // 3:
            result.append(cand)
    return result
```

Run vote cancellation to find the two survivors, then count them again to confirm which ones exceed the threshold.

**Complexity:** O(n) time and O(1) space.
