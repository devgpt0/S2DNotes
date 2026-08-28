# 03. Reverse an Array In Place

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Reverse an int[] without creating another array.

## Example

~~~text
Input: values = [1, 2, 3, 4]
Output: [4, 3, 2, 1]
~~~

## Simple idea

Swap matching elements from the two ends while pointers move inward.

## Java solution

~~~java
static void reverse(int[] values) {
    for (int left = 0, right = values.length - 1; left < right; left++, right--) {
        int temp = values[left]; values[left] = values[right]; values[right] = temp;
    }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

