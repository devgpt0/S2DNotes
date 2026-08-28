# 63. Find the Kth Largest Value

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Return the kth-largest value in an integer array.

## Example

~~~text
Input: values=[4,1,7,2], k=2
Output: 4
~~~

## Simple idea

Keep only k values in a min-heap; its root is the kth largest.

## Java solution

~~~java
static int kthLargest(int[] values, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    for (int value : values) {
        heap.offer(value); if (heap.size() > k) heap.poll();
    }
    return heap.peek();
}
~~~

## Complexity

- Time: `O(n log k)`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

