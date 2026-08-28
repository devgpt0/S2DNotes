# 99. Binary Search a Sorted List

**What you learn:** Java core java APIs and problem solving.

## Problem

Return target's index, or a negative value when absent.

## Example

~~~text
Input: values=[1,3,5,7], target=5
Output: 2
~~~

## Simple idea

Binary search repeatedly halves the sorted range.

## Java solution

~~~java
static int findSorted(List<Integer> values, int target) {
    return Collections.binarySearch(values, target);
}
~~~

## Complexity

- Time: `O(log n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

