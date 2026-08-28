# 06. Sort an Array

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Sort an int[] in ascending order.

## Example

~~~text
Input: values = [5, 1, 4, 2]
Output: [1, 2, 4, 5]
~~~

## Simple idea

Arrays.sort provides an in-place sort for primitive arrays.

## Java solution

~~~java
static int[] sorted(int[] values) {
    Arrays.sort(values);
    return values;
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(log n) typical stack space`

Try to write the solution yourself before reading the code.

