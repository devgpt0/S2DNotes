# 21. Keep Positive Values

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return a new ArrayList<Integer> containing only positive values.

## Example

~~~text
Input: values = [-2, 5, 0, 8]
Output: [5, 8]
~~~

## Simple idea

Read each element and append matching values.

## Java solution

~~~java
static ArrayList<Integer> positives(List<Integer> values) {
    ArrayList<Integer> result = new ArrayList<>();
    for (int value : values) if (value > 0) result.add(value);
    return result;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

