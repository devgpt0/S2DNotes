# 69. Check for Duplicates with a HashSet

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return whether an integer array contains a duplicate.

## Example

~~~text
Input: values=[1,4,2,4]
Output: true
~~~

## Simple idea

If add returns false, the value was already present.

## Java solution

~~~java
static boolean hasDuplicate(int[] values) {
    Set<Integer> seen = new HashSet<>();
    for (int value : values) if (!seen.add(value)) return true;
    return false;
}
~~~

## Complexity

- Time: `O(n) average`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

