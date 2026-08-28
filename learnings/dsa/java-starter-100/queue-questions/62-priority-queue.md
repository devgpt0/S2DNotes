# 62. Use a PriorityQueue

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Return values in ascending order using a min-priority queue.

## Example

~~~text
Input: values=[5,1,3]
Output: [1,3,5]
~~~

## Simple idea

A default PriorityQueue exposes the smallest value at peek.

## Java solution

~~~java
static ArrayList<Integer> ascending(int[] values) {
    Queue<Integer> queue = new PriorityQueue<>();
    for (int value : values) queue.offer(value);
    ArrayList<Integer> result = new ArrayList<>();
    while (!queue.isEmpty()) result.add(queue.poll());
    return result;
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

