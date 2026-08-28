# 22. Sum an ArrayList

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return the sum of all values in a list.

## Example

~~~text
Input: values = [3, 4, 5]
Output: 12
~~~

## Simple idea

The enhanced loop unboxes each Integer for arithmetic.

## Java solution

~~~java
static int sum(List<Integer> values) {
    int total = 0;
    for (int value : values) total += value;
    return total;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

