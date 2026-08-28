# 78. Distinct and Sort a Stream

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return unique numbers in ascending order.

## Example

~~~text
Input: values=[4,1,4,2]
Output: [1,2,4]
~~~

## Simple idea

Compose distinct and sorted stages before the terminal operation.

## Java solution

~~~java
static List<Integer> uniqueSorted(List<Integer> values) {
    return values.stream().distinct().sorted().toList();
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

