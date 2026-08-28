# 76. Filter and Sum with Streams

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Sum the positive values in a list.

## Example

~~~text
Input: values=[-2,4,0,7]
Output: 11
~~~

## Simple idea

Filter first, then use primitive mapToInt and sum.

## Java solution

~~~java
static int positiveSum(List<Integer> values) {
    return values.stream().filter(value -> value > 0).mapToInt(Integer::intValue).sum();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1) result space`

Try to write the solution yourself before reading the code.

