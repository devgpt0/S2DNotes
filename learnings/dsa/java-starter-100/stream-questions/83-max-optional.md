# 83. Find a Maximum with Streams

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return the largest value without throwing on an empty list.

## Example

~~~text
Input: values=[3,9,4]
Output: OptionalInt[9]
~~~

## Simple idea

A stream maximum is absent for an empty stream.

## Java solution

~~~java
static OptionalInt maximum(List<Integer> values) {
    return values.stream().mapToInt(Integer::intValue).max();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

