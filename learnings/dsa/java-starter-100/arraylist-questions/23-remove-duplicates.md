# 23. Remove ArrayList Duplicates

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return a duplicate-free ArrayList that keeps first occurrences in order.

## Example

~~~text
Input: values = [3, 1, 3, 2, 1]
Output: [3, 1, 2]
~~~

## Simple idea

LinkedHashSet remembers insertion order; copy it into an ArrayList.

## Java solution

~~~java
static ArrayList<Integer> unique(List<Integer> values) {
    return new ArrayList<>(new LinkedHashSet<>(values));
}
~~~

## Complexity

- Time: `O(n) average`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

