# 42. Check a LinkedList Palindrome

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Return whether a LinkedList<Character> is a palindrome.

## Example

~~~text
Input: values = [r, a, d, a, r]
Output: true
~~~

## Simple idea

Copy to a deque and compare its two ends.

## Java solution

~~~java
static boolean isPalindrome(LinkedList<Character> values) {
    Deque<Character> deque = new ArrayDeque<>(values);
    while (deque.size() > 1)
        if (!deque.removeFirst().equals(deque.removeLast())) return false;
    return true;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

