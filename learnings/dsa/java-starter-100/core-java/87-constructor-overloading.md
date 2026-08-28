# 87. Overload Constructors

**What you learn:** Java core java APIs and problem solving.

## Problem

Create a Point with either (0,0) or supplied coordinates.

## Example

~~~text
Input: new Point()
Output: Point[x=0, y=0]
~~~

## Simple idea

Delegate the no-argument constructor with this(...).

## Java solution

~~~java
record Point(int x, int y) {
    Point() { this(0, 0); }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

