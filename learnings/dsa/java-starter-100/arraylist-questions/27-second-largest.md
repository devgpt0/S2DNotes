# 27. Find the Second-Largest Distinct Value

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return the second-largest distinct value, or OptionalInt.empty().

## Example

~~~text
Input: values = [4, 9, 9, 2, 7]
Output: OptionalInt[7]
~~~

## Simple idea

Track the largest and second-largest distinct values in one pass.

## Java solution

~~~java
static OptionalInt secondLargest(List<Integer> values) {
    Integer largest = null, second = null;
    for (int value : values) {
        if (largest == null || value > largest) { second = largest; largest = value; }
        else if (value < largest && (second == null || value > second)) second = value;
    }
    return second == null ? OptionalInt.empty() : OptionalInt.of(second);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

