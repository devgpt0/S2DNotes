# 25. Update an ArrayList Element

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Replace the element at index with newValue.

## Example

~~~text
Input: values = [10, 20, 30], index = 1, newValue = 25
Output: [10, 25, 30]
~~~

## Simple idea

set replaces an existing position without changing list size.

## Java solution

~~~java
static void update(ArrayList<Integer> values, int index, int newValue) {
    values.set(index, newValue);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

