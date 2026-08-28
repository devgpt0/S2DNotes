# 50. Evaluate a Postfix Expression

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Evaluate space-separated integer postfix tokens using +, -, *, and /.

## Example

~~~text
Input: [2, 3, +, 4, *]
Output: 20
~~~

## Simple idea

Pop the right operand first, then the left operand.

## Java solution

~~~java
static int evaluate(String[] tokens) {
    Deque<Integer> stack = new ArrayDeque<>();
    for (String token : tokens) {
        if (token.matches("-?\\d+")) stack.push(Integer.parseInt(token));
        else {
            int right = stack.pop(), left = stack.pop();
            stack.push(switch (token) {
                case "+" -> left + right; case "-" -> left - right;
                case "*" -> left * right; case "/" -> left / right;
                default -> throw new IllegalArgumentException();
            });
        }
    }
    return stack.pop();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

