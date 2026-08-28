# 66. Count Frequencies with a HashMap

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return the frequency of every integer.

## Example

~~~text
Input: values=[2,2,3,2]
Output: {2=3, 3=1}
~~~

## Simple idea

For each value, increase its current count.

## Java solution

~~~java
static Map<Integer, Integer> frequencies(int[] values) {
    Map<Integer, Integer> result = new HashMap<>();
    for (int value : values) result.merge(value, 1, Integer::sum);
    return result;
}
~~~

## Complexity

- Time: `O(n) average`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

