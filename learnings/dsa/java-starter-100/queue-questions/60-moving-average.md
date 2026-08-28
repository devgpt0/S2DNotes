# 60. Calculate a Moving Average

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Return the average of the latest window values after each insertion.

## Example

~~~text
Input: values=[1,10,3], window=2
Output: [1.0, 5.5, 6.5]
~~~

## Simple idea

Keep a running sum and remove the oldest value when the queue is too large.

## Java solution

~~~java
static ArrayList<Double> movingAverage(int[] values, int window) {
    Queue<Integer> queue = new ArrayDeque<>(); ArrayList<Double> result = new ArrayList<>();
    long sum = 0;
    for (int value : values) {
        queue.offer(value); sum += value;
        if (queue.size() > window) sum -= queue.poll();
        result.add((double) sum / queue.size());
    }
    return result;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(window)`

Try to write the solution yourself before reading the code.

