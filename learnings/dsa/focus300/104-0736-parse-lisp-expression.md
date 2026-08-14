# Focus300 104: LeetCode 736 - Parse Lisp Expression

**Source:** [LeetCode 736](https://leetcode.com/problems/parse-lisp-expression/)  
**Difficulty:** Hard  
**Pattern:** recursive descent with lexical scope

## Exact contract

Evaluate a valid expression containing integers, variables, and the forms
`(add e1 e2)`, `(mult e1 e2)`, and
`(let v1 e1 ... vn en expr)`. A `let` binding is visible to later expressions
inside that same form, inner bindings shadow outer ones, and bindings do not
escape their form. Return the resulting integer.

## First principles

The grammar determines where each expression ends, so parsing must return both
its value and the next unread token. Lexical scope is a stack: entering a `let`
adds bindings, and leaving it restores exactly the bindings that form created.

## Cases that decide correctness

- Negative integers are atoms; lowercase names are variables.
- `add` and `mult` consume exactly two expressions.
- The last item in `let` is its result expression, not another assignment.
- A binding is visible to assignments that follow it in the same `let`.
- Shadowed values must reappear when the inner `let` ends.

## Brute force: copy the environment for every `let`

```python
def evaluate_lisp_copying(expression: str) -> int:
    if not expression:
        raise ValueError("expression must be non-empty")
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()

    def evaluate(index: int, environment: dict[str, int]) -> tuple[int, int]:
        item = tokens[index]
        if item != "(":
            if item.lstrip("-").isdigit():
                return int(item), index + 1
            if item not in environment:
                raise ValueError(f"undefined variable: {item}")
            return environment[item], index + 1

        operation = tokens[index + 1]
        index += 2
        if operation in {"add", "mult"}:
            first, index = evaluate(index, environment)
            second, index = evaluate(index, environment)
            if tokens[index] != ")":
                raise ValueError("expected closing parenthesis")
            value = first + second if operation == "add" else first * second
            return value, index + 1
        if operation != "let":
            raise ValueError(f"unknown operation: {operation}")

        local = environment.copy()
        while True:
            item = tokens[index]
            is_final = (
                item == "(" or item.lstrip("-").isdigit() or tokens[index + 1] == ")"
            )
            if is_final:
                result, index = evaluate(index, local)
                break
            value, index = evaluate(index + 1, local)
            local[item] = value
        if tokens[index] != ")":
            raise ValueError("expected closing parenthesis")
        return result, index + 1

    result, next_index = evaluate(0, {})
    if next_index != len(tokens):
        raise ValueError("unexpected trailing tokens")
    return result
```

Dictionary copying makes deeply nested `let` forms cost `O(n * d)` time and
space in the worst case, where `d` is scope depth.

## Better transition: keep one value stack per variable

Tokenizing once already prevents repeated string reconstruction. Instead of
copying every visible binding, push only assignments made by the current `let`
and pop those assignments when the form closes.

## Expert solution: recursive descent with binding stacks

```python
def evaluate_lisp(expression: str) -> int:
    if not expression:
        raise ValueError("expression must be non-empty")
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    bindings: dict[str, list[int]] = {}

    def evaluate(index: int) -> tuple[int, int]:
        item = tokens[index]
        if item != "(":
            if item.lstrip("-").isdigit():
                return int(item), index + 1
            values = bindings.get(item)
            if not values:
                raise ValueError(f"undefined variable: {item}")
            return values[-1], index + 1

        operation = tokens[index + 1]
        index += 2
        if operation in {"add", "mult"}:
            first, index = evaluate(index)
            second, index = evaluate(index)
            if tokens[index] != ")":
                raise ValueError("expected closing parenthesis")
            value = first + second if operation == "add" else first * second
            return value, index + 1
        if operation != "let":
            raise ValueError(f"unknown operation: {operation}")

        assigned: list[str] = []
        while True:
            item = tokens[index]
            is_final = (
                item == "(" or item.lstrip("-").isdigit() or tokens[index + 1] == ")"
            )
            if is_final:
                result, index = evaluate(index)
                break
            value, index = evaluate(index + 1)
            bindings.setdefault(item, []).append(value)
            assigned.append(item)

        if tokens[index] != ")":
            raise ValueError("expected closing parenthesis")
        for variable in reversed(assigned):
            bindings[variable].pop()
            if not bindings[variable]:
                del bindings[variable]
        return result, index + 1

    result, next_index = evaluate(0)
    if next_index != len(tokens):
        raise ValueError("unexpected trailing tokens")
    return result
```

Every token is consumed once and every binding is pushed and popped once. The
binding stack at evaluation time is therefore exactly the lexical environment.

**Complexity:** `O(n)` time and `O(n)` space for tokens, recursion, and active
bindings.
