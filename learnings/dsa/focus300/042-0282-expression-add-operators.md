# Focus300 042: LeetCode 282 - Expression Add Operators

**Source:** [LeetCode 282](https://leetcode.com/problems/expression-add-operators/)  
**Difficulty:** Hard  
**Pattern:** expression backtracking with deferred multiplication

## Exact contract

Given a nonempty decimal digit string and an integer target, insert zero or more
binary operators `+`, `-`, and `*` between digits. Return every expression that
evaluates to the target under normal multiplication precedence. Digits cannot
be reordered, and a multi-digit operand cannot start with zero. Output order is
unrestricted.

## First principles

At every gap, either continue the current operand or begin a new operand with
one of three operators. During DFS, maintain the full value and the most recent
signed additive term. Multiplication replaces that term:

```text
new_value = value - last_term + last_term * operand
```

## Cases that decide correctness

- The whole digit string may be one operand.
- Operand `0` is valid, but `00` and `05` are not.
- Multiplication binds more tightly than addition and subtraction.
- Negative intermediate values are valid.
- Distinct operator placements produce distinct expressions.

## Brute force: enumerate all four choices at every gap

```python
from itertools import product


def add_operators_brute(digits: str, target: int) -> list[str]:
    if not digits or any(not "0" <= character <= "9" for character in digits):
        raise ValueError("digits must be a nonempty decimal string")

    def evaluate(expression: str) -> int | None:
        operands: list[int] = []
        operators: list[str] = []
        start = 0
        for index, character in enumerate(expression):
            if character not in {"+", "-", "*"}:
                continue
            part = expression[start:index]
            if len(part) > 1 and part[0] == "0":
                return None
            operands.append(int(part))
            operators.append(character)
            start = index + 1
        part = expression[start:]
        if len(part) > 1 and part[0] == "0":
            return None
        operands.append(int(part))

        total = 0
        term = operands[0]
        sign = 1
        for operator, operand in zip(operators, operands[1:]):
            if operator == "*":
                term *= operand
            else:
                total += sign * term
                sign = 1 if operator == "+" else -1
                term = operand
        return total + sign * term

    answers: list[str] = []
    for choices in product(("", "+", "-", "*"), repeat=len(digits) - 1):
        parts = [digits[0]]
        for operator, digit in zip(choices, digits[1:]):
            parts.extend((operator, digit))
        expression = "".join(parts)
        if evaluate(expression) == target:
            answers.append(expression)
    return answers
```

This visits all `4^(n-1)` gap assignments and then reparses each expression.

## Better transition: evaluate while choosing operands

Choose an entire next operand substring at once. Carrying the accumulated value
and last multiplicative term avoids reparsing and applies precedence in
constant time per operator choice.

## Expert solution: DFS with the previous term

```python
def add_operators(digits: str, target: int) -> list[str]:
    if not digits or any(not "0" <= character <= "9" for character in digits):
        raise ValueError("digits must be a nonempty decimal string")

    answers: list[str] = []

    def search(index: int, expression: str, value: int, last_term: int) -> None:
        if index == len(digits):
            if value == target:
                answers.append(expression)
            return
        for end in range(index + 1, len(digits) + 1):
            if end > index + 1 and digits[index] == "0":
                break
            text = digits[index:end]
            operand = int(text)
            if index == 0:
                search(end, text, operand, operand)
                continue
            search(end, expression + "+" + text, value + operand, operand)
            search(end, expression + "-" + text, value - operand, -operand)
            multiplied = last_term * operand
            search(
                end,
                expression + "*" + text,
                value - last_term + multiplied,
                multiplied,
            )

    search(0, "", 0, 0)
    return answers
```

Every valid expression has one unique sequence of operand endpoints and
operators, so DFS generates it once. The carried value equals the expression's
value, and replacing `last_term` implements exactly multiplication precedence.

**Complexity:** `O(4^n)` output-sensitive time and `O(n)` recursion space,
excluding returned strings.
