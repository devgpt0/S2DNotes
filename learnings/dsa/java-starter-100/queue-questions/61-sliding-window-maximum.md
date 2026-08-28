# 61. Find Sliding Window Maximums

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Return the maximum value in every window of size k.

## Example

~~~text
Input: values=[1,3,-1,5], k=2
Output: [3, 3, 5]
~~~

## Simple idea

A monotonic deque keeps candidate indexes in decreasing-value order.

## Java solution

~~~java
static int[] windowMaximums(int[] values, int k) {
    int[] result = new int[values.length - k + 1]; Deque<Integer> deque = new ArrayDeque<>();
    for (int i = 0; i < values.length; i++) {
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.removeFirst();
        while (!deque.isEmpty() && values[deque.peekLast()] <= values[i]) deque.removeLast();
        deque.addLast(i);
        if (i >= k - 1) result[i - k + 1] = values[deque.peekFirst()];
    }
    return result;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

