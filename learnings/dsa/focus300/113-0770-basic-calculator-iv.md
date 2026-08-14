# Focus300 113: LeetCode 770 - Basic Calculator IV

**Source:** [LeetCode 770](https://leetcode.com/problems/basic-calculator-iv/)  
**Difficulty:** Hard  
**Pattern:** recursive descent over sparse multivariate polynomials

## Exact contract

Evaluate a valid expression containing nonnegative integers, lowercase
variables, `+`, `-`, `*`, parentheses, and spaces. Substitute paired evaluation
variables and integer values. Return nonzero polynomial terms ordered by
descending degree, then lexicographically by their sorted variable factors.
Each term is `coefficient*factor*...`; a constant contains only its coefficient.

## First principles

A monomial is completely identified by its sorted tuple of variable factors;
its value is the integer coefficient. Addition combines equal tuples, while
multiplication multiplies coefficients and merges factor tuples. Recursive
descent applies normal precedence: factors inside terms, terms inside sums.

## Cases that decide correctness

- Substituted variables become constants before polynomial operations.
- Repeated variables remain repeated factors, such as `a*a*b`.
- Like terms must combine and zero coefficients must disappear.
- Multiplication binds more tightly than addition and subtraction.
- Output ordering uses degree first, not the formatted string's lexicographic
  order.

## Brute force: expand into an uncombined term list

```python
from re import findall, fullmatch


Monomial = tuple[str, ...]
ExpandedPolynomial = list[tuple[int, Monomial]]


def basic_calculator_brute(
    expression: str,
    evaluation_variables: list[str],
    evaluation_values: list[int],
) -> list[str]:
    if type(expression) is not str:
        raise TypeError("expression must be a string")
    if not 1 <= len(expression) <= 250:
        raise ValueError("expression length must be between 1 and 250")
    if type(evaluation_variables) is not list or any(
        type(variable) is not str or fullmatch(r"[a-z]+", variable, flags=0) is None
        for variable in evaluation_variables
    ):
        raise TypeError("evaluation_variables must contain lowercase names")
    if type(evaluation_values) is not list or any(
        type(value) is not int for value in evaluation_values
    ):
        raise TypeError("evaluation_values must be a list of integers")
    if len(evaluation_variables) != len(evaluation_values):
        raise ValueError("evaluation arrays must have equal length")
    if len(set(evaluation_variables)) != len(evaluation_variables):
        raise ValueError("evaluation variable names must be unique")

    compact = expression.replace(" ", "")
    tokens = findall(r"[a-z]+|\d+|[()+\-*]", compact)
    if not tokens or "".join(tokens) != compact:
        raise ValueError("expression contains an invalid token")
    substitutions = dict(zip(evaluation_variables, evaluation_values, strict=True))
    index = 0

    def add(
        left: ExpandedPolynomial,
        right: ExpandedPolynomial,
        sign: int,
    ) -> ExpandedPolynomial:
        return left + [
            (sign * coefficient, monomial) for coefficient, monomial in right
        ]

    def multiply(
        left: ExpandedPolynomial,
        right: ExpandedPolynomial,
    ) -> ExpandedPolynomial:
        return [
            (
                left_coefficient * right_coefficient,
                tuple(sorted(left_monomial + right_monomial)),
            )
            for left_coefficient, left_monomial in left
            for right_coefficient, right_monomial in right
        ]

    def parse_factor() -> ExpandedPolynomial:
        nonlocal index
        if index == len(tokens):
            raise ValueError("expression ends before an operand")
        symbol = tokens[index]
        if symbol == "(":
            index += 1
            result = parse_expression()
            if index == len(tokens) or tokens[index] != ")":
                raise ValueError("expression has an unmatched parenthesis")
            index += 1
            return result
        index += 1
        if symbol.isdigit():
            return [(int(symbol), ())]
        if fullmatch(r"[a-z]+", symbol, flags=0) is not None:
            if symbol in substitutions:
                return [(substitutions[symbol], ())]
            return [(1, (symbol,))]
        raise ValueError("expected a number, variable, or parenthesized expression")

    def parse_term() -> ExpandedPolynomial:
        nonlocal index
        result = parse_factor()
        while index < len(tokens) and tokens[index] == "*":
            index += 1
            result = multiply(result, parse_factor())
        return result

    def parse_expression() -> ExpandedPolynomial:
        nonlocal index
        result = parse_term()
        while index < len(tokens) and tokens[index] in ("+", "-"):
            operator = tokens[index]
            index += 1
            result = add(result, parse_term(), 1 if operator == "+" else -1)
        return result

    expanded = parse_expression()
    if index != len(tokens):
        raise ValueError("expression has an unexpected token")

    combined: dict[Monomial, int] = {}
    for coefficient, monomial in expanded:
        combined[monomial] = combined.get(monomial, 0) + coefficient
    terms = [
        (monomial, coefficient)
        for monomial, coefficient in combined.items()
        if coefficient
    ]
    terms.sort(key=lambda term: (-len(term[0]), term[0]))
    return ["*".join((str(coefficient), *monomial)) for monomial, coefficient in terms]
```

Distributing every product materializes all raw terms before combining them,
so nested products can create exponentially many list entries.

## Better approach: parse to an abstract syntax tree

An AST cleanly separates syntax from evaluation and can postpone expansion,
but every node and traversal adds storage. For a one-shot calculation,
recursive descent can aggregate sparse polynomial terms during parsing.

## Expert solution: combine sparse terms after every operation

```python
from re import findall, fullmatch


Monomial = tuple[str, ...]
Polynomial = dict[Monomial, int]


def basic_calculator(
    expression: str,
    evaluation_variables: list[str],
    evaluation_values: list[int],
) -> list[str]:
    if type(expression) is not str:
        raise TypeError("expression must be a string")
    if not 1 <= len(expression) <= 250:
        raise ValueError("expression length must be between 1 and 250")
    if type(evaluation_variables) is not list or any(
        type(variable) is not str or fullmatch(r"[a-z]+", variable, flags=0) is None
        for variable in evaluation_variables
    ):
        raise TypeError("evaluation_variables must contain lowercase names")
    if type(evaluation_values) is not list or any(
        type(value) is not int for value in evaluation_values
    ):
        raise TypeError("evaluation_values must be a list of integers")
    if len(evaluation_variables) != len(evaluation_values):
        raise ValueError("evaluation arrays must have equal length")
    if len(set(evaluation_variables)) != len(evaluation_variables):
        raise ValueError("evaluation variable names must be unique")

    compact = expression.replace(" ", "")
    tokens = findall(r"[a-z]+|\d+|[()+\-*]", compact)
    if not tokens or "".join(tokens) != compact:
        raise ValueError("expression contains an invalid token")
    substitutions = dict(zip(evaluation_variables, evaluation_values, strict=True))
    index = 0

    def add(left: Polynomial, right: Polynomial, sign: int) -> Polynomial:
        result = left.copy()
        for monomial, coefficient in right.items():
            result[monomial] = result.get(monomial, 0) + sign * coefficient
            if result[monomial] == 0:
                del result[monomial]
        return result

    def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
        result: Polynomial = {}
        for left_monomial, left_coefficient in left.items():
            for right_monomial, right_coefficient in right.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                result[monomial] = result.get(monomial, 0) + (
                    left_coefficient * right_coefficient
                )
                if result[monomial] == 0:
                    del result[monomial]
        return result

    def parse_factor() -> Polynomial:
        nonlocal index
        if index == len(tokens):
            raise ValueError("expression ends before an operand")
        symbol = tokens[index]
        if symbol == "(":
            index += 1
            result = parse_expression()
            if index == len(tokens) or tokens[index] != ")":
                raise ValueError("expression has an unmatched parenthesis")
            index += 1
            return result
        index += 1
        if symbol.isdigit():
            value = int(symbol)
            return {} if value == 0 else {(): value}
        if fullmatch(r"[a-z]+", symbol, flags=0) is not None:
            if symbol in substitutions:
                value = substitutions[symbol]
                return {} if value == 0 else {(): value}
            return {(symbol,): 1}
        raise ValueError("expected a number, variable, or parenthesized expression")

    def parse_term() -> Polynomial:
        nonlocal index
        result = parse_factor()
        while index < len(tokens) and tokens[index] == "*":
            index += 1
            result = multiply(result, parse_factor())
        return result

    def parse_expression() -> Polynomial:
        nonlocal index
        result = parse_term()
        while index < len(tokens) and tokens[index] in ("+", "-"):
            operator = tokens[index]
            index += 1
            result = add(result, parse_term(), 1 if operator == "+" else -1)
        return result

    polynomial = parse_expression()
    if index != len(tokens):
        raise ValueError("expression has an unexpected token")
    terms = sorted(polynomial.items(), key=lambda term: (-len(term[0]), term[0]))
    return ["*".join((str(coefficient), *monomial)) for monomial, coefficient in terms]
```

The parser enforces precedence while each operation maintains one coefficient
per canonical monomial. That prevents duplicate like terms from accumulating
between operations.

**Complexity:** `O(T^2 * d log d)` for a multiplication of `T` sparse terms
with degree at most `d`; space is `O(Td)` for the resulting polynomial.
