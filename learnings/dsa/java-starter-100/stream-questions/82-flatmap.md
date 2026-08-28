# 82. Flatten Nested Lists

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return all numbers from a list of lists as one list.

## Example

~~~text
Input: values=[[1,2],[3],[4,5]]
Output: [1,2,3,4,5]
~~~

## Simple idea

flatMap joins the elements of each inner stream.

## Java solution

~~~java
static List<Integer> flatten(List<List<Integer>> values) {
    return values.stream().flatMap(Collection::stream).toList();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

