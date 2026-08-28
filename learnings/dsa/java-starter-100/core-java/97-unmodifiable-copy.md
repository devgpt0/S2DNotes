# 97. Make an Unmodifiable Copy

**What you learn:** Java core java APIs and problem solving.

## Problem

Return a list that callers cannot mutate.

## Example

~~~text
Input: values=[1,2,3]
Output: unmodifiable [1,2,3]
~~~

## Simple idea

Copying first prevents both source and caller mutation.

## Java solution

~~~java
static List<Integer> readOnlyCopy(List<Integer> values) {
    return List.copyOf(values);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

