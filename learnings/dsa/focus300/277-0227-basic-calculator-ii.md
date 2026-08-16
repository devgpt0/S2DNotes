# Focus300 277: LeetCode 227 - Basic Calculator II

**Source:** [LeetCode 227](https://leetcode.com/problems/basic-calculator-ii/)  
**Difficulty:** Medium  
**Pattern:** expression parsing with operator precedence

## Exact contract

Evaluate an arithmetic expression containing `+`, `-`, `*`, and `/` with normal precedence.

## First principles

Multiplication and division bind tighter than addition and subtraction, but the expression can still be evaluated in one pass if the current term is accumulated correctly.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Division uses truncation toward zero under the problem's rule.
- Spaces should be ignored.
- The expression may end with a number rather than an operator.
- A leading term still contributes positively or negatively.

## Brute force

```python
def calculate_brute(s):
    nums = []
    stack = []
    num = 0
    op = "+"
    s += "+"
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack[-1] *= num
            else:
                stack[-1] = int(stack[-1] / num)
            op = ch
            num = 0
    return sum(stack)
```

Convert to postfix or build a full parse tree first.

## Better insight

Track the current term and push only finalized terms onto a stack.

## Expert solution

```python
def calculate(s):
    stack = []
    num = 0
    op = "+"
    s += "+"
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack[-1] *= num
            else:
                stack[-1] = int(stack[-1] / num)
            op = ch
            num = 0
    return sum(stack)
```

Scan the string once, assemble each number, and apply the previous operator as soon as the next operator is encountered.

**Complexity:** O(n) time and O(n) space for the operator stack in the common implementation.
