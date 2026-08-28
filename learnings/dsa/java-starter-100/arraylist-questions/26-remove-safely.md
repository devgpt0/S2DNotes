# 26. Remove ArrayList Values Safely

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Remove every negative value from an ArrayList<Integer>.

## Example

~~~text
Input: values = [4, -1, 2, -3]
Output: [4, 2]
~~~

## Simple idea

removeIf performs safe iterator-backed removal.

## Java solution

~~~java
static void removeNegatives(ArrayList<Integer> values) {
    values.removeIf(value -> value < 0);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1) extra`

Try to write the solution yourself before reading the code.

