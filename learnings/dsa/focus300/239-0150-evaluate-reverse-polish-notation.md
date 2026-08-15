# Focus300 239: LeetCode 150 - Evaluate Reverse Polish Notation

**Source:** [LeetCode 150](https://leetcode.com/problems/evaluate-reverse-polish-notation/)  
**Difficulty:** Medium  
**Pattern:** operand stack evaluation

## Exact contract

Evaluate an expression written in reverse Polish notation.

## First principles

Every operator consumes the most recent operands. A stack exactly models that last-in, first-out data dependency.

## Cases that decide correctness

- Negative numbers must be parsed as values, not operators.
- Division uses the problem's truncation rule.
- The expression is always valid under the problem contract.
- Each operator reduces the stack size by one.

## Brute force

```python
def eval_rpn_brute(tokens):
    stack = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[-1]
```

Try to convert the expression back to infix and reparse it.

## Better insight

Push values and pop the top two values whenever an operator appears.

## Expert solution

```python
def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token == "+":
            b = stack.pop(); a = stack.pop(); stack.append(a + b)
        elif token == "-":
            b = stack.pop(); a = stack.pop(); stack.append(a - b)
        elif token == "*":
            b = stack.pop(); a = stack.pop(); stack.append(a * b)
        elif token == "/":
            b = stack.pop(); a = stack.pop(); stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[-1]
```

Walk the token stream once, use a stack for operands, and replace each operator with the computed result of its two inputs.

**Complexity:** O(n) time and O(n) space.
