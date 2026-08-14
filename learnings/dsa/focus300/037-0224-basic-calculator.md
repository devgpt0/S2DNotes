# Focus300 037: LeetCode 224 - Basic Calculator

**Source:** [LeetCode 224 - Basic Calculator](https://leetcode.com/problems/basic-calculator/)  
**Difficulty:** Hard  
**Pattern:** signed subtotal stack  

## Exact contract

Evaluate a valid expression containing nonnegative decimal integers, spaces,
`+`, `-`, `(`, and `)`. Parentheses may nest, and unary signs are allowed where
the source grammar permits them. Division and multiplication do not exist.

## First principles

Without multiplication, a parsed number or parenthesized subtotal is added to
the current subtotal with sign `+1` or `-1`. Entering parentheses saves the
outer subtotal and sign; closing them applies that context to the completed
inner subtotal.

## Cases that decide correctness

- Multi-digit numbers must be consumed as one token.
- A leading minus sign applies to the first number or parenthesized group.
- Spaces have no semantic effect.
- A minus before parentheses negates the entire subtotal.
- Parentheses must balance and only supported characters are accepted.

## Brute/reference approach: recursively rescan matching parentheses

```python
def basic_calculator_brute(expression: str) -> int:
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("expression must be nonempty")
    if any(character not in "0123456789+-() " for character in expression):
        raise ValueError("unsupported character")
    balance = 0
    for character in expression:
        balance += character == "("
        balance -= character == ")"
        if balance < 0:
            raise ValueError("unbalanced parentheses")
    if balance:
        raise ValueError("unbalanced parentheses")

    def evaluate(left: int, right: int) -> int:
        subtotal = 0
        sign = 1
        index = left
        while index < right:
            character = expression[index]
            if character == " ":
                index += 1
            elif character.isdigit():
                number = 0
                while index < right and expression[index].isdigit():
                    number = 10 * number + int(expression[index])
                    index += 1
                subtotal += sign * number
                sign = 1
            elif character in "+-":
                sign = 1 if character == "+" else -1
                index += 1
            elif character == "(":
                depth = 1
                closing = index + 1
                while depth:
                    depth += expression[closing] == "("
                    depth -= expression[closing] == ")"
                    closing += 1
                subtotal += sign * evaluate(index + 1, closing - 1)
                sign = 1
                index = closing
            else:
                raise ValueError("unexpected closing parenthesis")
        return subtotal

    return evaluate(0, len(expression))
```

Repeatedly scanning for a matching close makes deeply nested input quadratic.

**Complexity:** `O(n^2)` worst-case time and `O(n)` recursion space.

## Better approach: tokenize, then use two stacks

A shunting-yard evaluator stores numbers and operators separately and reduces
on closing parentheses. Because all binary operators have equal precedence, a
single context stack is sufficient.

## Expert solution: one pass with saved signed subtotals

```python
def basic_calculator(expression: str) -> int:
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("expression must be nonempty")
    if any(character not in "0123456789+-() " for character in expression):
        raise ValueError("unsupported character")

    subtotal = 0
    number = 0
    sign = 1
    contexts: list[tuple[int, int]] = []
    for character in expression:
        if character.isdigit():
            number = 10 * number + int(character)
        elif character in "+-":
            subtotal += sign * number
            number = 0
            sign = 1 if character == "+" else -1
        elif character == "(":
            contexts.append((subtotal, sign))
            subtotal = 0
            number = 0
            sign = 1
        elif character == ")":
            subtotal += sign * number
            number = 0
            if not contexts:
                raise ValueError("unbalanced parentheses")
            outer_subtotal, outer_sign = contexts.pop()
            subtotal = outer_subtotal + outer_sign * subtotal
            sign = 1
    if contexts:
        raise ValueError("unbalanced parentheses")
    return subtotal + sign * number
```

The stack entry is the complete context immediately before an opening
parenthesis. Closing the group restores that context once, so every character
is processed exactly once.

**Complexity:** `O(n)` time and `O(parenthesis depth)` space.

