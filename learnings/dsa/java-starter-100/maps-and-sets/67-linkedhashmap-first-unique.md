# 67. Find First Unique with LinkedHashMap

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return the first string that occurs once.

## Example

~~~text
Input: words=[red,blue,red,green]
Output: blue
~~~

## Simple idea

Count first, then scan the insertion-ordered map.

## Java solution

~~~java
static Optional<String> firstUnique(List<String> words) {
    Map<String, Integer> counts = new LinkedHashMap<>();
    for (String word : words) counts.merge(word, 1, Integer::sum);
    for (var entry : counts.entrySet())
        if (entry.getValue() == 1) return Optional.of(entry.getKey());
    return Optional.empty();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

