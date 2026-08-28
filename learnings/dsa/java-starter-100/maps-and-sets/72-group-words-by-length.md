# 72. Group Words by Length

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return words grouped by their length.

## Example

~~~text
Input: words=[a,to,cat,be]
Output: {1=[a],2=[to,be],3=[cat]}
~~~

## Simple idea

computeIfAbsent creates a list only for a new length.

## Java solution

~~~java
static Map<Integer, List<String>> groupByLength(List<String> words) {
    Map<Integer, List<String>> groups = new TreeMap<>();
    for (String word : words)
        groups.computeIfAbsent(word.length(), ignored -> new ArrayList<>()).add(word);
    return groups;
}
~~~

## Complexity

- Time: `O(n log k)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

