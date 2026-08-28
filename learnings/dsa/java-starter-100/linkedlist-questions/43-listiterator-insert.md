# 43. Insert with a ListIterator

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Insert value before the first value greater than it.

## Example

~~~text
Input: values = [1, 3, 5], value = 4
Output: [1, 3, 4, 5]
~~~

## Simple idea

ListIterator.add inserts relative to its cursor without manual indexes.

## Java solution

~~~java
static void insertBeforeLarger(LinkedList<Integer> values, int value) {
    ListIterator<Integer> it = values.listIterator();
    while (it.hasNext()) if (it.next() > value) { it.previous(); it.add(value); return; }
    it.add(value);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

