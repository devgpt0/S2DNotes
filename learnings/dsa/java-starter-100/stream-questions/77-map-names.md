# 77. Map Names with Streams

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return every name in uppercase.

## Example

~~~text
Input: names=[Ada,Lin]
Output: [ADA, LIN]
~~~

## Simple idea

map transforms each element without changing the source list.

## Java solution

~~~java
static List<String> uppercase(List<String> names) {
    return names.stream().map(String::toUpperCase).toList();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

