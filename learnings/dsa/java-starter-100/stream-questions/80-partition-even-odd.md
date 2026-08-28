# 80. Partition Even and Odd Values

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Split integers into even and odd lists.

## Example

~~~text
Input: values=[1,2,4,5]
Output: {false=[1,5], true=[2,4]}
~~~

## Simple idea

partitioningBy creates boolean groups from a predicate.

## Java solution

~~~java
static Map<Boolean, List<Integer>> evenOdd(List<Integer> values) {
    return values.stream().collect(Collectors.partitioningBy(value -> value % 2 == 0));
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

