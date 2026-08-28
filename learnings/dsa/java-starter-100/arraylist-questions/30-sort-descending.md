# 30. Sort an ArrayList Descending

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Sort an ArrayList<Integer> in descending order.

## Example

~~~text
Input: values = [4, 1, 9, 2]
Output: [9, 4, 2, 1]
~~~

## Simple idea

Pass Comparator.reverseOrder() to sort.

## Java solution

~~~java
static void sortDescending(ArrayList<Integer> values) {
    values.sort(Comparator.reverseOrder());
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(log n) typical stack space`

Try to write the solution yourself before reading the code.

