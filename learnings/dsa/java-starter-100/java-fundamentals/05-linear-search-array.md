# 05. Linear Search an Array

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Return the index of target, or -1 when it is absent.

## Example

~~~text
Input: values = [4, 9, 1], target = 9
Output: 1
~~~

## Simple idea

Check each index and stop at the first match.

## Java solution

~~~java
static int indexOf(int[] values, int target) {
    for (int index = 0; index < values.length; index++)
        if (values[index] == target) return index;
    return -1;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

