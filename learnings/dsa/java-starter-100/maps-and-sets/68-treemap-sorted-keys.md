# 68. Print Map Keys in Sorted Order

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return a map whose string keys are alphabetically sorted.

## Example

~~~text
Input: scores={Bob:8, Ann:9}
Output: {Ann=9, Bob=8}
~~~

## Simple idea

TreeMap maintains keys in sorted order.

## Java solution

~~~java
static Map<String, Integer> sortedScores(Map<String, Integer> scores) {
    return new TreeMap<>(scores);
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

