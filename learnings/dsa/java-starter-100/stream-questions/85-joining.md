# 85. Join Names for Display

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Join names with comma-space and surround them with brackets.

## Example

~~~text
Input: names=[Ada,Lin]
Output: [Ada, Lin]
~~~

## Simple idea

Collectors.joining handles delimiters and optional prefix/suffix.

## Java solution

~~~java
static String displayNames(List<String> names) {
    return names.stream().collect(Collectors.joining(", ", "[", "]"));
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

