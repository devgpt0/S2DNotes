# 75. Convert Celsius to Fahrenheit

**What you learn:** Using a formula.

## Problem

Return the Fahrenheit temperature for a Celsius temperature.

## Example

```text
Input: celsius = 25
Output: 77.0
```

## Simple idea

Multiply Celsius by 9, divide by 5, then add 32.

## Python solution

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
