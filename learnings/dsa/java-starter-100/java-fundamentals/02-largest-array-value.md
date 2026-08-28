# 02. Find the Largest Array Value

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Return the largest value in a non-empty int[].

## Example

~~~text
Input: values = [7, 2, 9, 4]
Output: 9
~~~

## Simple idea

Start with the first value and replace it when a larger value appears.

## Java solution

~~~java
static int largest(int[] values) {
    int best = values[0];
    for (int value : values) best = Math.max(best, value);
    return best;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

