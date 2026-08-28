# 28. Merge Two Sorted ArrayLists

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Merge two ascending lists into a new ascending ArrayList.

## Example

~~~text
Input: left = [1, 4], right = [2, 3]
Output: [1, 2, 3, 4]
~~~

## Simple idea

Compare current values, append the smaller one, and append the remainder.

## Java solution

~~~java
static ArrayList<Integer> merge(List<Integer> left, List<Integer> right) {
    ArrayList<Integer> result = new ArrayList<>();
    int i = 0, j = 0;
    while (i < left.size() && j < right.size())
        result.add(left.get(i) <= right.get(j) ? left.get(i++) : right.get(j++));
    while (i < left.size()) result.add(left.get(i++));
    while (j < right.size()) result.add(right.get(j++));
    return result;
}
~~~

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

