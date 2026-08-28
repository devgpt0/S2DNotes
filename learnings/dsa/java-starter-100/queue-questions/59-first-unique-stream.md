# 59. Track a Non-Repeating Character Stream

**What you learn:** Java queue questions APIs and problem solving.

## Problem

After each character, return the current first unique character or #.

## Example

~~~text
Input: stream = "aabc"
Output: [a, #, b, b]
~~~

## Simple idea

Count characters and discard queue heads that are no longer unique.

## Java solution

~~~java
static String firstUniqueAfterEach(String stream) {
    Map<Character, Integer> counts = new HashMap<>(); Queue<Character> queue = new ArrayDeque<>();
    StringBuilder result = new StringBuilder();
    for (char c : stream.toCharArray()) {
        counts.merge(c, 1, Integer::sum); queue.offer(c);
        while (!queue.isEmpty() && counts.get(queue.peek()) > 1) queue.poll();
        result.append(queue.isEmpty() ? '#' : queue.peek());
    }
    return result.toString();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

