# 35. Count a Value in an ArrayList

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Count occurrences of target in a list.

## Example

~~~text
Input: values = [2, 4, 2, 2], target = 2
Output: 3
~~~

## Simple idea

Collections.frequency compares elements using equals.

## Java solution

~~~java
static int frequency(List<Integer> values, int target) {
    return Collections.frequency(values, target);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

