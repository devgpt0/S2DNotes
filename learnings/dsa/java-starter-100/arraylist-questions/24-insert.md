# 24. Insert into an ArrayList

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Insert value at index and return the same list.

## Example

~~~text
Input: values = [1, 3, 4], index = 1, value = 2
Output: [1, 2, 3, 4]
~~~

## Simple idea

add(index, value) shifts later elements right.

## Java solution

~~~java
static void insert(ArrayList<Integer> values, int index, int value) {
    values.add(index, value);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1) extra`

Try to write the solution yourself before reading the code.

