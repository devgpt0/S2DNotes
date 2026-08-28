# 93. Write a Generic Maximum Method

**What you learn:** Java core java APIs and problem solving.

## Problem

Return the larger of two Comparable values.

## Example

~~~text
Input: max(cat, dog)
Output: dog
~~~

## Simple idea

The bound allows the method to call compareTo safely.

## Java solution

~~~java
static <T extends Comparable<? super T>> T maximum(T first, T second) {
    return first.compareTo(second) >= 0 ? first : second;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

