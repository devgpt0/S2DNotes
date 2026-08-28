# 70. Remove Duplicates and Keep Order

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return unique strings in first-seen order.

## Example

~~~text
Input: values=[b,a,b,c]
Output: [b,a,c]
~~~

## Simple idea

LinkedHashSet remembers insertion order unlike HashSet.

## Java solution

~~~java
static ArrayList<String> uniqueInOrder(List<String> values) {
    return new ArrayList<>(new LinkedHashSet<>(values));
}
~~~

## Complexity

- Time: `O(n) average`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

