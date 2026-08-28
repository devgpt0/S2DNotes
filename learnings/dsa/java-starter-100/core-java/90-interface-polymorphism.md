# 90. Use an Interface

**What you learn:** Java core java APIs and problem solving.

## Problem

Sum the price returned by every Priced item.

## Example

~~~text
Input: items=[Book:10, Pen:2]
Output: 12
~~~

## Simple idea

Depend on the behavior in the interface, not concrete classes.

## Java solution

~~~java
interface Priced { int price(); }
static int totalPrice(List<Priced> items) {
    int total = 0;
    for (Priced item : items) total += item.price();
    return total;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

