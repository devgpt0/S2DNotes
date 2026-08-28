# 15. Find the First Non-Repeating Character

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return the first character appearing exactly once.

## Example

~~~text
Input: text = "swiss"
Output: Optional[w]
~~~

## Simple idea

A LinkedHashMap counts characters while retaining first-seen order.

## Java solution

~~~java
static Optional<Character> firstUnique(String text) {
    Map<Character, Integer> counts = new LinkedHashMap<>();
    for (char c : text.toCharArray()) counts.merge(c, 1, Integer::sum);
    for (var entry : counts.entrySet())
        if (entry.getValue() == 1) return Optional.of(entry.getKey());
    return Optional.empty();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

