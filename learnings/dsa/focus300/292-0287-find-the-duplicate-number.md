# Focus300 292: LeetCode 287 - Find the Duplicate Number

**Source:** [LeetCode 287](https://leetcode.com/problems/find-the-duplicate-number/)  
**Difficulty:** Medium  
**Pattern:** cycle detection on implicit pointers

## Exact contract

Return the one duplicated value in an array where numbers map into index positions.

## First principles

The array defines a functional graph: each value points to another index. The duplicate creates a cycle entrance, which can be found with Floyd's algorithm.

## Cases that decide correctness

- The duplicate may appear many times.
- The array length is one greater than the value range.
- The solution should not modify the array.
- The same mapping that creates a cycle also identifies the duplicate value.

## Brute force

```python
def find_duplicate_brute(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
```

Count occurrences with a hash map.

## Better insight

Treat the values as next pointers and locate the cycle entry.

## Expert solution

```python
def find_duplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

Run tortoise and hare on the implicit graph, then reset one pointer to find the entry, which is the duplicate value.

**Complexity:** O(n) time and O(1) space.
