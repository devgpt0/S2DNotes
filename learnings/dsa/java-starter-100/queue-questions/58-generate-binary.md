# 58. Generate Binary Numbers with a Queue

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Generate binary strings from 1 through n in numeric order.

## Example

~~~text
Input: n = 4
Output: [1, 10, 11, 100]
~~~

## Simple idea

Remove one string and enqueue it with 0 and 1 appended.

## Java solution

~~~java
static ArrayList<String> binaryNumbers(int n) {
    ArrayList<String> result = new ArrayList<>();
    Queue<String> queue = new ArrayDeque<>(); queue.offer("1");
    for (int i = 0; i < n; i++) {
        String value = queue.poll(); result.add(value);
        queue.offer(value + "0"); queue.offer(value + "1");
    }
    return result;
}
~~~

## Complexity

- Time: `O(n) outputs`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

