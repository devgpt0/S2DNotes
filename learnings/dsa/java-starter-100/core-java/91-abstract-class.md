# 91. Implement an Abstract Class

**What you learn:** Java core java APIs and problem solving.

## Problem

Create a Rectangle subclass that implements area.

## Example

~~~text
Input: width=3, height=4
Output: 12
~~~

## Simple idea

The abstract base class defines the contract; Rectangle supplies the formula.

## Java solution

~~~java
abstract static class Figure { abstract int area(); }
static final class Rectangle extends Figure {
    private final int width, height;
    Rectangle(int width, int height) { this.width = width; this.height = height; }
    @Override int area() { return width * height; }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

