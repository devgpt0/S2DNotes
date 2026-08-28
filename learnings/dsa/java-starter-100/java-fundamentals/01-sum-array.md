# 01. Sum an Array

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Given an int[], return the sum of all values.

## Example

~~~text
Input: values = [2, 4, 6]
Output: 12
~~~

## Simple idea

Keep a running total and visit every element once.

## Java solution

~~~java
static int sum(int[] values) {
    int total = 0;
    for (int value : values) total += value;
    return total;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

