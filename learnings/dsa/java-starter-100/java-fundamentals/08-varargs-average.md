# 08. Average Values with Varargs

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Average any number of int arguments.

## Example

~~~text
Input: values = [2, 4, 6]
Output: 4.0
~~~

## Simple idea

int... is an array inside the method; cast before division.

## Java solution

~~~java
static double average(int... values) {
    if (values.length == 0) return 0.0;
    int total = 0;
    for (int value : values) total += value;
    return (double) total / values.length;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n) for the varargs array`

Try to write the solution yourself before reading the code.

