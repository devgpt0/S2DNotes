# 34. Understand Immutable List Factories

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return a mutable list containing given values.

## Example

~~~text
Input: values = [1, 2, 3]
Output: mutable [1, 2, 3]
~~~

## Simple idea

List.of is unmodifiable; copy it before add or remove.

## Java solution

~~~java
static ArrayList<Integer> mutableCopy(Integer... values) {
    return new ArrayList<>(List.of(values));
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

