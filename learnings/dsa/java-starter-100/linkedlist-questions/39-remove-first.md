# 39. Remove the First Matching LinkedList Value

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Remove only the first occurrence of target.

## Example

~~~text
Input: values = [2, 4, 2, 5], target = 2
Output: [4, 2, 5]
~~~

## Simple idea

Use the operation named for the required behavior.

## Java solution

~~~java
static boolean removeFirst(LinkedList<Integer> values, int target) {
    return values.removeFirstOccurrence(target);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

