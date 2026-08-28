# 31. Remove an Integer Value Correctly

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Remove the value 2, not the element at index 2.

## Example

~~~text
Input: values = [1, 2, 3], value = 2
Output: [1, 3]
~~~

## Simple idea

remove(2) means index; remove(Integer.valueOf(2)) means value.

## Java solution

~~~java
static void removeValue(ArrayList<Integer> values, int target) {
    values.remove(Integer.valueOf(target));
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

