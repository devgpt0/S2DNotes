# 04. Count Even Array Values

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Count how many values in an int[] are even.

## Example

~~~text
Input: values = [3, 8, 10, 11]
Output: 2
~~~

## Simple idea

A value is even when value % 2 == 0.

## Java solution

~~~java
static int countEven(int[] values) {
    int count = 0;
    for (int value : values) if (value % 2 == 0) count++;
    return count;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

