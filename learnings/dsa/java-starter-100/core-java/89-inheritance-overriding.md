# 89. Override a Method

**What you learn:** Java core java APIs and problem solving.

## Problem

Make each shape report its own area through a common method.

## Example

~~~text
Input: circle radius 2
Output: 12.566...
~~~

## Simple idea

A subclass override is selected through a parent reference at runtime.

## Java solution

~~~java
static class Shape { double area() { return 0; } }
static final class Circle extends Shape {
    private final double radius;
    Circle(double radius) { this.radius = radius; }
    @Override double area() { return Math.PI * radius * radius; }
}
static double areaOf(Shape shape) { return shape.area(); }
~~~

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

