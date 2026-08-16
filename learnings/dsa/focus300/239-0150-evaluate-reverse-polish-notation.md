# Focus300 239: LeetCode 150 - Evaluate Reverse Polish Notation

**Source:** [LeetCode 150](https://leetcode.com/problems/evaluate-reverse-polish-notation/)  
**Difficulty:** Medium  
**Pattern:** operand stack evaluation

## Exact contract

Evaluate an expression written in reverse Polish notation.

## First principles

Every operator consumes the most recent operands. A stack exactly models that last-in, first-out data dependency.


## Classroom board: evaluate with an operand stack

```text
    tokens = [2, 1, +, 3, *]

    push numbers, pop two numbers for each operator, push the result back.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

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
