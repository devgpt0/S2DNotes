# 71. Find Sorted Unique Values

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return unique values from low through high inclusive.

## Example

~~~text
Input: values=[5,1,3,3,8], low=2, high=5
Output: [3,5]
~~~

## Simple idea

Build a TreeSet and use its inclusive subset view.

## Java solution

~~~java
static NavigableSet<Integer> between(int[] values, int low, int high) {
    TreeSet<Integer> sorted = new TreeSet<>();
    for (int value : values) sorted.add(value);
    return sorted.subSet(low, true, high, true);
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

