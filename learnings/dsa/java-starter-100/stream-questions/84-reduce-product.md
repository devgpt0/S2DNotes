# 84. Multiply Values with Reduce

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return the product of all values.

## Example

~~~text
Input: values=[2,3,4]
Output: 24
~~~

## Simple idea

The identity 1 makes an empty list's product one.

## Java solution

~~~java
static int product(List<Integer> values) {
    return values.stream().reduce(1, (left, right) -> left * right);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

