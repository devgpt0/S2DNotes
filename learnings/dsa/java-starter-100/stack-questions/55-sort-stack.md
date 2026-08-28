# 55. Sort a Stack

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Return stack values in ascending order using stacks only.

## Example

~~~text
Input: values = [3, 1, 2]
Output: [1, 2, 3]
~~~

## Simple idea

Move larger temporary values back until the new value fits.

## Java solution

~~~java
static Deque<Integer> sortStack(Deque<Integer> input) {
    Deque<Integer> sorted = new ArrayDeque<>();
    while (!input.isEmpty()) {
        int value = input.pop();
        while (!sorted.isEmpty() && sorted.peek() > value) input.push(sorted.pop());
        sorted.push(value);
    }
    return sorted;
}
~~~

## Complexity

- Time: `O(n²)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

